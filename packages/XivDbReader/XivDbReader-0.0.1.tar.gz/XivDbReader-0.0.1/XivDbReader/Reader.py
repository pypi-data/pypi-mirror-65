
from XivDbReader.settings import Settings
from XivDbReader.scrape import ParseList, ParseItems
from XivDbReader.collections import *
from typing import List
from requests import get
from time import sleep

class Reader():
    """
    About:
        This is the primary method of getting information from loadstone DB.
    """

    def __init__(self):
        self.__settings__: Settings = Settings()
        pass

    def getArms(self, job: str, amount: int= 1) -> List:
        """
        About:
            This will make a call into the module and return 

        Params:
            job: Defines what type of items you are looking for.
                ex: 'pld', 'mrd', 'war', 'ast'

            amount: defines the number of records to return
                default: 1.  This returns one record
                Accepts: -1 = all records
                    1 - 999 exact number of records
        """
        
        url: str = ''
        res: List = []

        if job.lower() == "pld" or \
            job.lower() == 'gld':
            url = self.__settings__.links.armsPld
            pass

        pl = ParseList(url)
        res = pl.FindLinks()
        if res.__len__() == 0:
            raise Exception("Failed to parse list of items." f"url: {url}")
        sleep(self.__settings__.sleepTimer)

        # Convert the url to a weapon class
        items: List = []
        for l in res:
            items.append(self.GetSingleItem(l, "arm"))
            if items.__len__() == amount:
                break
            sleep(self.__settings__.sleepTimer)
        
        return items

    def GetSingleItem(self, url: str, type: str):
        if type == "arm":
            pi = ParseItems()
            item: Weapon = Weapon()
            item = pi.getDetails(href=url)
            return item
        pass
