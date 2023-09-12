# Turbot

Turbo Twitch bot?
European fish?
Who can say.

## Installation

    python -m pip install -r requirements.txt

## Configuration

Copy `.env.template` to `.env` and fill in the values.
Details on how to obtain these values are provided below.

### Registering a Twitch Application

As the user your bot will act as, log in to the [Twitch Developer Portal](https://dev.twitch.tv/).

From the [Twitch Developer Console page](https://dev.twitch.tv/console), click the "Register Your Application" button.
Your application can use these values:

- "Name" is the name of your unique bot application.
- "OAuth Redirect URLs" can be set to `http://localhost`.
Click the Add button.
- Category is "Chat bot"

When you have created your application, copy the "Client ID" value into your `.env` file.

### Getting a Twitch Token

Paste this URL into a browser, where `<your client id>` is the Client ID you retrieved in the above section.

    https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=<your client id>&redirect_uri=http://localhost&scope=chat%3Aread+chat%3Aedit

You will be redirected to a page where you can authorize the application.
When you authorize the application, it will attempt to redirect you back to your callback address.
Although this redirect will not succeed* the token will be present in the redirect URL.

Copy the token value from the redirect URL into your `.env` file.

More details are available at https://dev.twitch.tv/docs/irc/authenticate-bot/.

### Putting It All Together

With this information you can fill out your `.env` file.

- `USERNAME` is the account name that registered and authorized the application.
It should be all lowercase.
- `CHANNEL` is your channel name where the bot will respond to commands. It should be all lowercase.
- `CLIENT_ID` is the client ID you were provided when you registered the application on the Twitch Developer console page.
- `TOKEN` is the token you were provided when granting the application access for your user.

## Dependencies

Python `irc` module

Python `python-dotenv` module

## Resources

https://dev.twitch.tv/docs/irc/

https://dev.twitch.tv/docs/irc/authenticate-bot/

https://python-irc.readthedocs.io/en/latest/

https://github.com/jaraco/irc/blob/main/scripts/testbot.py#L38

https://github.com/twitchdev/chatbot-python-sample/tree/main

