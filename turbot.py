import logging
import sys
import threading
import time

from irc.client import ServerNotConnectedError

from config import load_config
from twitch.twitch_bot import TwitchBot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("turbot")

if __name__ == "__main__":

    def check_twitch_bot_is_connected(twitch_bot):
        logger.debug(f"connected is {twitch_bot.connection.is_connected()}")
        if twitch_bot.connection.is_connected() is False:
            twitch_bot.stop()

    server, username, channel, token = load_config.load()

    bot = TwitchBot(channel, username, token, server)
    bot_thread = threading.Thread(target=bot.start)
    bot_thread.daemon = True  # Setting as daemon so it terminates on exit
    timer_thread = threading.Timer(10, check_twitch_bot_is_connected, args=(bot,))

    try:
        logger.info("Starting Turbot. Press CTRL+C to exit.")
        logger.debug(f"Connecting to {server}...")

        bot_thread.start()
        timer_thread.start()
        timer_thread.join()

        while bot.connection.is_connected() is True:
            time.sleep(5)
    except ServerNotConnectedError:
        logger.debug("Not connected to IRC server. Exiting.")
    except KeyboardInterrupt:
        logger.info("Exiting.")

    bot.stop()
    sys.exit()
