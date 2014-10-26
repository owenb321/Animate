#Prismatik Animate plugin

##Description
This is a port of the Animate plugin for Prismatik, originally written by [Atarity](https://github.com/Atarity/Prismatik-plugins).

## Version 0.1

##Dependencies
* Python 2.7
* Prismatik (tested on 5.11.1)

##Installation
* Install Python 2.7
* Download the ZIP from the repository
* Unzip to a new local folder
* In Prismatik:
  * Enable the API
    * Enable `Expert mode` under `Profiles`
    * Check `Enable server` under `Experimental`
* Place the unzipped folder in the Prismatik plugins directory (e.g. `C:\Users\owenb321\Prismatik\Plugins\Animate`)
* Adjust settings in the Animate.ini file
* Refresh the plugin list in Prismatik

##Configuration
Settings are configured in the `Animate.ini` file.
* Main
  * These are used by Prismatik to identify the plugin
* Lightpack
  * `host` - Address of the API server. `127.0.0.1` is the local machine.
  * `port` - API server port number. `3636` is the Prismatik default.
  * `ledmap` - Specifies the clockwise order of your LEDs (comma-separated). This is needed for the Snake animation. LED numbers can be found on the screen grabber setup boxes. If commented out, the Snake animation defaults to an ordered list of all LEDs
  * `cylonmap` - Specifies groups of LEDs to use for the Cylon animation. Groups are semicolon-separated, LEDs within the groups are comma-separated. For example, the default setting is `10,9,8; 7,6; 5,4; 3,2,1` in these groups, `10,9,8'`are the left side LEDs, `7,6` are the top-left `5,4` are the top-right, and `3,2,1` are the right side. If commented out, these default groups are used.
* Animation
  * `type` - Selects animation type; 1 = 1-dimension plasm, 2 = Disco distro, 3 = Snake, 4 = Cylon