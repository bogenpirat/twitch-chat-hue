from phue import Bridge
import colorsys
import irc.bot
import os
import re
from dotenv import load_dotenv

load_dotenv()

TWITCH_CHAT_SERVER = 'irc.chat.twitch.tv'
TWITCH_CHAT_SERVER_PORT = 6667

BRIDGE_IP = os.getenv('BRIDGE_IP')
TWITCH_NICKNAME = os.getenv('TWITCH_NICKNAME')
TWITCH_OAUTH = os.getenv('TWITCH_OAUTH')
TWITCH_CHANNEL = os.getenv('TWITCH_CHANNEL')
TRANSITION_TIME = int(os.getenv('TRANSITION_TIME', 10)) # 1sec
LIGHTS_TO_MANIPULATE = None # None to get all, or [ 1, 2, 3 ], or [ 'names', ... ]

def rgbhex2dec(rgbStr):
    rgbStr = rgbStr.lstrip('#')
    return tuple(int(rgbStr[i:i+2], 16) for i in (0, 2, 4))

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, token, channel, color_func):
        self.channel = channel
        self.token = token
        self.color_func = color_func
        irc.bot.SingleServerIRCBot.__init__(self, [(TWITCH_CHAT_SERVER, TWITCH_CHAT_SERVER_PORT, 'oauth:' + token)], username, username)

    def on_welcome(self, c, e):
        print('welcome')
        
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')

        c.join('#' + self.channel)

    def on_pubmsg(self, c, e):
        color = next((x for x in e.tags if x['key'] == 'color'), {'value': '#000000'})['value']
        
        self.color_func(color)

        return

    def on_action(self, c, e):
        return self.on_pubmsg(c, e)

if __name__ == '__main__':
    b = Bridge(BRIDGE_IP)
    b.connect()

    if not LIGHTS_TO_MANIPULATE:
        LIGHTS_TO_MANIPULATE = b.lights

    def set_color(color):
        if not isinstance(color, str) or not re.match('^#?[0-9a-zA-Z]{6}$', color):
            return

        rgb = rgbhex2dec(color)
        hsl = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)

        hue = round(hsl[0] * 360 * 182.04)
        sat = round(hsl[1] * 254)
        bri = round(hsl[2] * 254)

        print(f'sending color rgb{color} => hsb({hue}, {sat}, {bri})')

        lights = b.get_light_objects('name')
        selected_lights = list(lights.keys())[-2:]
        for l in selected_lights:
            lights[l].transitiontime = TRANSITION_TIME
            lights[l].on = True
            lights[l].hue = hue
            lights[l].brightness = 254 #bri
            lights[l].saturation = sat

    bot = TwitchBot(TWITCH_NICKNAME, TWITCH_OAUTH, TWITCH_CHANNEL, set_color)
    bot.start()