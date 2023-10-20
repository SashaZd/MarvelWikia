from lxml import html

import requests
import json


initialList = open("marvel_shortlistURLs.txt")
tempListing = open("marvel_kb1.txt", "a")
charDict = {}


for char in initialList: 
	url = char.split(",")[0]
	name = ""
	alias = ""

	if url.split("/")[-1]=="featured":
		name = url.split("/")[-2]
	else:
		name = url.split("/")[-1]
	
	if "_" in name:
		name_temp = name.split("_")
		name = ""
		for eachName in name_temp:
			name += eachName + " "

		name.strip()
		
		if "(" in name:
			alias = name.split("(")[1][:-2]


	charSetUrl = url.strip()
	page = requests.get(charSetUrl)
	tree = html.fromstring(page.text)

	infoTable_forImage = tree.xpath("//img[@class='character-image']")
	infoTable_forWiki = tree.xpath("//a[@class='featured-item-notice primary']")


	character_image = ""
	urlToWiki = ""

	if infoTable_forImage: 
		character_image = infoTable_forImage[0].values()[1]
	
	if infoTable_forWiki:
		urlToWiki = infoTable_forWiki[0].values()[0]+"\n"

	charDict[name]={
		"more_info": url,
		"name": name,
		"character_image": character_image,
		"alias": [alias],
		"urlToWiki": urlToWiki
	}

	tempListing.write(json.dumps(charDict[name]))








