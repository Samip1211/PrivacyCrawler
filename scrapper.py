import requests
import re
from bs4 import BeautifulSoup
import sqlite3
import sys
#UserAgent,

def parse(page):
     soup = BeautifulSoup(page, 'html.parser')
     
     return soup;

def search_condition(Bodycontent,domain):
    
    for div in Bodycontent.find_all("div"):
        
        for terms in div.find_all("a",text=re.compile("Condition")):
            termsURL = terms.get('href').encode('ascii','ignore')
            if(str(termsURL).find(domain)):
            #print(termsURL)
                return termsURL
            else:
                return str(domain)+str(termsURL)    

def get_Body_Content(domain):
    req = requests.get(domain) # amazon,apple,facebook, youtube, 

    page = req.text

    soup = parse(page)

    Bodycontent = soup.find("body")
    
    return Bodycontent

def get_robots_file(domain):
    req = requests.get(domain+"/robots.txt")
    page = req.text
    f = open("robots.txt","w")
    f.write(page)
    f.close()
    
    return page      

def findPrivacy(Bodycontent,domain):
	
    #print(Bodycontent)
    for div in Bodycontent.find_all("div"):

        for privacy in div.find_all("a",text=re.compile("Privacy")):

            privacyURL = str(privacy.get('href').encode('ascii','ignore'))
            
            print(privacyURL.find(domain))
            
            if(privacyURL.find(domain) is -1):
                return privacyURL.replace(" ' ","").replace("b","")
                    
def findToS(Bodycontent,domain):
    #print(Bodycontent)
    for div in Bodycontent.find_all("div"):
        
        for terms in div.find_all("a",text=re.compile("Legal")):
            termsURL = terms.get('href').encode('ascii','ignore')
            #print(termsURL)
            if(str(termsURL).find(domain) is not -1):
                return termsURL
            else:
                return str(domain)+str(termsURL)     

def insertDB(domain, privacy, terms):

	conn = sqlite3.connect('/var/www/html/tos_scraper/tos_scraper.db')

	try:
		conn.execute("INSERT INTO website(tos, privacy, url) VALUES (?, ?, ?)", [terms, privacy, domain])

		conn.commit()
	except sqlite3.Error as er:
		print ('er:' + er.message)
	conn.close()

def read_robot_file():
    f = open("robots.txt","r")
    
    lines = f.readlines()
    
    f.close()
    
    return lines

def get_allow_files(list):
    allow_list =[]
    for content in list:
        allow = content.split(':')
        if allow[0] == "Allow":
            allow_list.append(allow[1])
    return allow_list        

def get_disallow_files(list):
    disallow_list =[]
    for content in list:
        disallow = content.split(':')
        if disallow[0] == "Disallow":
            disallow_list.append(disallow[1]) 
    return disallow_list                              

def main():

    domain = sys.argv[1]
    
    robots = get_robots_file(domain)
    
    lines = read_robot_file()
    list_of_allow_and_disallow=[]
    
    for i in range(0,len(lines)):
        if lines[i]=="User-agent: *\n":
            
            j=i
            
            while True:
                j=j+1
                if lines[j]!="\n":
                    list_of_allow_and_disallow.append(lines[j].replace('\n',""))
                else:
                    break
                    
    allow_list = get_allow_files(list_of_allow_and_disallow) )
    
    disallow_list =get_disallow_files(list_of_allow_and_disallow))          
                
    #print(list)
    
    
    
    content = get_Body_Content(domain)
    
    #print(content)
    
    privacy = findPrivacy(content,domain)

    terms = findToS(content,domain)
    
    if terms is None:
        terms = search_condition(content,domain)

    print(terms)
    
    print(privacy)

	#insertDB(domain, privacy, terms)
       

main()


