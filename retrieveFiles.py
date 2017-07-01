#============================================================
#	Install the relevant libraries:
#
#	Run this in the command-line:
#	pip3 install bs4, requests
#
#	Run program in python3
#
#============================================================

import os
import requests
from bs4 import BeautifulSoup

# NOTE: Change this url to the site with the math links
URL = 'http://www.maths.usyd.edu.au/u/UG/IM/MATH2961/resources.html'

# This is just for creating a login session. No need to change
LOGINURL = """
			https://wasm.usyd.edu.au/login.cgi?appID=maths&destURL=http%3A%2
			F%2Fwww.maths.usyd.edu.au%2Fs%2Flogin%3Furl64%3DL3UvVUcvSU0vTUFU
			SDI5NjIvci9wZGYvbG9jL2V4YW0yMDEzLnBkZg%3D%3D
		   """

#==================================================
#	Creating the payload for the session
# 	You need to enter your unikey and pass
#==================================================
payload = {
	# the names of the user, pass and login button
	# NOTE: must change these to your details
	'credential_0': '<username>',
	'credential_1': '<password>',
	'Submit': 'Sign in'
}

req_headers = {
	'Content-Type': 'application/x-www-form-urlencoded',
}

# Create a session object
session = requests.Session()

# Send POST request for authentication
r = session.post(LOGINURL, data=payload, headers=req_headers, allow_redirects=True)

# Retrieve session of URL
r = session.get(URL)
data = r.text

# Parse the data
soup = BeautifulSoup(data, 'html.parser')

# interate through the links on the page
for link in soup.find_all('a'):
	string = link.get('href')
	if string is not None:
		if (string[-4:] == '.pdf'):
			name = ''
			try:
				# NOTE: Modify this url to this format.
				new_url = 'http://www.maths.usyd.edu.au/u/UG/IM/MATH2961/' + string
				r = session.get(new_url)

				#=========================
				# Checking for redirection
				#=========================
				# if r.history:
				# 	print('Request was redirected')
				# 	for resp in r.history:
				# 		print(resp.status_code, resp.url)
				# 	print('Final destination:')
				# 	print(r.status_code, r.url)
				# else:
				# 	print('Request was not redirected')

				string = string.lower()
				name = string.split('/')[-1]
				folder = ''

				# You can modify the strings according to how the
				# files are named so that they will be placed in
				# the folders you want them to be placed in
				if 'exam' in string:
					folder = 'Exams'
				elif 'lect' in string:
					folder = 'Lectures'
				elif 'quiz' in string:
					folder = 'Quizzes'
				elif 'week' in string:
					folder = 'Tutorials'
				elif 'prac' in string or 'exercise' in string:
					folder = 'Practice'
				elif 'ass' in string:
					folder = 'Assignments'
				else:
					folder = 'Extra'

				#=========================
				# Testing
				#=========================
				print(folder, '--', name)
				# print(r.content)
				# break

				#=========================
				# Writing files to the folders
				# Do this once you are satisfied
				# that all files will go to their
				# relevant folders.
				#=========================
				# directory = folder + '/'
				# if not os.path.exists(directory):
				# 	os.makedirs(directory)
				# with open(directory + name, "wb") as code:
				# 	code.write(r.content)
				# print('completed file ', name)
			except Exception as e:
				print('Cannot get the file (' + name + '):', str(e))
