import requests
import re
from bs4 import BeautifulSoup
import sqlite3
import sys


def parse(page):
     soup = BeautifulSoup(page, 'html.parser')
     
     return soup;

def search_condition(Bodycontent):
    
    for div in Bodycontent.find_all("div"):
        
        for terms in div.find_all("a",text=re.compile("Condition")):
            termsURL = terms.get('href').encode('ascii','ignore')
        
            print(termsURL)
            return termsURL

def get_Body_Content(domain):
    req = requests.get(domain) # amazon,apple,facebook, youtube, 

    page = req.text

    soup = parse(page)

    Bodycontent = soup.find("body")
    
    return Bodycontent

def findPrivacy(Bodycontent,domain):
	
    #print(Bodycontent)
    for div in Bodycontent.find_all("div"):

        for privacy in div.find_all("a",text=re.compile("Privacy")):

            privacyURL = privacy.get('href').encode('ascii','ignore')
            
            #print(privacyURL)
            
            if(str(privacyURL).find(domain)):
                return privacyURL

def findToS(Bodycontent,domain):

#print(Bodycontent)
    for div in Bodycontent.find_all("div"):
        
        for terms in div.find_all("a",text=re.compile("Legal")):
            termsURL = terms.get('href').encode('ascii','ignore')
            print(termsURL)
            if(str(termsURL).find(domain)):
                return termsURL

def insertDB(domain, privacy, terms):

	conn = sqlite3.connect('/var/www/html/tos_scraper/tos_scraper.db')

	try:
		conn.execute("INSERT INTO website(tos, privacy, url) VALUES (?, ?, ?)", [terms, privacy, domain])

		conn.commit()
	except sqlite3.Error as er:
		print ('er:' + er.message)
	conn.close()


def main():

    domain = sys.argv[1]
	
    content = get_Body_Content(domain)
    
    #print(content)
    
    privacy = findPrivacy(content,domain)

    terms = findToS(content,domain)
    
    if terms is None:
        terms = search_condition(content)

    print(terms)
    print(privacy)

	#insertDB(domain, privacy, terms)


main()


