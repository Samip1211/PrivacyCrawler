import requests
import re
from bs4 import BeautifulSoup
import sqlite3
import sys


def parse(page):
     soup = BeautifulSoup(page, 'html.parser')
     
     return soup;



def findPrivacy(domain):
	

	req = requests.get(domain) # amazon,apple,facebook, youtube, 

	page = req.text

	soup = parse(page)

	Bodycontent = soup.find("body")

	#print(Bodycontent)


	for div in Bodycontent.find_all("div"):

	    #print(div) 
	        for privacy in div.find_all("a",text="Privacy Policy"):
	                privacyURL = privacy.get('href').encode('ascii','ignore')
	                if(privacyURL.find(domain)):
	                        return privacyURL
def findToS(domain):

	req = requests.get(domain) # amazon,apple,facebook, youtube, 

	page = req.text

	soup = parse(page)

	Bodycontent = soup.find("body")

	#print(Bodycontent)


	for div in Bodycontent.find_all("div"):

	    #print(div) 
	        for terms in div.find_all("a",text="Legal"):
	                termsURL = terms.get('href').encode('ascii','ignore')
	                if(termsURL.find(domain)):
	                        return termsURL

def insertDB(domain, privacy, terms):

	conn = sqlite3.connect('/var/www/html/tos_scraper/tos_scraper.db')

	try:
		conn.execute("INSERT INTO website(tos, privacy, url) VALUES (?, ?, ?)", [terms, privacy, domain])

		conn.commit()
	except sqlite3.Error as er:
		print 'er:', er.message
	conn.close()


def main():

	domain = sys.argv[1]
	print(domain)
	privacy = findPrivacy(domain)

	terms = findToS(domain)

	print(terms)
	print(privacy)

	insertDB(domain, privacy, terms)


main()


