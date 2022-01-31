import mmap
import re
import pickle
import requests
from bs4 import BeautifulSoup
import regex
import main
urllist= []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
url2 = 'https://github.com/search?q=bpmn'
url = 'https://github.com/search?p=3&q=bpmn&type=Repositories'



def makeBetterList(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    counter = 0
    thislist = []
    while counter < 10:
        try:
            #print("asd")
            a = soup.find_all("div", class_="f4 text-normal")[counter]

            b= str(a)
            print(counter)
            print(b)
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', b)
            counter += 1
            urllist.append(urls[0])
        except:
            counter +=1
            pass

def makeList(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    #print(soup.prettify())
    a = soup.find_all("div", class_="f4 text-normal")
    b = str(a)
    print(a)
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', b)
    #urllist.append(urls[0])
    #urllist.append(urls[2])
    #urllist.append(urls[4])
    #urllist.append(urls[6])
    #urllist.append(urls[8])
    #urllist.append(urls[10])
    #urllist.append(urls[12])
    #urllist.append(urls[14])
    #urllist.append(urls[16])
    #urllist.append(urls[18])



#makeBetterList(url2)
#print("List:")
print(urllist)
print(len(urllist))

def buildList():
    y = 1
    while y < 10:
        urled = 'https://github.com/search?p='+str(y)+'&q=bpmn&type=Repositories'
        print(urled)
        makeBetterList(urled)
        #makeList(urled)
        y = y +1

    with open('license.txt', 'wb') as fp:
        pickle.dump(urllist, fp)
    with open ('license.txt', 'rb') as fp:
        itemlist = pickle.load(fp)
        print(itemlist)

buildList()
print(len(urllist))
print(len(urllist))