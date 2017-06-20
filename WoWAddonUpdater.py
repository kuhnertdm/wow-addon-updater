import requests, zipfile, configparser
from io import *
from os.path import isfile


def confirmExit():
    input('\nPress the Enter key to exit')
    exit(0)


class AddonUpdater:
    def __init__(self):
        print('')

        # Read config file

        if not isfile('config.ini'):
            print(
                'Failed to read configuration file. Are you sure there is a file called "config.ini" with the "WowAddonUpdater.py" file?')
            confirmExit()

        config = configparser.ConfigParser()
        config.read('config.ini')

        try:
            self.WOW_ADDON_LOCATION = config['WOW ADDON UPDATER']['WoW Addon Location']
            self.ADDON_LIST_FILE = config['WOW ADDON UPDATER']['Addon List File']
        except Exception:
            print('Failed to parse configuration file. Are you sure it is formatted correctly?')
            confirmExit()

        if not isfile(self.ADDON_LIST_FILE):
            print('Failed to read addon list file. Are you sure the file exists?')
            confirmExit()
        return

    def update(self):

        # Main process (yes I formatted the project badly)

        with open(self.ADDON_LIST_FILE, "r") as fin:
            for line in fin:
                print('Installing/updating addon: ' + line)
                ziploc = self.findZiploc(line.rstrip('\n'))
                self.getAddon(ziploc)

    def getAddon(self, ziploc):
        if ziploc == '':
            return
        try:
            r = requests.get(ziploc, stream=True)
            z = zipfile.ZipFile(BytesIO(r.content))
            z.extractall(self.WOW_ADDON_LOCATION)
        except Exception:
            print('Failed to download or extract zip file for addon. Skipping...\n')
            return

    def findZiploc(self, addonpage):
        import SiteHandler
        if addonpage.startswith('https://mods.curse.com/addons/wow/'):
            return SiteHandler.curse(addonpage)
        else:
            print('Invalid addon page. Make sure you are using the Curse page for the addon.')
            confirmExit()


def main():
    addonupdater = AddonUpdater()
    addonupdater.update()

    return


if __name__ == "__main__":
    # execute only if run as a script
    main()
