import requests
import re
from bs4 import BeautifulSoup

def parse(page):
     soup = BeautifulSoup(page, 'html.parser')
     
     return soup;



req = requests.get("https://www.stackoverflow.com/") # amazon,apple,facebook, youtube, 

page = req.text

soup = parse(page)

Bodycontent = soup.find("body")

#print(content)

for div in Bodycontent.find_all("div"):

    #print(div) 

    for privacy in div.find_all("a",text="Privacy"):
        print(privacy.get('href'))    