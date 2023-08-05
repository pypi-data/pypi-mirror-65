
from XivDbReader import Settings
#from XivDbReader.modules.soup import *
#from XivDbReader.modules.request import *
from typing import Tuple, List
import requests
from bs4 import BeautifulSoup, Tag

class ParseList():
    def __init__(self, url: str):
        self.__settings__: Settings = Settings()
        self.url = url

    def GetHtmlSource(self, href: str) -> str:
        if href == '':
            raise Exception("href needs to be filled to process")

        self.href = href
        return requests.get(href)

    def FindLinks(self, page: str = '*') -> List:
        links = []
        html: str = requests.get(self.url)
        soup: BeautifulSoup = BeautifulSoup(html.text, 'html.parser')
        table = soup.find_all('table', class_='db-table')
        for i in table[0].contents[3].contents:
            href: str = ''
            if i == '\n':
                continue

            try:
                href = i.contents[1].contents[5].contents[3].attrs['href']
                links.append(self.__settings__.links.rootUrl + href)
                continue
            except:
                pass

            # Older items have a different structure to check for
            try:
                href = i.contents[1].contents[1].contents[1].contents[3].attrs['href']
                links.append(self.__settings__.links.rootUrl + href)
                continue
            except:
                pass        

            try:
                href = i.contents[1].contents[1].contents[1].contents[5].attrs['href']
                links.append(self.__settings__.links.rootUrl + href)
            except:
                pass
        return links

    def __parseMajorPatchItems__(self, row: Tag) -> Tuple:
        """
        About: This will parse the row of data that has the flag for 'latest_patch__major_icon'

        Params:
            row = Contains the data extracted by BeautifulSoup
        """
        try:
            # Get to the extact cell that contains the name and link to the full items info
            # This extracts the items that are marked as new adds from SE
            name: str = row.text
            link: str = row.attrs['href']
            itemLink: Tuple = (name, self.linkRoot + link)
            #self.links.append(itemLink)
            print(f"Found {name} - {self.linkRoot + link}")
            return itemLink
        except:
            print('Error: Failed to parse for MajorPatchItem.')

    def __parseOlderItems__(self, row: Tag) -> Tuple:
        """
        About: Extract items that have been in the game already from older patches
        """
        try:
            name: str = row.text
            link: str = row.attrs['href']
            itemLink = (name, self.linkRoot + link)
            #self.links.append(itemLink)
            print(f"Found {name} - {self.linkRoot + link}")
            return itemLink
        except:
            print("Error: Failed to parse old Item")