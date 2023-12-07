import time


# Load messages
# Determine message interval
# Spread messages out
# Return function that continues to trigger next message


class TimedMessages():
    def __init__(self, bot):
        self.bot = bot
        self.interval = 0

    def next_message(self):
        bot = self.bot
        print("ping")
        pass

    def message_loop(self):
        self.interval = 1  # Temporary value
        while True:
            self.next_message()
            time.sleep(self.interval)
