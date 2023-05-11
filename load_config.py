import os

from dotenv import load_dotenv


def load():
    load_dotenv()
    server = os.getenv("IRC_SERVER")
    username = os.getenv("USERNAME")
    channel = os.getenv("CHANNEL")
    token = os.getenv("TOKEN")

    return server, username, channel, token
