# A Bitcoin tracker using Python, Telegram and Docker

This repository contains a simple Python script that can be used to run a Bitcoin tracker. A Telegram bot updates the user on the latest price of Bitcoin, Ethereum, Doge Coin and Cardano following a pre-defined interval. In order to use this code, a Telegram bot has to be created in advance and - more importantly - the Bot's token has to be provided in form of an environmental variable.

This repository builds on the resources provided by [1], [2], and [3].

## How to get started

Clone the repository:

```bash
git clone https://github.com/realblockjack/bitcoin-tracker.git
cd bitcoin-tracker/
```

Create the Docker container:
```bash
docker build . -t tracker-bot
```

Look for the Token of your Telegram bot and run the Docker container on your system:
```python
docker run -it -e BOT_TOKEN="THE-TOKEN-OF-YOUR-BOT" tracker-bot
```

## Tips

Please feel free to alter this project as you desire. If you would like to express your gratitude, I invite you to use my [TIP JAR](https://coinos.io/blockjack).

## References

* [1] https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/timerbot.py
* [2] https://www.section.io/engineering-education/cryptocurrency-tracking-telegram-bot/
* [3] https://realpython.com/twitter-bot-python-tweepy/