import urllib2

from pyquery import PyQuery as pq
from lxml import etree

def download_file(url):
	f = urllib2.urlopen(url)
	data = f.read()
	with open(str(index) + ".pdf", "wb") as code:
		code.write(data)

links = []
names = []

d = pq(url='https://research.google.com/pubs/QuantumAI.html')

# # get of journal titles
# for name in d('.pub-title'):
# 	names.append(name.text_content().replace('  ', '').replace('\n', ''))

# get all the pdf links
count = 0
for item in d('.pdf-icon'):
	if not item.attrib['href'].endswith("pdf"):
		continue
	if not item.attrib['href'].startswith("http"):
		links.append('https://static.googleusercontent.com/media/research.google.com/en/' + item.attrib['href'])
	else:
		links.append(item.attrib['href'])

	count += 1

with open('links.data', mode='w') as f:
	for link in links:
		f.write(link + '\n')

index = 1
with open('links.data') as f:
	for line in f:
		try:
			url = line.rstrip()
			download_file(url)
			print 'completed file ' + str(index)
			index += 1
		except Exception, e:
			print 'cannot get file at ' + str(index) + ': ' + str(e)


print 'finished :)'
