from dotenv import load_dotenv
import os
from phue import Bridge
import random
import time

load_dotenv()

def lightning():
    b = Bridge(os.getenv('BRIDGE_IP'))
    lights = [ int(i) for i in os.getenv('ALARM_LIGHTS', '').split(' ') ]
    b.create_group('alarmlichter', lights)

    # store old states
    old_state = [ {
            'on': l.on,
            'hue': l.hue,
            'bri': l.brightness,
            'sat': l.saturation
            } for l in b.lights ]
    
    # make flashy epilepsy magic
    total_duration = 0
    flash = True
    while total_duration < float(os.getenv('LIGHTNING_DURATION', 3)):
        cmd = { 
            'transitiontime': 0,
            'sat': 0,
            'bri': 254 if flash else 0,
            }
        
        duration = random.choice([ 
            float(os.getenv('LIGHTNING_SHORT_FLASH', 0.1)),
            float(os.getenv('LIGHTNING_LONG_FLASH', 0.5))
            ]) if not flash else float(os.getenv('LIGHTNING_SHORT_FLASH', 0.1))
        
        total_duration = total_duration + duration
        
        b.set_group('alarmlichter', cmd)

        time.sleep(duration)
        
        flash = not flash


    # recover old state
    for l in lights:
        b.set_light(l, {
            'transitiontime': 0,
            'on': old_state[l-1]['on'],
            'hue': old_state[l-1]['hue'],
            'bri': old_state[l-1]['bri'],
            'sat': old_state[l-1]['sat']
            })
    
    # delete group
    b.delete_group('alarmlichter')


if __name__ == '__main__':
    lightning()