import logging
import math
import os.path
import time
from collections import deque

MESSAGES_FILENAME = "timed_messages/timed_messages.txt"

logger = logging.getLogger(__name__)


def interval(number_of_messages):
    seconds_in_hour = 60 * 60

    if number_of_messages < 1:
        return seconds_in_hour

    interval_seconds = math.floor(seconds_in_hour / number_of_messages)

    logger.debug(f"Setting interval to {interval_seconds} seconds.")

    return interval_seconds


def read_messages():
    with open(MESSAGES_FILENAME) as messages_file:
        if os.path.isfile(MESSAGES_FILENAME) is False:
            raise FileExistsError("Messages file does not exist.")

        messages = []

        logger.debug("Reading messages from text file.")
        lines = messages_file.readlines()

        for line in lines:
            messages.append(line.strip())

        return messages


class TimedMessages:
    def __init__(self, bot):
        self.bot = bot

        self.messages = deque(read_messages())

        # Divide the number of seconds in an hour by the number of messages and drop precision
        self.interval_seconds = interval(len(self.messages))

    def next_message(self):
        if len(self.messages) < 1:
            return ""

        message = self.messages[0]

        self.messages.popleft()
        self.messages.append(message)

        return message

    def message_loop(self):
        while True:
            message = self.next_message()

            self.bot.send_private_message(message)

            time.sleep(self.interval_seconds)
