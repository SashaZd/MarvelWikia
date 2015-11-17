from lxml import html

import requests
import json, re

BASE_URL_FOR_WIKIA = 'http://marvel.wikia.com'
FILE_FOR_CHARACTER_LINKS = "CharacterURLs.txt"


def findInterestingChars():
	charsFromMarvel = open('MarvelCharacters.txt', 'r')
	charsFromWikia = open('allChars.json', 'r')

	charsFromMarvelMissing = open('MarvelCharacters.txt', 'a')
	charsFromMarvelWithAlias = open('MarvelCharacters_Aliases.json', 'w')

	wikiaChars = json.load(charsFromWikia)
	newWikiaChars = {}
	marvelChars = charsFromMarvel.readlines()

	for eachChar in wikiaChars: 
		if "Aliases" in wikiaChars[eachChar]:
			aliases = re.split(',|;', wikiaChars[eachChar]["Aliases"][0].encode("utf-8"))
			for eachAlias in aliases: 
				newWikiaChars[eachAlias.strip()] = eachChar

	# wikiaChars.update(newWikiaChars)
	print len(newWikiaChars)

	charsFromMarvelWithAlias.write(json.dumps(newWikiaChars, sort_keys=True,indent=4,))



	# print wikiaChars["Iron Man"]["Aliases"]

	# for eachChar in wikiaChars:
	# 	if "Iron Man" in eachChar: 
	# 		print wikiaChars[eachChar]

	# counter = 0

	# charsFromMarvelMissing.write("-------------- Append ---------------\n")

	# for eachChar in marvelChars: 
	# 	charName = eachChar.strip()
	# 	if charName in wikiaChars:
	# 		counter += 1

	# 	# Check in aliases
	# 	else:
	# 		for eachChar in wikiaChars: 
	# 			if "Aliases" in wikiaChars[eachChar]:
	# 				if charName in str(wikiaChars[eachChar]["Aliases"]):
	# 					counter += 1


	# 	else:
	# 		charsFromMarvelMissing.write(charName+"\n")

	# print counter


findInterestingChars()