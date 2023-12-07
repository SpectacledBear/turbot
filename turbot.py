import logging
import sys
import threading
import time

from irc.client import ServerNotConnectedError

from config import load_config
from timed_messages.timed_messages import TimedMessages
from twitch.twitch_bot import TwitchBot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("turbot")

if __name__ == "__main__":

    def check_twitch_bot_is_connected(twitch_bot):
        logger.debug(f"connected is {twitch_bot.connection.is_connected()}")
        if twitch_bot.connection.is_connected() is False:
            twitch_bot.stop()

    server, username, channel, token = load_config.load()

    logger.info("Starting Turbot. Press CTRL+C to exit.")
    logger.debug(f"Connecting to {server}...")

    bot = TwitchBot(channel, username, token, server)
    bot_thread = threading.Thread(target=bot.start)
    bot_thread.daemon = True  # Setting as daemon so it terminates on exit
    # Register commands
    # Scheduled messages thread
    timed_messages = TimedMessages(bot)
    timed_messages_thread = threading.Thread(target=timed_messages.message_loop)
    # CLI thread
    # switch to CLI thread
    bot_thread.start()
    # Do I want a connection retry mechanism here with timeout?
    timed_messages_thread.start()

    try:
        while bot.connection.is_connected() is True:
            time.sleep(5)
    except ServerNotConnectedError:
        logger.debug("Not connected to IRC server. Exiting.")
    except KeyboardInterrupt:
        logger.info("Exiting.")

    bot.stop()
    bot_thread.join(5)
    sys.exit()
