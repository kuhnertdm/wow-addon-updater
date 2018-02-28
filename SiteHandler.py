import packages.requests as requests


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
    elif addonpage.startswith('http://git.tukui.org/'):
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
    elif addonpage.startswith('http://git.tukui.org/'):
        return getTukuiVersion(addonpage)

    # Wowinterface
    elif addonpage.startswith('http://www.wowinterface.com/'):
        return getWowinterfaceVersion(addonpage)

    # Invalid page
    else:
        print('Invalid addon page.')


# Curse

def curse(addonpage):
    if '/datastore' in addonpage:
        return curseDatastore(addonpage)
    try:
        page = requests.get(addonpage + '/download')
        contentString = str(page.content)
        indexOfZiploc = contentString.find('download__link') + 22  # Will be the index of the first char of the url
        endQuote = contentString.find('"', indexOfZiploc)  # Will be the index of the ending quote after the url
        return 'https://www.curseforge.com' + contentString[indexOfZiploc:endQuote]
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        return ''

def curseDatastore(addonpage):
    try:
        # First, look for the URL of the project file page
        page = requests.get(addonpage)
        contentString = str(page.content)
        endOfProjectPageURL = contentString.find('">Visit Project Page')
        indexOfProjectPageURL = contentString.rfind('<a href="', 0, endOfProjectPageURL) + 9
        projectPage = contentString[indexOfProjectPageURL:endOfProjectPageURL] + '/files'

        # Then get the project page and get the URL of the first (most recent) file
        page = requests.get(projectPage)
        projectPage = page.url  # We might get redirected, need to know where we ended up.
        contentString = str(page.content)
        indexOfZiploc = contentString.find('<a class="button tip fa-icon-download icon-only" href="/') + 55
        endOfZiploc = contentString.find('"', indexOfZiploc)

        # Add on the first part of the project page URL to get a complete URL
        endOfProjectPageDomain = projectPage.find("/", 8)
        projectPageDomain = projectPage[0:endOfProjectPageDomain]
        return projectPageDomain + contentString[indexOfZiploc:endOfZiploc]
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
    if '/datastore' in addonpage:
        # For some reason, the dev for the DataStore addons stopped doing releases back around the
        # start of WoD and now just does alpha releases on the project page. So installing the
        # latest 'release' version gets you a version from 2014 that doesn't work properly. So
        # we'll grab the latest alpha from the project page instead.
        return getCurseDatastoreVersion(addonpage)
    try:
        page = requests.get(addonpage + '/files')
        contentString = str(page.content)
        indexOfVer = contentString.find('file__name full') + 17  # first char of the version string
        endTag = contentString.find('</span>', indexOfVer)  # ending tag after the version string
        return contentString[indexOfVer:endTag].strip()
    except Exception:
        print('Failed to find version number for: ' + addonpage)
        return ''

def getCurseDatastoreVersion(addonpage):
    try:
        # First, look for the URL of the project file page
        page = requests.get(addonpage)
        contentString = str(page.content)
        endOfProjectPageURL = contentString.find('">Visit Project Page')
        indexOfProjectPageURL = contentString.rfind('<a href="', 0, endOfProjectPageURL) + 9
        projectPage = contentString[indexOfProjectPageURL:endOfProjectPageURL] + '/files'

        # Then get the project page and get the version of the first (most recent) file
        page = requests.get(projectPage)
        contentString = str(page.content)
        indexOfVer = contentString.find('data-name="') + 11
        endOfVer = contentString.find('"', indexOfVer)
        return contentString[indexOfVer:endOfVer].strip()
    except Exception:
        print('Failed to find alpha version number for: ' + addonpage)


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
    print('Tukui is not supported yet.')
    return ''


def getTukuiVersion(addonpage):
    # print('Tukui is not supported yet.')
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
