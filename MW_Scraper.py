from lxml import html

import requests
import json

BASE_URL_FOR_WIKIA = 'http://marvel.wikia.com'


def getNextPageOfCharacterLinks(url):
	"get the link of the next page of characters to go to"

	nextPage = "";
	page = requests.get('http://marvel.wikia.com/wiki/Category:Characters?display=exhibition&sort=alphabetical')
	tree = html.fromstring(page.text)
	infoTable = tree.xpath("//div[@id='mw-pages']/a")

	for eachLink in infoTable:
		if(eachLink.text_content() == "next 200"):
			nextPage = infoTable[0].values()[0];
			break	

	return

def getCharacterNamesFromURL(url):
	"build a list of all the characters with their Wiki names to encode into URLs"

	charList = []
	page = requests.get('http://marvel.wikia.com/wiki/Category:Characters?sort=alphabetical')
	tree = html.fromstring(page.text)
	infoTable = tree.xpath("//div[@class='mw-content-ltr']/table/tr")

	# text returned as a giant string, splitlines gives us each character indpendantly for the page.
	charList = infoTable[1].text_content().strip().splitlines()
	return charList


def getTableDataGivenUrl(url):
	"Create dictionary of character data attributes from the Wiki Character table"

	page = requests.get(url)
	tree = html.fromstring(page.text)

	infoTable = tree.xpath("//table[@class='infobox-table']/tr")

	charDict = {};

	print len(infoTable)

	for i in range(0,29):
		value = tree.xpath("//table[@class='infobox-table']/tr[{i}]/td".format(i=i))
		# print "---------------"
		valueList = []
		for j in range(1,len(value)):
			valueList.append(value[j].text_content().encode('utf-8').strip())

		try: 
			charDict[value[0].text_content().encode('utf-8').strip()] = valueList
		except: 
			pass

	print charDict.keys()
	return charDict





