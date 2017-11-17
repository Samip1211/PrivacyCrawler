import requests
import re
from bs4 import BeautifulSoup
import sqlite3
import sys
import fnmatch
import urllib.request
import reader
import json

# UserAgent,


# sets up parser using beautifulsoup
def parse(page):
    soup = BeautifulSoup(page, 'html.parser')

    return soup;



##This function will take in the domain and a term, it will then try to find that term anywhere on the page using Mercury API wrapper

def confirm_Page(domain, term):


    body = reader.reader(domain, "OJ6jo9V0rAu5OITm4SbhzWHrJcKyzDtaB8s4INic", 720)

    d = json.loads(str(body))
    if(term in str((d['content']))):
        return True

    else:
        return False




## Finds the <body> of a html file
def get_Body_Content(domain):
    req = requests.get(domain)  # amazon,apple,facebook, youtube,

    page = req.text

    soup = parse(page)

    Bodycontent = soup.find("body")

    return Bodycontent


## Grabs the robots text file from the webserver. We will use this to detect whether or
## not website administrator will allow our bot to crawl their page by checking if / is disallowed


def read_robot_file(domain):
    req = urllib.request.urlopen(domain + "/robots.txt")  #requests the robots file

    code = req.code                                       #checks to see if the file exists. If it doesn't exist, return true
    if (code / 100 >= 4):
        return True

    fileContent = req.read().splitlines()
    x = 0
    for line in fileContent:                            #goes through the robots file on by one looking for our useragent
        x += 1
        l = line.find(b'User-agent: tos-scrapper')
        if (l >= 0):
            print(fileContent[x])
            if (fileContent[x] in 'Disallowed: /'):     #if it shows we are disallowed, return False
                return False
    return True


## This function takes in the html of the body, and keyword we are searching for that is contained in a hyperlink. It returns the
## url that is attached to the hyperlink text

def findToS(Bodycontent, keyword):
    termsURL = ""
    for div in Bodycontent.find_all("div"):
        for terms in div.find_all("a", text=re.compile(keyword)):
            termsURL = terms.get('href').encode('ascii', 'ignore')
            return termsURL

    if not termsURL:
        return False


##inserts the website tos/privacy and domain if the information is found.
def insertDB(domain, privacy, terms):
    conn = sqlite3.connect('tos_scraper.db')

    try:
        conn.execute("INSERT INTO website(tos, privacy, url) VALUES (?, ?, ?)", [terms, privacy, domain])

        conn.commit()
    except sqlite3.Error as er:
        print('er:' + er.message)
    conn.close()


## goes through a keyword list stored in file variable and then calls the findToS function with each keyword. Trying to find
## the keyword on the page inside a hyperlink text.
def checkKeyWords(url, file):
    myfile = open(file, "r").read().split('\n')

    body = get_Body_Content(url)

    if len(myfile) != 0:
        for line in myfile:
            # print(line)
            policy_url = findToS(body, line)
            if (policy_url != False):
                return policy_url

    return False



def main():
    domain = "https://stackoverflow.com"

    if(read_robot_file("https://stackoverflow.com")):



        content = get_Body_Content(domain)

        # print(content)


        terms = checkKeyWords(domain, "terms.txt")          #look for terms and conditions
        privacy = checkKeyWords(domain, "privacy.txt")      #look for privacy policy


        if terms is None:
            print("Could not find the terms of service")

        if privacy is None:
            print("Could not find Privacy Policy")

        print(terms)
        print(privacy)


        if(confirm_Page(terms, "Terms of Service")):
            print("Terms of Service confirmed")
        else:
            print("Terms of service url might be a false positive")

        if(confirm_Page(privacy, "Privacy Policy")):
            print("Privacy Policy Confirmed")
        else:
            print("Privac Policy url might be a false positive")


    else:

        print("The website is not allowing us to scrape their main page")


    insertDB(domain, privacy, terms)              #after we find the privacy and terms, we can insert it into database


main()
