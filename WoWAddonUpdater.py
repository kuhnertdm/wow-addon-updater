import requests, zipfile, configparser
from io import *
from os.path import isfile

print('')

def confirmExit():
	input('\nPress the Enter key to exit')
	exit(0)

# Read config file

if(not isfile('config.ini')):
	print('Failed to read configuration file. Are you sure there is a file called "config.ini" with the "WowAddonUpdater.py" file?')
	confirmExit()

config = configparser.ConfigParser()
config.read('config.ini')

try:
	WOW_ADDON_LOCATION = config['WOW ADDON UPDATER']['WoW Addon Location']
	ADDON_LIST_FILE = config['WOW ADDON UPDATER']['Addon List File']
except Exception:
	print('Failed to parse configuration file. Are you sure it is formatted correctly?')
	confirmExit()

if(not isfile(ADDON_LIST_FILE)):
	print('Failed to read addon list file. Are you sure the file exists?')
	confirmExit()

def getAddon(ziploc):
	r = requests.get(ziploc, stream=True)
	z = zipfile.ZipFile(BytesIO(r.content))
	z.extractall(WOW_ADDON_LOCATION)

def findZiploc(addonpage):
	page = requests.get(addonpage + '/download')
	contentString = str(page.content)
	indexOfZiploc = contentString.find('data-href') + 11 # Will be the index of the first char of the url
	endQuote = contentString.find('"', indexOfZiploc) # Will be the index of the ending quote after the url
	return contentString[indexOfZiploc:endQuote]

# Main process (yes I formatted the project badly)

with open(ADDON_LIST_FILE, "r") as fin:
	for line in fin:
		ziploc = findZiploc(line.rstrip('\n'))
		getAddon(ziploc)