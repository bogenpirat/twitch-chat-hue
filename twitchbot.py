import asyncio
import irc.bot

from mylog import log

TWITCH_CHAT_SERVER = 'irc.chat.twitch.tv'
TWITCH_CHAT_SERVER_PORT = 6667

class TwitchBot(irc.bot.SingleServerIRCBot):
    listeners = []

    def __init__(self, settings):
        self.channel = settings['TWITCH_CHANNEL']
        self.token = settings['TWITCH_OAUTH']
        self.settings = settings
        irc.bot.SingleServerIRCBot.__init__(self, [(TWITCH_CHAT_SERVER, TWITCH_CHAT_SERVER_PORT, 'oauth:' + self.token)], settings['TWITCH_NICKNAME'], settings['TWITCH_NICKNAME'])

    def add_listener(self, listener):
        self.listeners.append(listener)

    def on_welcome(self, c, e):
        log('twitch says hi 👋')
        
        log('requesting caps')
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')

        log(f'joining {self.channel}')
        c.join('#' + self.channel)

    def on_pubmsg(self, c, e):
        for listener in self.listeners:
            print(f'func IN: {listener}') # TODO: debugging
            listener(c, e, self.settings)
            print(f'func OUT: {listener}') # TODO: debugging

        return

    def on_action(self, c, e): # just redirect to pubmsg
        return self.on_pubmsg(c, e)