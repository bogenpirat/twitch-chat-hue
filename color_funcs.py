import re
import colorsys
import time

from mylog import log


def rgbhex2dec(rgbStr):
    rgbStr = rgbStr.lstrip('#')
    return tuple(int(rgbStr[i:i+2], 16) for i in (0, 2, 4))

def set_color(c, e, settings):
    color = next((x for x in e.tags if x['key'] == 'color'), {'value': '#000000'})['value']
    b = settings['HUE_BRIDGE']

    if not isinstance(color, str) or not re.match('^#?[0-9a-zA-Z]{6}$', color):
        return

    rgb = rgbhex2dec(color)
    hsl = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)

    hue = round(hsl[0] * 360 * 182.04)
    sat = round(hsl[1] * 254)
    bri = round(hsl[2] * 254)

    log(f'sending color rgb{color} => hsb({hue}, {sat}, {bri})')

    for l in settings['LIGHTS_TO_MANIPULATE']:
        b.set_light(int(l), {
            'transitiontime': settings['TRANSITION_TIME'],
            'on': True,
            'hue': hue,
            'bri': 254, # for better effect, set to max
            'sat': sat
            })


def handle_alarm(c, e, settings):
    #user_type = next((x for x in e.tags if x['key'] == 'user-type'), {'value': None})['value']
    if e.arguments[0].strip().lower() == '!alarm':
        log("aaaalaaaAAAAAARM")

        b = settings['HUE_BRIDGE']

        # store old states
        old_state = [ {
                'on': l.on,
                'hue': l.hue,
                'bri': l.brightness,
                'sat': l.saturation
                } for l in b.lights ]


        # do some visual alarm stuff
        for i in range(settings['ALARM_CYCLES']):
            for l in settings['ALARM_LIGHTS']: # set 1st alarm color
                log('color: red')
                b.set_light(int(l), { 'transitiontime': 1, 'on': True, 'hue': 0, 'bri': 254, 'sat': 254 })

            time.sleep(settings['ALARM_RISEFALL_TIME']) # remain on that color

            for l in settings['ALARM_LIGHTS']: # set 2nd alarm color
                log('color: green')
                b.set_light(int(l), { 'transitiontime': 1, 'on': True, 'hue': 21844, 'bri': 254, 'sat': 254 })

            if i < settings['ALARM_CYCLES'] - 1: # only wait if loop's not over yet
                time.sleep(settings['ALARM_RISEFALL_TIME']) # remain on that color

        # recover old state
        for l in settings['ALARM_LIGHTS']:
            l = int(l)
            b.set_light(l, {
                'transitiontime': 0,
                'on': old_state[l-1]['on'],
                'hue': old_state[l-1]['hue'],
                'bri': old_state[l-1]['bri'],
                'sat': old_state[l-1]['sat']
                })