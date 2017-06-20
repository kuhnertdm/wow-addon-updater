import requests


def findZiploc(self, addonpage):
    if addonpage.startswith('https://mods.curse.com/addons/wow/'):
        return curse(addonpage)
    elif addonpage.startswith('http://git.tukui.org/'):
        return tukui(addonpage)
    else:
        print('Invalid addon page.')


def curse(addonpage):
    try:
        page = requests.get(addonpage + '/download')
        contentString = str(page.content)
        indexOfZiploc = contentString.find('data-href') + 11  # Will be the index of the first char of the url
        endQuote = contentString.find('"', indexOfZiploc)  # Will be the index of the ending quote after the url
        return contentString[indexOfZiploc:endQuote]
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        return ''


def tukui(addonpage):
    ziploc = addonpage + '/repository/archive.zip'  # TODO: Stop creating a new elvui-master folder with subfolders
    return ziploc
