


class Settings():
    def __init__(self):
        self.sleepTimer: int = 5

        self.links = Links()



class Links():
    def __init__(self):
        self.rootUrl = "https://na.finalfantasyxiv.com"
        self.dbUrl = f"{self.rootUrl}/lodestone/playguide/db"
        
        self.armsAllUrl = f"{self.dbUrl}/item/?category2=1"
        self.armsUrl = f"{self.dbUrl}/item/?category2=1&category3="
        self.armsMnk = f"{self.armsUrl}1"
        self.armsPld = f"{self.armsUrl}2"
        self.armsWar = f"{self.armsUrl}3"
        
        self.toolsAllUrl = f"{self.dbUrl}/item/?category2=2"

        self.armorAllUrl = f"{self.dbUrl}/item/?category2=3"
        self.accessoriesAllUrl = f"{self.dbUrl}/item/?category2=4"
        self.medsAllUrl = f"{self.dbUrl}/item/?category2=5&category3=44"
        self.foodAllUrl = f"{self.dbUrl}/item/?category2=5&category3=46"
        self.materialsAllUrl = f"{self.dbUrl}/item/?category2=6"
