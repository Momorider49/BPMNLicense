import requests
from bs4 import BeautifulSoup
import config
import main

headers = {'User-Agent': config.UserAgent}

#Hier wird die Lizenz Datei auf die Keywords überprüft; Nutzbare Dateien werden in license.txt gespeichert
def checkLicense(s, url):
    if s.find('MIT License') != -1 or s.find('Apache') != -1 or s.find('ISC License') != -1 or s.find('BSD 3-Clause License') or s.find('ISC License') != -1 or s.find('BSD Zero Clause') != -1 or s.find('Artistic License') != -1 or s.find('BSD 2-Clause') != -1 or s.find('BSD License') != -1 or s.find('BSD 3-Clause') != -1 or s.find('BSD 4-Clause') != -1 or s.find('Boost Software License') != -1 or s.find('CCO 1.0 Universal') != -1 or s.find('Attribution 4.0') != -1 or s.find('Educational Community License') != -1 or s.find('MIT No Attribution') != -1 or s.find('Microsoft Public License') != -1 or s.find('Mulan PSL v2') != -1 or s.find('NCSA Open Soruce License') != -1 or s.find('SIL OPEN FONT LICENSE') != -1 or s.find('PostgreSQL License') != -1 or s.find('free and unencumbered software') != -1 or s.find('Universal Permissive License') != -1 or s.find('DO WHAT THE FUCK YOU WANT') != -1 or s.find('BSD Zero Clause License') != -1 or s.find('zlib License') != -1:
        print('License found')
        with open('license.txt', 'a') as file:
            file.write(url + "\n")

#Lizenz Dateien haben typischer weise eine spezifische Url Endung am Ende des Projekt Namens, diese wird hier hinzugefügt 
#falls eine Datei gefunden wird sucht die Main methode weiter nach dem Inhalt
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
    return 0

#die foundfiles.txt Datei wird gelöscht, damit die Dateien nicht nochmal überprüft werden
def removeoldlist():
    lines_seen = set()
    outfile = open('foundfiles.txt', "w")
    for line in open('foundfiles.txt', "r"):
        if line not in lines_seen:
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()

#doppelte Elemente werden aus der foundfiles.txt Datei entfernt    
def removeduplicate():
    lines_seen = set()
    for line in open('foundfiles.txt', "r"):
        if line not in lines_seen:
            #outfile.write(line)
            lines_seen.add(line)
    outfile = open('foundfiles.txt', "w")
    for lined in lines_seen:
        outfile.write(lined)
    outfile.close()

#führt die einzelnen Elemente der Klasse aus
if __name__ == '__main__':
    lines = []
    removeduplicate()
    #jedes Element der Datei wird in eine Liste gespeichert
    with open('foundfiles.txt', 'rt') as file:
        for line in file:
            lines.append(line.strip())
        #die Einzelnen Elemente werden durchsucht
        for element in lines:
                try:
                    #Das Programm baut sich aus der URL der Datei die URL des Repositories zusammen
                    originalurl = (str(element).split('/', -1)[0] + "//" + str(element).split('/')[2] + "/" + str(element).split('/')[3] +"/"+ str(element).split('/')[4])
                    #print(originalurl)
                except:
                    print("-")
                url = addURL(originalurl)
                if url != 0:
                    #Der Text der Lizenz wird über requests extrahiert und dann geprüft
                    r = requests.get(url, headers=headers)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    checkLicense(str(soup.getText), element)
                lines.remove(element)

    removeoldlist()
