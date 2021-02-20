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
from a terminal:
```
python chattercolor.py
```
from the windows explorer, click on `start.cmd` in the folder

# additional configuration
`LIGHTS_TO_MANIPULATE` can be altered in the code to allow for more granular lights selection - by default the script will attempt to use every light attached to the bridge. valid configuration values are integers for ids, or names.

# parameter details
http://rsmck.co.uk/hue