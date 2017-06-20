# wow-addon-updater

This utility provides an alternative to the Twitch/Curse client for management and updating of addons for World of Warcraft. The Twitch/Curse client is rather bloated and buggy, and comes with many features that most users will not ever use in the first place. This utility, however, is lightweight and makes it very easy to manage which addons are being updated, and to update them just by running a python script.

## First-time setup

This utility has two dependencies:

* A version of [Python](https://www.python.org/) 3 (Any version of Python 3 should do)

* The [requests](http://docs.python-requests.org/en/master/) module

If you are familiar with Python / Pip / etc, and already have Pip installed or know how to install it, then installing this should be as easy as "pip install requests". If you don't know what any of those words mean, don't fret. I've included some extra files (namely "get-pip.py", "get-requests.py", and "setup.bat") that should automatically install everything you need. All you need to do is right click on "setup.bat" and run it as an administrator.

**NOTE: YOU MUST INSTALL PYTHON 3 ON YOUR OWN BEFORE RUNNING THE SETUP FILE. CLICK [HERE](https://www.python.org/downloads/) TO DO THAT FROM THE PYTHON SITE.**

*Note for concerned nerds: The "setup.bat" file just runs "get-pip.py" and then "get-requests.py". The "get-pip.py" file is the standard file for easily installing Pip in a windows environment, and you may have seen it elsewhere on the internet. The "get-requests.py" file just has Pip install the requests module.*

## Configuring the utility

The "config.ini" file is used by the utility to find where to install the addons to, and where to get the list of mods from.

The default location to install the addons to is "C:\Program Files (x86)\World of Warcraft\Interface\AddOns". If this is not the location where you have World of Warcraft installed, you will need to edit "config.ini" to point to your addons folder.

The default location of the addon list file is simply "in.txt", but this file will not exist on your PC, so you should either create "in.txt" in the same location as the utility, or name the file something else and edit "config.ini" to point to the new file.

## Input file format

Whatever file you use for your list of mods needs to be formatted in a particular way. Each line corresponds to a mod, and the line just needs to contain the link to the Curse page for the mod. For example:

    https://mods.curse.com/addons/wow/world-quest-tracker
    https://mods.curse.com/addons/wow/deadly-boss-mods
    https://mods.curse.com/addons/wow/auctionator
    
Each link needs to be the main page for the addon, as shown above.

## Running the utility

After configuring the utility and setting up your input file, updating your addons is as simple as double clicking the "WoWAddonUpdater.py" file.

*Note: The more addons you have in your list, the longer it will take to update them... Duh.*

## Contact info

Have any questions, concerns, issues, or suggestions for the utility? Feel free to either submit an issue through Github or email me at kuhnerdm@gmail.com. Please put in the subject line that this is for the WoW Addon Updater.

## Future plans

* Make a video guide detailing all the above information

* Update to use a visual interface instead of a command-line interface

* Make the code structure not suck. No, seriously... it's bad...

Thanks for checking this out; hopefully it helps a lot of you :)
