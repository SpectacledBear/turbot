import load_config
from twitch_bot import TwitchBot

if __name__ == "__main__":
    server, username, channel, token = load_config.load()

    bot = TwitchBot(channel, username, token, server)

    try:
        print(f"Connecting to {server}...")
        bot.start()
    except KeyboardInterrupt:
        bot.stop()
