from lxml import html
import requests
import json


# The Request


# page = requests.get('http://marvel.wikia.com/api.php?format=json&page=Thor_(Thor_Odinson)&action=parse');

page = requests.get('http://marvel.wikia.com/wiki/Thor_(Thor_Odinson)')
tree = html.fromstring(page.text)

infoTable = tree.xpath("//table[@class='infobox-table']/tr")
print len(infoTable)

for i in range(0,29):
	value = tree.xpath("//table[@class='infobox-table']/tr[{i}]/td".format(i=i))
	print "---------------"
	for j in value:
		print j.text_content().strip()