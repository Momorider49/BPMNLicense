# This is a sample Python script.
import mmap
import scrapy
import requests
from bs4 import BeautifulSoup

import main

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
mitcount = 0
gnucount = 0
apachecount = 0
isccount = 0

def checkLicense(s):
    if s.find('MIT License') != -1:
        main.mitcount += 1
        print('MIT: ' + str(main.mitcount))
    if s.find('GNU') != -1:
        main.gnucount = main.gnucount + 1
        print('GNU: ' + str(main.gnucount))
    if s.find('Apache') != -1:
        main.apachecount = main.apachecount + 1
        print('Apache: ' + str(main.apachecount))
    if s.find('ISC') != -1:
        main.isccount = main.isccount + 1
        print('ISC: ' + str(main.isccount))



def addURL(url):
    if requests.get(str(url) + '/raw/master/LICENSE', headers=headers):
        url = str(url) + '/raw/master/LICENSE'
    if requests.get(str(url) + '/raw/master/License.md', headers=headers):
        url = str(url) + '/raw/master/License.md'
    return url

if __name__ == '__main__':
    # url = 'https://github.com/fau-is/xnap'
    #url = 'https://github.com/ViktorStefanko/BPMN_Crawler'
    # url = url + '/raw/master/License.md'


    lines = []
    with open('license.txt', 'rt') as file:
        for line in file:
            lines.append(line.strip()) #sehr wichtig
        for element in lines:
                url = addURL(element)
                #print(element)
                #print(url)
                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.text, 'html.parser')
                checkLicense(str(soup.getText))
                # print(soup.prettify())



    # soup.findAll('div', attrs={'class' : 'name'})
    #print(soup.prettify())
    #print(mitcount)
    #print(gnucount)
    #print(apachecount)
    #print(isccount)


        #checkIt(str(soup.getText))

def checkIt(license):
    with open(license, 'rb', 0) as file, \
       mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if s.find(b'MIT License') != -1:
                print('MIT')
                main.mitcount = main.mitcount + 1
            if s.find(b'GNU') != -1:
                print('GNU')
                main.gnucount = main.gnucount +1
            if s.find(b'Apache') != -1:
                print('Apache')
                main.apachecount = main.apachecount +1
            if s.find(b'ISC') != -1:
                print('ISC')
                main.isccount = main.isccount +1