from logging import log
from phue import Bridge
import os
from dotenv import load_dotenv

from twitchbot import TwitchBot
from color_funcs import set_color, handle_alarm
from mylog import log

load_dotenv()

settings = {
    'BRIDGE_IP': os.getenv('BRIDGE_IP'),
    'TWITCH_NICKNAME': os.getenv('TWITCH_NICKNAME'),
    'TWITCH_OAUTH': os.getenv('TWITCH_OAUTH'),
    'TWITCH_CHANNEL': os.getenv('TWITCH_CHANNEL'),
    'TRANSITION_TIME': int(os.getenv('TRANSITION_TIME', 10)), # 1sec
    'LIGHTS_TO_MANIPULATE': os.getenv('LIGHTS_TO_MANIPULATE', '').split(' ') if os.getenv('LIGHTS_TO_MANIPULATE', None) != None else None,
    'ALARM_LIGHTS': os.getenv('ALARM_LIGHTS', '').split(' ') if os.getenv('ALARM_LIGHTS', None) != None else None,
    'ALARM_CYCLES': int(os.getenv('ALARM_CYCLES', 5)),
    'ALARM_RISEFALL_TIME': float(os.getenv('ALARM_RISEFALL_TIME', 0.3)),
}

if __name__ == '__main__':
    # Hue connection
    log('connecting to hue')
    settings['HUE_BRIDGE'] = Bridge(settings['BRIDGE_IP'])
    settings['HUE_BRIDGE'].connect()
    config = settings["HUE_BRIDGE"].get_api()["config"]
    log(f'hue connected: {config["name"]} ({config["ipaddress"]})')

    if not settings['LIGHTS_TO_MANIPULATE']:
        settings['LIGHTS_TO_MANIPULATE'] = settings['HUE_BRIDGE'].lights
    if not settings['ALARM_LIGHTS']:
        settings['ALARM_LIGHTS'] = settings['LIGHTS_TO_MANIPULATE']

    bot = TwitchBot(settings)

    #bot.add_listener(lambda c, e, settings: print(f'setting color for {e.source}')) # TODO: debugging
    bot.add_listener(set_color)
    bot.add_listener(handle_alarm)

    bot.start()