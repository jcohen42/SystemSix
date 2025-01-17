<p align="center">
<img width="212" src="https://github.com/jcohen42/SystemSix/blob/main/documentation/SystemSixLogo.png" alt="SystemSix">
</p>

This project is a fork of [the original SystemSix](https://github.com/EngineersNeedArt/SystemSix), made by EngineersNeedArt. SystemSix is a "desk accessory" running on a Raspberry Pi. This project differs from the main repository in that it is intended to be run on an LCD display that can handle diplaying images at a resolution of 512 x 384. It also allows you to swap out the calendar list display with bus arrival times for your nearby bus stops using the OneBusAway API.

<p align="center">
<img src="https://github.com/jcohen42/SystemSix/blob/main/documentation/DisplaySample.jpg" alt="SystemSix screenshot.">
</p>

### Features

• Calendar date is displayed.

• Retrieves and displays your first four calendar events for the day, refreshes in the evening.

• Optionally replace calendar list with a list of live bus arrival times using the OneBusAway API. You must provide your own API key.

• Retrieves and displays the local weather forecast at the start of each day.

• Current phase of the moon displayed. (New moon? Maybe you get a Calculator instead.)

• Specify "trash day" and on that day of the week, the trash can icon will display full. Can be a handy reminder.

• Several different overall layouts and a random selection from over 100 classic icons means you wake up to a surprise desktop every day.

<p align="center">
<img width="768" src="https://github.com/jcohen42/SystemSix/blob/main/documentation/SystemSixDisplayed.jpg" alt="SystemSix">
</p>

I have my computer running on a 8" 1024 x 768 display, mounted using a 3D-printed mount I found on Thingiverse. My Pi is running Raspberry Pi OS, and is set to automatically run the `run_systemsix.sh` script upon login.


### Running

If you are new to Python as I was: briefly, you pull down the sources and open `systemsix.py` in a Python IDE (example: Thonny, that generally comes pre-installed on the Raspberry Pi — on a desktop OS, PyCharm is a popular one). Then you *run* it.

Hopefully the `requirements.txt` file covers the needed Python modules and you have no problems running SystemSix. (Hopefully too your Python environment already is pointing to Python3 and not an older Python implmentation.)

You'll also need to install `feh` in order to display the image on your screen. You can do so by running `sudo apt install feh -y`. If you want to quit to the Desktop while SystemSix is running, simply click Q or Escape on your keyboard.

BEWARE: The e-ink display functionality might be broken in this fork. In `systemsix.py`, there is a flag at the top: `USE_EINK_DISPLAY`. Set this to `False` and you can run `systemsix.py` in any environment, even without an e-ink display attached. The workflow for updating the e-ink display involves first creating the image that you want displayed. Most of the code in SystemSix is doing just that: creating the final image of the desktop. When you set `USE_EINK_DISPLAY` to `False` the final image is instead opened in your current OS environment, not sent to the e-ink driver. (On MacOS it is Preview that is launched to display the resulting image.)

See the *Settings* section below on how to customize SystemSix and personalize it.

To dedicate a Raspberry Pi to run SystemSix headless, you can create an entry in the Wayfire config.

In the Terminal app on a Raspberry Pi I entered:

`nano ~/.config/wayfire.ini`

This brings up a text editor in Terminal. Then I scrolled down to the bottom of the file and added these lines:

```
[autostart]
systemsix = /home/pi/SystemSix/run_systemsix.sh
dpms_timeout=300
```

This says that after logging in, the computer will run the shell script named `run_systemsix.sh` located at the path `/home/pi/SystemSix/`. Replace the user `pi` with your username if yours differs. If you pulled the files down somewhere else you will have a different path to the shell script file. The `dpms_timeout` block configures the screen to turn off after 300 seconds (5 minutes), feel free to change as desired.

### Settings

"Trash day" is defined in `Settings.py` as an integer. Set the value to `1` for Monday, `2` for Tuesday, etc. Setting the value to `None` will cause the trash to never be shown full. Set to any other value to indicate that "trash day" should be random.

For the weather API I use, `LATITUDE` and `LONGITUDE` should be supplied in `Settings.py`. I query [api.weather.gov](api.weather.gov) to turn the LAT/LONG into an office ID and grid X and Y that weather.gov uses to retrieve local forecasts.

To display your upcoming calendar events the settings and code are the same as the implementation from 13Bytes. I can only speak to my experiences with MacOS Calendar. `WEBDAV_IS_APPLE` I set to `True` and for `WEBDAV_CALENDAR_URL` I entered the URL to fetch my public calendar.

Figuring out my calendar URL turned out to be a challenge. In the end I had to create a new calendar in Apple's Calendar app and make sure to mark it as *public*. Then I found the sharing affordance in Calendar and "shared" the calendar with myself (I emailed it to myself). The link in the email contained the (150+ character) URL that I was then able to paste into `Settings.py`. Mine started out like this: `webcal://p97-caldav.icloud.com/published/2/NDYyNT....`.

`REFRESH_SECONDS` determines how often SystemSix generates a new image. This is particularly userful for updating bus arrival times. If you don't want to display bus information, setting this value to~4 hours should suffice.

If you'd rather display bus arrival times in [supported regions](https://onebusaway.org/onebusaway-deployments/) using OneBusAway, you must set `REPLACE_CALENDAR_WITH_BUS_SCHEDULE` to `True` and provide an API key. You can then supply any number of bus stop IDs in the `ONEBUSAWAY_STOP_IDS` list.
