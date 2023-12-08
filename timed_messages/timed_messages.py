import math
import os.path
import time
from collections import deque

# Load messages
# Determine message interval
# Spread messages out
# Return function that continues to trigger next message


MESSAGES_FILENAME = "timed_messages/timed_messages.txt"


def interval(number_of_messages):
    seconds_in_hour = 60 * 60

    if number_of_messages < 1:
        return seconds_in_hour

    return math.floor(number_of_messages / seconds_in_hour)


def read_messages():
    with open(MESSAGES_FILENAME) as messages_file:
        if os.path.isfile(MESSAGES_FILENAME) is False:
            raise FileExistsError("Messages file does not exist.")

        messages = messages_file.readlines()

        return messages


class TimedMessages:
    def __init__(self, bot):
        self.bot = bot

        self.messages = deque(read_messages())

        # Divide the number of seconds in an hour by the number of messages and drop precision
        self.interval_seconds = math.floor(len(self.messages) / (60 * 60))

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

            time.sleep(self.interval_seconds)

            self.bot.send_private_message(message)
