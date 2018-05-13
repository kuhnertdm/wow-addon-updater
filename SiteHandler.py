import packages.requests as requests
import re
import zipfile
import os
import tempfile
import shutil
from io import *

# Site splitter

def findZiploc(addonpage):
    # Curse
    if addonpage.startswith('https://mods.curse.com/addons/wow/'):
        return curse(convertOldCurseURL(addonpage))
    elif addonpage.startswith('https://www.curseforge.com/wow/addons/'):
        return curse(addonpage)

    # Curse Project
    elif addonpage.startswith('https://wow.curseforge.com/projects/'):
        return curseProject(addonpage)
		
    # Tukui
    elif addonpage.startswith('https://git.tukui.org/'):
        return tukui(addonpage)

    # Wowinterface
    elif addonpage.startswith('http://www.wowinterface.com/'):
        return wowinterface(addonpage)

    # Invalid page
    else:
        print('Invalid addon page.')


def getCurrentVersion(addonpage):
    # Curse
    if addonpage.startswith('https://mods.curse.com/addons/wow/'):
        return getCurseVersion(convertOldCurseURL(addonpage))
    elif addonpage.startswith('https://www.curseforge.com/wow/addons/'):
        return getCurseVersion(addonpage)

    # Curse Project
    elif addonpage.startswith('https://wow.curseforge.com/projects/'):
        return getCurseProjectVersion(addonpage)
		
    # Tukui
    elif addonpage.startswith('https://git.tukui.org/'):
        return getTukuiVersion(addonpage)

    # Wowinterface
    elif addonpage.startswith('http://www.wowinterface.com/'):
        return getWowinterfaceVersion(addonpage)

    # Invalid page
    else:
        print('Invalid addon page.')

def installAddon(addonUrl, installPath):
    try:
        if addonUrl.lower().startswith(('https://mods.curse.com/',
            'https://www.curseforge.com/', 'http://www.wowinterface.com/')):
            installSingleLevelZip(addonUrl, installPath)
        elif addonUrl.startswith('https://git.tukui.org/'):
            installZippedGitRepo(addonUrl, installPath)
        else:
            print('Invalid addon URL.')
    except Exception as err:
        print('Failed to install ' + addonUrl)
        print(err)

def installSingleLevelZip(addonUrl, installPath):
    try:
        r = requests.get(addonUrl, stream=True)
        z = zipfile.ZipFile(BytesIO(r.content))
        z.extractall(installPath)
    except Exception as err:
        print('Failed to install ' + addonUrl)
        print(err)

def installZippedGitRepo(addonUrl, installPath):
    try:
        r = requests.get(addonUrl, stream=True)
        z = zipfile.ZipFile(BytesIO(r.content))
        with tempfile.TemporaryDirectory() as tempDirPath:
            z.extractall(tempDirPath)
            directories = list(filter(gitZipFilter, z.infolist()))
            for info in directories:
                parts = splitall(info.filename)
                src = os.path.join(tempDirPath, parts[0], parts[1])
                dst = os.path.join(installPath, parts[1])
                shutil.rmtree(dst, True)
                shutil.copytree(src, dst)
            shutil.rmtree(os.path.join(tempDirPath, z.infolist()[0].filename), True)

    except Exception as err:
        print('Failed to install ' + addonUrl)
        print(err)

# This function returns true if the ZipInfo objects references a directory
# and that directory is one level below the root of the archive and it
# does not begin with '.'
def gitZipFilter(zipInfo):
    if zipInfo.is_dir() == False:
        return False
    parts = splitall(zipInfo.filename)
    if len(parts) != 3:
        return False
    if parts[1].startswith('.'):
        return False
    return True

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

# Curse

def curse(addonpage):
    try:
        page = requests.get(addonpage + '/download')
        contentString = str(page.content)
        indexOfZiploc = contentString.find('download__link') + 22  # Will be the index of the first char of the url
        endQuote = contentString.find('"', indexOfZiploc)  # Will be the index of the ending quote after the url
        return 'https://www.curseforge.com' + contentString[indexOfZiploc:endQuote]
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        return ''

def convertOldCurseURL(addonpage):
    try:
        # Curse has renamed some addons, removing the numbers from the URL. Rather than guess at what the new
        # name and URL is, just try to load the old URL and see where Curse redirects us to. We can guess at
        # the new URL, but they should know their own renaming scheme better than we do.
        page = requests.get(addonpage)
        return page.url
    except Exception:
        print('Failed to find the current page for old URL "' + addonpage + '". Skipping...\n')
        return ''

def getCurseVersion(addonpage):
    try:
        page = requests.get(addonpage + '/files')
        contentString = str(page.content)
        indexOfVer = contentString.find('file__name full') + 17  # first char of the version string
        endTag = contentString.find('</span>', indexOfVer)  # ending tag after the version string
        return contentString[indexOfVer:endTag].strip()
    except Exception:
        print('Failed to find version number for: ' + addonpage)
        return ''

# Curse Project

def curseProject(addonpage):
    try:
        return addonpage + '/files/latest'
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        return ''


def getCurseProjectVersion(addonpage):
    try:
        page = requests.get(addonpage + '/files')
        contentString = str(page.content)
        indexOfVer = contentString.find('data-name') + 11  # first char of the version string
        endTag = contentString.find('">', indexOfVer)  # ending tag after the version string
        return contentString[indexOfVer:endTag].strip()
    except Exception:
        print('Failed to find version number for: ' + addonpage)
        return ''


# Tukui

def tukui(addonpage):
    try:
        return addonpage + '/repository/development/archive.zip'
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        return ''


def getTukuiVersion(addonpage):
    try:
        response = requests.get(addonpage)
        content = str(response.content)
        match = re.search('<a\sclass="commit-sha\s[^>]*>(?P<hash>[^<]*)<\/a>', content)
        result = ''
        if match:
            result = match.group('hash')
        return result
    except Exception as err:
        print('Failed to find version number for: ' + addonpage)
        print(err)
        return ''

# Wowinterface

def wowinterface(addonpage):
    downloadpage = addonpage.replace('info', 'download')
    try:
        page = requests.get(downloadpage + '/download')
        contentString = str(page.content)
        indexOfZiploc = contentString.find('Problems with the download? <a href="') + 37  # first char of the url
        endQuote = contentString.find('"', indexOfZiploc)  # ending quote after the url
        return contentString[indexOfZiploc:endQuote]
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        return ''


def getWowinterfaceVersion(addonpage):
    try:
        page = requests.get(addonpage)
        contentString = str(page.content)
        indexOfVer = contentString.find('id="version"') + 22  # first char of the version string
        endTag = contentString.find('</div>', indexOfVer)  # ending tag after the version string
        return contentString[indexOfVer:endTag].strip()
    except Exception:
        print('Failed to find version number for: ' + addonpage)
        return ''
