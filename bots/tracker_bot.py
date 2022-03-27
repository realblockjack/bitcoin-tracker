#!/usr/bin/env python
# References: this code builds on:
# [1] https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/timerbot.py
# [2] https://www.section.io/engineering-education/cryptocurrency-tracking-telegram-bot/
# [3] https://realpython.com/twitter-bot-python-tweepy/

import logging, requests, os

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    update.message.reply_text('Hi! Use /set <seconds> to set an interval')


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(crypto_update, interval=due, first=10, context=chat_id, name=str(chat_id))

        text = 'Timer successfully set!'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def crypto_update(context: CallbackContext) -> None:
    """Send the alarm message.
        #change_hour = crypto_data[i]["change_hour"]
        #message += f"Coin: {coin}\nPrice: €{price:,.2f}\nHour Change: {change_hour:.2f}%\nDay Change: {change_day:.2f}%\n\n"
    """
    job = context.job
    message = ""

    crypto_data = get_prices()
    for i in crypto_data:
        coin = crypto_data[i]["coin"]
        price = crypto_data[i]["price"]
        change_day = crypto_data[i]["change_day"]
        message += f"Coin: {coin}\nPrice: €{price:,.2f}\nDay Change: {change_day:.2f}%\n\n"
    context.bot.send_message(job.context, text=message)


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)


def get_prices() -> dict:
    coins = ["BTC", "ETH", "DOGE", "ADA"]

    crypto_data = requests.get(
        "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=EUR".format(",".join(coins))).json()["RAW"]

    data = {}
    for i in crypto_data:
        data[i] = {
            "coin": i,
            "price": crypto_data[i]["EUR"]["PRICE"],
            "change_day": crypto_data[i]["EUR"]["CHANGEPCT24HOUR"],
            "change_hour": crypto_data[i]["EUR"]["CHANGEPCTHOUR"]
        }

    return data


def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    bot_token = os.getenv("BOT_TOKEN")
    updater = Updater(bot_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("set", set_timer))
    dispatcher.add_handler(CommandHandler("unset", unset))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()