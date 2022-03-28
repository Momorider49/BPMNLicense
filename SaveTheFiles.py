import requests
import os
import codecs
from bs4 import BeautifulSoup
from github import Github
import main
import config

#Der Personal Access Token muss hier in die Klammer als String
g = Github(config.GHAC)
#Und hier als String
Github.AccessToken = config.GHAC
#Hier den eigenen User-Agent einfügen
headers = {'User-Agent': config.UserAgent}

removablelines = []
mains = main
def addURL(url):
    if requests.get(str(url) + '/raw/master/LICENSE', headers=headers):
        url = str(url) + '/raw/master/LICENSE'
        return url
    if requests.get(str(url) + '/raw/master/License.md', headers=headers):
        url = str(url) + '/raw/master/License.md'
        return url
    if requests.get(str(url) + '/blob/develop/LICENSE', headers=headers):
        url = str(url) + '/blob/develop/LICENSE'
        return url
    else:
        return 0


def savelicenses():
    c = True
    while c == True:
        lines = []
        with open('license.txt', 'rt') as file:
            for lin in file:
                removablelines.append(lin.strip())
                line = lin.strip()
                try:
                    ous = str(line).split('/', -1)[0] + "//" + "raw.githubusercontent.com/" + str(line).split('/')[
                        3] + "/" + str(line).split('/')[4]
                    i = 6
                    while i <= len((line.split('/'))):
                        ous += "/"
                        ous += str(line).split('/')[i]
                        i += 1
                except IndexError:
                    ok = 0
                #print(ous[:-1])
                lines.append(ous[:-1])
                c = False
        for line in lines:
            #print(line)
            try:
                originalurl = (str(line).split('/', -1)[0] + "//" + "github.com" + "/" +
                               str(line).split('/')[3] + "/" + str(line).split('/')[4])
                #print(originalurl)
            except:
                print("-")
            #print(originalurl)
            licenseurl = addURL(originalurl)
            #print(licenseurl)
            #print(line.split('/'))
            filename = f"{config.savefolder}/{str(line.split('/')[3])}+{str(line.split('/')[4])}/{str(line.split('/')[-1])}"
            licensename = f"{config.savefolder}/{str(line.split('/')[3])}+{str(line.split('/')[4])}/license.txt"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            os.makedirs(os.path.dirname(licensename), exist_ok=True)
            r = requests.get(line, headers=headers)
            sp = BeautifulSoup(r.text, 'html.parser')
            s = str(sp.get_text(separator= '\n'))
            s.encode('ascii', 'ignore')
            with codecs.open(filename, "w", encoding="utf-8") as f:
                try:
                    f.write(s.strip())
                    print(s.split("\n")[1:])
                except UnicodeEncodeError:
                    f.write('Unknown Characters Found')
                lines.remove(line)
            with codecs.open(licensename, "w", encoding="utf-8") as ln:
                if licenseurl != 0:
                    re = requests.get(licenseurl, headers=headers)
                    soups = BeautifulSoup(re.text, 'html.parser')
                    try:
                        ln.write(soups.getText())
                    except UnicodeEncodeError:
                        ln.write('Unknown Characters Found')
            savedlines = []
            with open('savedlicenses.txt', 'w') as file:
                file.write(line + "\n")
numlines = sum(1 for line in open('license.txt'))
if int(numlines) >= 1:
    savelicenses()
    with open("license.txt", "r") as f:
        lines = f.readlines()
    with open("license.txt", "w") as f:
        for line in lines:
            if line.strip("\n") not in removablelines:
                f.write(line)
else:
    print('Empty License file found')
