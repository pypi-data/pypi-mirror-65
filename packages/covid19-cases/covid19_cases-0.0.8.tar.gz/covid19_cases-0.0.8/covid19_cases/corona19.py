import urllib.request
from bs4 import BeautifulSoup as bf
import time

def confirmed_people(state):
	time.sleep(5)
	#url = 'https://www.google.com/search?q=python'
	url='https://www.worldometers.info/coronavirus/country/'+state+'/'
	# now, with the below headers, we defined ourselves as a simpleton who is
	# still using internet explorer.
	headers = {}
	headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
	req = urllib.request.Request(url, headers = headers)
	resp = urllib.request.urlopen(req)
	respData = resp.read()
	soup = bf(respData,'html.parser')
	tag = soup("span")
	confirmed_people = tag[4].contents[0]
	return(confirmed_people)
def deaths_people(state):
	time.sleep(5)
	#url = 'https://www.google.com/search?q=python'
	url='https://www.worldometers.info/coronavirus/country/'+state+'/'
	# now, with the below headers, we defined ourselves as a simpleton who is
	# still using internet explorer.
	headers = {}
	headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
	req = urllib.request.Request(url, headers = headers)
	resp = urllib.request.urlopen(req)
	respData = resp.read()
	soup = bf(respData,'html.parser')
	tag = soup("span")
	death_people = tag[5].contents[0]
	return(death_people)
def recoverd_people(state):
	time.sleep(5)
	#url = 'https://www.google.com/search?q=python'
	url='https://www.worldometers.info/coronavirus/country/'+state+'/'
	# now, with the below headers, we defined ourselves as a simpleton who is
	# still using internet explorer.
	headers = {}
	headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
	req = urllib.request.Request(url, headers = headers)
	resp = urllib.request.urlopen(req)
	respData = resp.read()
	soup = bf(respData,'html.parser')
	tag = soup("span")
	recovers_people = tag[6].contents[0]
	return(recovers_people)