import logging

import load_config
from twitch_bot import TwitchBot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("turbot")

if __name__ == "__main__":
    server, username, channel, token = load_config.load()

    bot = TwitchBot(channel, username, token, server)

    try:
        logger.info("Starting Turbot. Press CTRL+C to exit.")
        logger.debug(f"Connecting to {server}...")
        bot.start()
    except KeyboardInterrupt:
        logger.info("Exiting.")
        bot.stop()
