import irc.bot


class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, username, token, server, port=6667):
        super().__init__([(server, port, "oauth:" + token)], username, username)
        self.channel = channel
        self.chatters = []

    def stop(self):
        c = self.connection
        c.privmsg(self.channel, "I'm out!")
        self.disconnect()

    def is_new_chatter(self, e):
        tags_dict = {}
        for tag in e.tags:
            tags_dict[tag["key"]] = tag["value"]

        chatter = tags_dict["display-name"]

        if chatter is not None:
            if chatter not in self.chatters:
                self.chatters.append(chatter)
                return chatter

        return None

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
        print(f"private message: {str(e)}")
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        print(f"public message: {str(e)}")
        chatter = self.is_new_chatter(e)
        if chatter is not None:
            c.privmsg(self.channel, f"Hello {chatter}!")

        self.do_command(e, e.arguments[0])

    # def on_dccmsg(self, c, e):
    #     print(f"dcc message: {str(e)}")

    def do_command(self, e, cmd):
        c = self.connection
        print(f"cmd: {cmd}")
        c.privmsg(self.channel, f"{cmd} command received.")
