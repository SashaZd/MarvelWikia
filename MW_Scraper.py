from lxml import html

import requests
import json

BASE_URL_FOR_WIKIA = 'http://marvel.wikia.com'
FILE_FOR_CHARACTER_LINKS = "CharacterURLs.txt"


'''
	Completed : Methods to get every set of character page links from the Marvel Wikia
'''

def getAllCharacterLinks():
	"Writing each pageinated link from the Marvel Wikia of Characters to a new line in the file assigned to FILE_FOR_CHARACTER_LINKS"

	url = "http://marvel.wikia.com/wiki/Category:Characters?display=exhibition&sort=alphabetical&pageuntil=Abraham+Erskine+%28Earth-9047%29#mw-pages";
	
	'''
		COMMENTED FOR FUTURE USE 
		Until refresh of data needed. If refresh is needed, check next commented section below.
	'''
	# fileForCharacterURLs = open('CharacterURLs.txt', 'w')

	while url != "Finis":
		urlTemp = getNextPageOfCharacterLinks(url)
		if urlTemp != "Finis":
			url = BASE_URL_FOR_WIKIA + urlTemp
			
			'''
				COMMENTED FOR FUTURE USE
				Stored all the URLs to the File on Oct 7th.
				Need to uncomment the next 2 file write lines only if the data needs to be refreshed. 
			'''
			# fileForCharacterURLs.write(url);
			# fileForCharacterURLs.write("\n");


		else:
			url = "Finis";

def getNextPageOfCharacterLinks(url):
	"get the link of the next page of characters to go to"

	nextPage = "";
	page = requests.get(url)
	tree = html.fromstring(page.text)
	infoTable = tree.xpath("//div[@id='mw-pages']/a")

	for eachLink in infoTable:
		if(eachLink.text_content() == "next 200"):
			nextPage = eachLink.values()[0]
			return nextPage	

	if nextPage == "":
		return "Finis"


'''
	sample URL to be supplied to this method: http://marvel.wikia.com/wiki/Category:Characters?display=exhibition&sort=alphabetical&pagefrom=Ahadi+%28Earth-9590%29#mw-pages
'''

def getIndividualCharacterPagesFromURL():
	"build a URL list of all the characters with their Wiki Pages to encode into URLs"

	fileForCharacterSets = open('CharacterSets.txt', 'r')
	fileForCharacterUrls = open('CharacterUrls.txt', 'w')

	for characterSets in fileForCharacterSets:
		charSetUrl = characterSets.strip()
		page = requests.get(charSetUrl)
		tree = html.fromstring(page.text)
		infoTable = tree.xpath("//div[@class='mw-content-ltr']/table/tr/td/ul/li/a")

		flag = False;
		for each in infoTable:
			if flag:
				charUrl = BASE_URL_FOR_WIKIA+each.values()[0]+"\n"
				fileForCharacterUrls.write(charUrl)
			elif each.values()[0] == "/wiki/Category:Secret_Wars_participants":
				flag = True;


'''
	In Progress: Methods to get character data from character
'''

def getTableDataGivenUrl(url):
	"Create dictionary of character data attributes from the Wiki Character table"

	page = requests.get(url)
	tree = html.fromstring(page.text)

	infoTable = tree.xpath("//table[@class='infobox-table']/tr")

	charDict = {};
	flagName = False;
	# print len(infoTable)

	for i in range(0,len(infoTable)):
		value = tree.xpath("//table[@class='infobox-table']/tr[{i}]/td".format(i=i))
		# print "---------------"
		valueList = []
		try: 
			keyToAdd = value[0].text_content().encode('utf-8').strip()

			# Check for headers in the table
			for j in range(1,len(value)):
				valueToAdd = value[j].text_content().encode('utf-8').strip()
				valueList.append(valueToAdd)

			# Is this his title?
			if len(valueList) == 0:
				if flagName==False:
					flagName = keyToAdd
			elif "First Appearance" not in keyToAdd:
				charDict[keyToAdd] = valueList

		except: 
			pass

	return flagName, charDict;

allChars = {};

fileForCharacterData = open('CharacterData.json', 'w')
fileForCharacterUrls = open('CharacterUrls.txt', 'r')
fileForCharacterData.write("{ \n");
flagDoneTill = False;

for eachCharLink in fileForCharacterUrls:
	charLink = eachCharLink.strip()

	# Only getting Earth-616 characters first. Will append the dictionaries later. 
	if "Earth-616" in charLink:
		# if flagDoneTill==False: 
		# 	if "http://marvel.wikia.com/wiki/Jane_Melville_(Earth-616)" in charLink:
		# 		flagDoneTill = True;

		# else:
		char, charDict = getTableDataGivenUrl(charLink)
		allChars[char] = charDict
		toWrite = "'" + str(char)+ "' : " + str(allChars[char]) + ",\n"
		fileForCharacterData.write(toWrite)
		print char

allData = open('allChars.json', 'w')
allData.write(json.dumps(allChars))



# print getTableDataGivenUrl("http://marvel.wikia.com/wiki/Abraham_Erskine_(Earth-616)")
# print getTableDataGivenUrl("http://marvel.wikia.com/wiki/Hulk_(Robert_Bruce_Banner)")
