import logging

import irc.bot

logger = logging.getLogger(__name__)


class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, username, token, server, port=6667):
        logger.debug("Instantiating bot.")
        super().__init__([(server, port, "oauth:" + token)], username, username)
        self.channel = channel
        self.chatters = []

    def stop(self):
        c = self.connection
        logger.debug("Sending departing message.")
        c.privmsg(self.channel, "I'm out!")
        logger.debug("Disconnecting.")
        self.disconnect()

    # Courtesy methods

    def welcome_chatter_if_new(self, e):
        # Collapse array of single-key dictionaries into one dictionary
        tags_dict = {}
        for tag in e.tags:
            tags_dict[tag["key"]] = tag["value"]

        chatter = tags_dict["display-name"]

        if chatter is not None:
            if chatter not in self.chatters and chatter is not self.channel:
                logger.debug("Adding chatter to list of chatters.")
                self.chatters.append(chatter)

                logger.info(f'Welcoming new chatter "{chatter}".')
                logger.debug("Sending hello message in IRC channel.")
                c = self.connection
                c.privmsg(self.channel, f"Hello {chatter}!")

    # Event-based methods

    def on_nicknameinuse(self, c, e):
        logger.debug("Selecting alternate nickname.")
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        logger.debug("Received server welcome.")
        logger.info("Joining " + self.channel)

        # You must request specific capabilities before you can use them
        logger.debug("Setting Twitch chat capabilities.")
        c.cap("REQ", ":twitch.tv/membership")
        c.cap("REQ", ":twitch.tv/tags")
        c.cap("REQ", ":twitch.tv/commands")

        logger.debug("Joining IRC channel.")
        c.join(self.channel)
        logger.debug("Sending starting message in IRC channel.")
        c.privmsg(self.channel, "I have arrived.")

    def on_privmsg(self, c, e):
        logger.debug(f"e: {str(e)}")

        message = e.arguments[0]
        logger.info(f"private message: {message}")
        self.do_command(e, message)

    def on_pubmsg(self, c, e):
        logger.debug(f"e: {str(e)}")

        message = e.arguments[0]
        logger.info(f"public message: {message}")

        self.welcome_chatter_if_new(e)

        self.do_command(e, message)

    # def on_dccmsg(self, c, e):
    #     print(f"dcc message: {str(e)}")

    def do_command(self, e, cmd):
        if cmd is None:
            return None

        c = self.connection

        logger.debug(f"cmd: {cmd}")
        if cmd.startswith("!"):
            command_word = cmd.split()[0]
            c.privmsg(
                self.channel,
                f"I do not know what to do with the command {command_word}.",
            )
