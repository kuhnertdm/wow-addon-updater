import requests, zipfile
from io import *

WOW_ADDON_LOCATION = "C:/Users/dkuhnert/Desktop/test"
ADDON_LIST_LOCATION = "C:/Users/dkuhnert/Desktop/in.txt"

def getAddon(ziploc):
	r = requests.get(ziploc, stream=True)
	z = zipfile.ZipFile(BytesIO(r.content))
	z.extractall(WOW_ADDON_LOCATION)

def findZiploc(addonpage):
	page = requests.get(addonpage + "/download")
	contentString = str(page.content)
	indexOfZiploc = contentString.find("data-href") + 11 # Will be the index of the first char of the url
	endQuote = contentString.find('"', indexOfZiploc) # Will be the index of the ending quote after the url
	return contentString[indexOfZiploc:endQuote]

with open(ADDON_LIST_LOCATION, "r") as fin:
	for line in fin:
		ziploc = findZiploc(line.rstrip('\n'))
		getAddon(ziploc)