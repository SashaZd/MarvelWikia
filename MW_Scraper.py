from lxml import html
import requests
import json


# The Request

page = requests.get('http://marvel.wikia.com/wiki/Thor_(Thor_Odinson)')
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
	