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


def makeList(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    a = soup.find_all("div", class_="f4 text-normal", attrs='url')
    b= str(a)

    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', b)
    #print(soup.find_all("div", class_="f4 text-normal"))
    # print(re.search("(?P<url>https?://[^\s]+)", b).group("url"))
    # print(urls[3])
    x = 0
    while x < 19:
        for urls[x] in urls:
        #if urls[x] not in urllist:
            urllist.append(urls[x])
        x = x +2
    print(urllist)

def makeBetterList(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    counter = 0
    thislist = []
    while counter < 10:
        try:
            print("asd")
            print(counter)
            a = soup.find_all("div", class_="f4 text-normal", attrs='url')[counter]
            b= str(a)
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', b)
            counter += 1
            urllist.append(urls[0])
        except:
            counter +=1
            pass



makeBetterList(url2)
print(urllist)

def buildList(pageNumber, maxNumber):
    y = pageNumber
    while y < maxNumber:
        urled = 'https://github.com/search?p='+str(y)+'&q=bpmn&type=Repositories'
        #print(urled)
        makeBetterList(urled)
        y = y +1
    with open('license.txt', 'a') as file:
        for line in urllist:
            file.write(line + "\n")
    #with open ('license.txt', 'rb') as fp:
        #itemlist = pickle.load(fp)
        #print(itemlist)

buildList(12, 21)