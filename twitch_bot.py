import irc.bot


class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, username, token, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(
            self, [(server, port, "oauth:" + token)], username, username
        )
        self.channel = channel

    def stop(self):
        c = self.connection
        c.privmsg(self.channel, "I'm out!")
        self.disconnect()

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        print("Joining " + self.channel)

        # You must request specific capabilities before you can use them
        c.cap("REQ", ":twitch.tv/membership")
        c.cap("REQ", ":twitch.tv/tags")
        c.cap("REQ", ":twitch.tv/commands")

        c.join(self.channel)
        c.privmsg(self.channel, "I have arrived.")

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    # def on_dccmsg(self, c, e):
    #     pass

    def do_command(self, e, cmd):
        c = self.connection
        print(f"cmd: {cmd}")
        c.privmsg(self.channel, f"{cmd} command received.")
