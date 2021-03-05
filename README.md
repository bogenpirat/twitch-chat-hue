# twitch-chat-hue
A script that will turn your hue lights to the nick color that the latest chatter has.

# installation
install the deps:

```
pip install -r requirements.txt
```

# configuration
create a file called `.env` in the directory with the following, filled in contents:
```
BRIDGE_IP="192.168.0.100"
TWITCH_NICKNAME="somenick"
TWITCH_CHANNEL="somechanwithoutthepoundsign"
TWITCH_OAUTH="oauthtoken"
TRANSITION_TIME=10
```

note that transition time is in deciseconds (tenths of a second), so e.g. 10dsec = 1sec.

# run the code
on the first run, you need to pair the hue hub with the script. this is done by briefly pressing the link button on the device and then, within less than 30 seconds, running the script.

from a terminal:
```
python chattercolor.py
```
from the windows explorer, click on `start.cmd` in the folder

# additional configuration
`LIGHTS_TO_MANIPULATE` can be altered in the code to allow for more granular lights selection - by default the script will attempt to use every light attached to the bridge. valid configuration values are integers for ids, or names.

# parameter details

* `hue` is a 16 bit value (0-65535), so from an HSB model with 360° for its hue parameter, you'll want to multiply H by 182.04 to get a philips hue-expected hue.
* `saturation` is an 8 bit value (0-255), so just multiply a (0.0 - 1.0) value by 255 and round the result
* `brightness` behaves the same as `saturation`
* `transitiontime` is expected in **deciseconds**, so tenths of a second. 3 seconds are 30 deciseconds.

some more technical information: http://rsmck.co.uk/hue
