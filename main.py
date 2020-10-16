# coding=utf-8
# This is a sample Python script.
debug = False
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

url = 'http://prod-mapserver-001.traffic.tt3.com/release/tomtom/maps/'
filterDirs = ["Parent Directory", "adhoc/"]
thePast = datetime.strptime('2001-01-01', '%Y-%m-%d')


def findLatestDirForUrl(url):
    latestDate = thePast
    latestDirName = ''

    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table')

    if debug:
        print("Directories found for URL {0}".format(url))

    for row in table.findAll('tr')[0:]:
        col = row.findAll('td')
        if len(col) > 3:
            if col[1].string not in filterDirs and col[3].getText().strip() == '-':
                name = col[1].string
                date = datetime.strptime(col[2].getText().strip(), '%Y-%m-%d %H:%M')

                if debug:
                    type = 'Dir'
                    entry = (type, name, date.__str__())
                    print " | ".join(entry)

                if date > latestDate and name != '':
                    latestDirName = name
                    latestDate = date

                    if debug:
                        print ("Latest dir:" + name)

    if latestDirName != '':
        latestDirName += findLatestDirForUrl(url + latestDirName)

    return latestDirName


def listFilesForUrl(url):
    count = 0
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table')


    varsYmlFile = open("vars.yml", "w")
    varsYmlFile.write("variables:\n")
    for row in table.findAll('tr')[0:]:
        col = row.findAll('td')
        if len(col) > 3:
            if col[3].getText().strip() != '-':
                count += 1
                name = col[1].string
                varsYmlFile.write("  file{0}: \"{1}\"\n".format(count, name))
                print(name)
    varsYmlFile.close()
    print ("Found {0} files".format(count))


if __name__ == '__main__':
    print("\n------------------------------------------------------")
    print("Input URL: {0}".format(url))
    dirName = findLatestDirForUrl(url)
    print("Calculated LATEST DIR PATH: {0}".format(dirName))
    print("Calculated LATEST DIR URL : {0}".format(url + dirName))
    print("------------------------------------------------------\n")
    listFilesForUrl(url + dirName)
