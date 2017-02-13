# Check if a string is a number
def is_number(s):
	try:
		int(s)
		return True
	except:
		return False

def search_all_rows(section, title, rows):
	for row in rows:
		for elem in row:
			try:
				text = elem.text.lower()
				if 'total bus' in text and 'withdrawn' not in text:
					number = text.split(' ')[-1]
					print("%s - %s: %s" % (section, title, number))
					print('%s,%s' % (title.strip(), number), file=f)
					return True
			except:
				continue
	return False

def get_data(section, title, desired_row):
	for row in desired_row:
			try:
				text = row.text.lower()
				if 'total bus' in text and 'withdrawn' not in text:
					number = text.split(' ')[-1]
					print("%s - %s: %s" % (section, title, number))
					print('%s,%s' % (title.strip(), number), file=f)
					return True
				elif is_number(text):
					print("%s - %s: %s" % (section, title, text))
					print('%s,%s' % (title.strip(), text), file=f)
					return True
			except:
				continue
	# When the desired_row does not contain the right data
	# we then search every row (usually 30-50 rows)
	return search_all_rows(file_names[file_count], title, temp)

import sys
from pyquery import PyQuery as pq
from lxml import etree

links = []
urls = []
default_url = "https://fleetlists.busaustralia.com/"

with open('error_links.txt') as f:
	for line in f:
		links.append(line.strip())

for link in links:
	try:
		d = pq(link)
	except Exception as e:
		print('# Error with:\n"%s"\nReason: %r' % (link, e))
		continue
	
	for a in d('#content p a'):
		if a.text == "Full Fleet Listing":
			urls.append('%s%s' % (default_url, str(a.attrib['href'])))
			break

file = str(sys.argv[1])
with open('bus_data (%s).cv' % file, 'a') as f:
	for url in urls:
		try:
			d = pq(url)
		except Exception as e:
			print('# Error with:\n"%s"\nReason: %r' % (url, e))
			continue
		
		temp = d('body tr')[-1]
		desired_row = temp
		title = d('#content h1')[0].text
		written_to_file = get_data(file, title, desired_row)
		if not written_to_file:
			print("failed with link %s" % url)
