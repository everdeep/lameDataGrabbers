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

import os
from pyquery import PyQuery as pq
from lxml import etree

# Stores the links retrieved from the page
links = []

# Grab url from user
urls = [
	#'https://fleetlists.busaustralia.com/index-act.php',
	#'https://fleetlists.busaustralia.com/index-nsw.php',
	'https://fleetlists.busaustralia.com/index-nt.php',
	'https://fleetlists.busaustralia.com/index-qld.php',
	'https://fleetlists.busaustralia.com/index-sa.php',
	'https://fleetlists.busaustralia.com/index-tas.php',
	'https://fleetlists.busaustralia.com/index-vic.php',
	'https://fleetlists.busaustralia.com/index-nat.php',
	'https://fleetlists.busaustralia.com/index-nz.php'
]

default_url = 'https://fleetlists.busaustralia.com/'
#file_names = ['act', 'nsw', 'nt', 'qld', 'sa', 'tas', 'vic', 'national', 'nz']
file_names = ['nt', 'qld', 'sa', 'tas', 'vic', 'national', 'nz']
file_count = 0
for url in urls:
	print(url)
	d = pq(url)

	count = 1
	with open('error_links.txt', 'w+') as errors:
		with open('bus_data (%s).cv' % file_names[file_count], 'w+') as f:
			# Grabs all the links with the data about busses
			for a in d('#resultform tr td a'):
				link = default_url + str(a.attrib['href'])
				try:
					d = pq(link)
				except Exception as e:
					#print('# Error with:\n"%s"\nReason: %r' % (link.replace('\n', ''), e))
					continue
				
				temp = d('body tr')
				desired_row = temp[-1]
				title = d('#content h1')[0].text
				written_to_file = get_data(file_names[file_count], title, desired_row)
				if not written_to_file:
					print(link, file=errors)
				count += 1

	os.system('python3 error_link_data.py %s' % file_names[file_count])
	links = []
	file_count += 1
	