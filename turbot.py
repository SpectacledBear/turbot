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
    server, username, channel, token = load_config.load()

    logger.info("Starting Turbot. Press CTRL+C to exit.")
    logger.debug(f"Connecting to {server}...")

    bot = TwitchBot(channel, username, token, server)
    bot_thread = threading.Thread(target=bot.start)
    bot_thread.daemon = True  # Setting as daemon so it terminates on exit
    # Register commands
    timed_messages = TimedMessages(bot)
    timed_messages_thread = threading.Thread(target=timed_messages.message_loop)

    try:
        bot_thread.start()
        time.sleep(5)

        connection_attempt = 0
        while bot.connection.is_connected() is False:
            connection_attempt += 1

            if connection_attempt > 5:
                raise ServerNotConnectedError()

            logger.debug(f"Connection attempt {connection_attempt}")

            bot.connection.disconnect()
            bot.connection.connect()

            time.sleep(5)

        logger.debug("Sending starting message in IRC channel.")
        bot.send_private_message("Hi, I'm Turbot, a bot created by ASolitaryBear. "
                                 "You can find out more about me at https://github.com/SpectacledBear/turbot.")

        # Scheduled messages thread
        timed_messages_thread.start()
        # CLI thread
        # switch to CLI thread
        # Do I want a connection retry mechanism here with timeout?

        while bot.connection.is_connected() is True:
            time.sleep(5)

        raise ServerNotConnectedError()
    except ServerNotConnectedError:
        logger.info("Not connected to IRC server. Exiting.")
    except KeyboardInterrupt:
        logger.info("Exiting.")

    logger.debug("Sending departing message.")
    bot.send_private_message("I'm out!")
    bot.stop()
    bot_thread.join(5)

    sys.exit()
