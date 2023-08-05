
from XivDbReader.collections import Item, Weapon, Armor
from XivDbReader.exceptions import UnableToFindValue

from typing import Dict, List
from bs4 import BeautifulSoup, Tag, ResultSet
import re
import requests

class ParseItems():
    def __init__(self):
        pass

    def GetHtmlSource(self, href: str) -> str:
        self.href = href
        return requests.get(href)

    def getDetails(self, href:str = '', html: str = '') -> Item:
        if html == '':
            if href == '':
                raise Exception("Submit a valid url to getWeaponDetails(href='www....)")
            html: str = requests.get(href)

        self.item = Item()

        soup: BeautifulSoup = BeautifulSoup(html.text, 'html.parser')

        itemText = soup.find_all('div', class_='db-view__item__text')
        innerText = itemText[0].contents[1]

        unique: bool = False
        untradable: bool = False
        name: str = ''
        rarity: str = ''

        try:
            innerText = soup.find_all('div', class_='db-view__item__text__inner')
            for i in innerText[0].contents:
                if i == '\n':
                    continue

                if len(i.contents) == 5:
                    for rareType in i.contents:
                        if rareType == '\n':
                            continue

                        if rareType.text == 'Unique':
                            unique = True
                            continue
                        
                        if rareType.text == 'Untradable':
                            untradable = True
                            continue

                if len(i.contents) == 7:
                    for g in i.contents:
                        if g == '\n':
                            continue

                        alt = g.contents[0].attrs['alt']
                        if "company crests" in alt:
                            if "Cannot" in alt: 
                                companyCrest = False
                            else: 
                                companyCrest = True
                        
                        if "dresser" in alt:
                            if "Cannot" in alt: 
                                glamourChest = False
                            else: 
                                glamourChest = True
                        
                        if "armoire" in alt: 
                            if "Cannot" in alt: 
                                armorie = False
                            else: 
                                armorie = True

                # Gets the name of the time
                if i.name == 'h2':
                    name = i.text
                    name = name.replace('\n', '')
                    name = name.replace('\t', '')
                    name = name.replace('\ue03c', '')
                    name = name

                    rarity = i.attrs['class'][1]
                    if "uncommon" in rarity:
                        rarity = "Uncommon"
                    elif "common" in rarity:
                        rarity = "Common"
                    elif "rare" in rarity:
                        rarity = "Rare"
                    elif "epic" in rarity:
                        rarity = "Epic"
                    continue

                # Gets what slot the item goes to
                if i.attrs['class'][0] == 'db-view__item__text__category':
                    slot = i.text
        except Exception as e:
            pass

        if slot == "Shield" or slot == "Head" or slot == "Body" or slot == 'Hands' or slot == "Waist" or slot == "Legs" or slot == "Feet":
            self.item = Armor()
        elif "Arm" in slot:
            self.item = Weapon()

        self.item.name = name
        self.item.rarity = rarity
        self.item.unique = unique
        self.item.untradable = untradable
        self.item.url = href
        self.item.companyCrest = companyCrest
        self.item.glamourChest = glamourChest
        self.item.armorie = armorie

        itemLevel: str = soup.find_all('div', class_='db-view__item_level')[0].text
        self.item.itemLevel: int = int(itemLevel.replace('Item Level ', ''))

        try:
            pictureUrl = soup.find_all('div', class_='db-view__item__icon latest_patch__major__detail__item')
            try:
                for p in pictureUrl[0].contents:
                    if p == '\n':
                        continue

                    elif p.attrs['class'][0] == 'db-view__item__icon__cover':
                        continue

                    elif p.attrs['width'] == '152':
                        continue

                    elif p.attrs['width'] == '128':
                        self.item.pictureUrl = p.attrs['src']
                        self.item.pictureWidth = int(p.attrs['width'])
                        self.item.pictureHeight = int(p.attrs['height'])
                    else:
                        print("new values found in pictureUrl")
            except Exception as e:
                print("Error parsing pictureUrl", e)

            #self.item.pictureUrl = pictureUrl[0].contents[5].attrs['src']
            #picutreHeight: int = pictureUrl[0].contents[3].attrs['height']
            #pictureWidth: int = pictureUrl[0].contents[3].attrs['width']
        except Exception as e:
            raise UnableToFindValue("msg: Unable to find a 'div' with class 'db-view__item__icon latest_patch__major__detail__item'")

        try:
            #specValue = soup.find_all('div', class_='db-view__item_spec__value')
            specValue = soup.find_all('div', class_='clearfix sys_nq_element')

            # Armor values
            if ("Shield" in slot 
                or "Head" in slot 
                or "Body" in slot 
                or "Hands" in slot
                or "Legs" in slot
                or "Feet" in slot):

                if len(i.contents) == 5:
                    self.item.defense = i.contents[1].text
                    self.item.magicDefense = i.contents[3].text

            # Weapon Values
            elif ("Arm" in slot or "Grimorie" in slot):
                # Healer Weapons
                if ("Conjurer" in slot 
                    or "Scholar" in slot 
                    or "Astrologian" in slot
                    or "Thaumaturge" in slot 
                    or "Arcanist" in slot 
                    or "Red" in slot 
                    or "Blue" in slot):
                    self.item.magicDamage = int(specValue[0].contents[1].text)
                else:
                    # general dps
                    self.item.physicalDamage = int(specValue[0].contents[1].text)

                self.item.autoAttack = float(specValue[0].contents[3].text)
                self.item.delay = float(specValue[0].contents[5].text)

        except Exception as e:
            pass

        try:
            bonusAttr = soup.find_all('div', class_='sys_nq_element')

            # Bonus Stats
            self.__getBonusAttr__(bonusAttr)

            self.item.requiredItems = []
            if "Required Items" in bonusAttr[2].contents[0].text:
                requiredItemsList: List = []

                for ri in bonusAttr[2].contents:
                    if ri.text == "Required Items":
                        continue

                    if ri.contents[0].attrs['class'][0] == 'db-shop__item':
                        requiredItemsDict: Dict = {'item': '', 'itemAmount': 0 , 'npc': '', 'location': ''}
                        # Item amount is always the last value in the array
                        
                        itemName = ri.contents[0].contents[1].text
                        requiredItemsDict['item'] = itemName

                        rx = re.findall(r'\d', requiredItemsDict['item'])
                        itemAmount: int = rx[len(rx) - 1]
                        requiredItemsDict['itemAmount'] = itemAmount

                        requiredItemsDict['item'] = itemName.replace(itemAmount, '')

                        requiredItemsDict['npc'] = ri.contents[1].text
                        requiredItemsDict['location'] = ri.contents[2].text
                        requiredItemsList.append(requiredItemsDict)

                self.item.requiredItems = requiredItemsList

        except:
            print("Unable to find 'div class='sys_nq_element'.  Could be expected result based on the item.")
            #raise UnableToFindValue("Unable to find 'div class='sys_nq_element'")

        try:
            htmlJobs = soup.find_all('div', {'class': "db-view__item_equipment__class"})
            jobsSplit = htmlJobs[0].contents[0].split(' ')
            self.item.jobs = []
            for j in jobsSplit:
                self.item.jobs.append(j)
        except Exception as e:
            print(e)

        try:
            htmlJobLevel = soup.find_all('div', {'class': 'db-view__item_equipment__level'})
            if "Lv." in htmlJobLevel[0].text:
                level = htmlJobLevel[0].text.replace("Lv. ", '')
                self.item.level = int(level)
            else:
                self.item.level = 0
        except Exception as e:
            print("Failed to find what level is required for the item.", e)

        try:
            #materia_ = soup.find_all('div', class_='db-popup__inner')
            materia_ = soup.find_all("ul", {'class': 'db-view__materia_socket'})
            self.item.materiaSlots = 0
            self.item.materiaMelderClass = ''
            self.item.materiaMelderLevel = 0
            if materia_ != []:
                self.__parseMateriaValues__(materia_)
            else:
                self.item.materiaSlots = 0
                self.item.materiaMelder = None
                print(f"{self.item.name} seems to not accept materia.")
        except:
            print(f'Unable to find expected HTML for materia')

        try:
            repair = soup.find_all('ul', class_='db-view__item_repair')
            for r in repair[0].contents:
                if r == '\n':
                    continue

                if r.contents[0].text == "Repair Level":
                    _repair = r.contents[0].next_sibling.text.split(" Lv. ")                    
                    self.item.repairClass = _repair[0]
                    self.item.repairClassLevel = int(_repair[1])
                    continue
                
                if r.contents[0].text == "Materials":
                    repairMaterial == r.contents[1].previous_sibling.next_sibling.text
                    continue

                if r.contents[0].text == "Materia Melding":
                    pass

            if "Lv." in repair[0].contents[1].contents[1].text:
                repairBy = repair[0].contents[1].contents[1].contents[0].split(" Lv. ")
                self.item.repairClass: str = repairBy[0]
                self.item.repairClassLevel: int = int(repairBy[1])
                self.item.repairMaterial: str = repair[0].contents[1].next_sibling.contents[1].contents[0]
        except:
            print(f"Unable to find expected HTML for repair values")

        try:
            itemInfo2 = soup.find_all('ul', class_='db-view__item-info__list')
            self.item.extractable = self.__getItemExtractable__(itemInfo2)
            self.item.projectable = self.__getItemProjectable__(itemInfo2)
            self.item.dyeable = self.__getItemDyeable__(itemInfo2)
            self.item.desynth = self.__getItemDesynthesizable__(itemInfo2)
        except:
            print("Item was missing 'db-view__item-info__list' class")


        try:
            footer = soup.find_all('div', class_='db-view__item_footer')
            self.item.buyPrice = 0
            self.item.sellPrice = 0
            self.item.marketProhibited = False
            self.item.advancedMelding = True
            # Check for Advanced Melding
            for i in footer[0].contents:
                if i.text == 'Advanced Melding Forbidden':
                    self.item.advancedMelding = False
                    continue

                elif 'Available for Purchase:' in i.text:
                    
                    continue
                
                elif "Sale Price:" in i.text:
                    textSplit = i.text.split("Sale Price: ")
                    gilSplit = textSplit[1].split(' gil')
                    self.item.buyPrice = gilSplit[0]
                    continue

                elif 'Sells for' in i.text:
                    split = i.text.split("Sells for")
                    if len(split) >= 2:
                        for g in split:
                            if 'gil' in g:
                                gil = g
                                continue

                    else:
                        gil = split

                    gil = gil.replace(" gil", '')
                    gil = gil.replace(',', '')
                    gil = gil.replace(' ', '')

                    self.item.sellPrice = int(gil)
                    continue

                elif i.text == 'Market Prohibited':
                    self.item.marketProhibited = True
                    continue
                
                else:
                    print("Found new value in footer to review.")

            pass
        except Exception as e:
            pass

        try:
            vendors = soup.find_all('div', class_='db-shop__npc__space')
            self.item.buyFrom: List = []
            if vendors != []:
                vendorRows = vendors[0].contents[0].contents[1].contents
                vendorsList: List = []
                for v in vendorRows:
                    vendorsDict: Dict = {'name': '', 'loc': ''}

                    name = v.contents[0].contents[0].text
                    loc = v.contents[1].text
                    if name != '' and loc != '':
                        vendorsDict['name'] = name
                        vendorsDict['loc'] = loc
                        vendorsList.append(vendorsDict)

                self.item.buyFrom = vendorsList
        except:
            print(f"Item did not contain venders")

        # Check if the item contains extra info
        try:
            htmlBase = soup.find_all('div', class_='db__l_main db__l_main__base')
            self.item.relatedDuties = []            
            if htmlBase != []:

                for a in htmlBase:
                    if a == '\n':
                        continue

                    if "Related Duties" in a.contents[1].text:
                        dutiesList: List = []
                        try:
                            duty: Dict = {'name': '', 'requiredLevel': 0, 'averageItemLevel': 0}
                            duties = a.contents[3].contents[1].contents[3]
                            duty['name'] = duties.contents[1].contents[1].contents[3].contents[0]
                            duty['requiredLevel'] = duties.contents[1].contents[3].text
                            duty['averageItemLevel'] = duties.contents[1].contents[5].string
                            dutiesList.append(duty)

                            self.item.relatedDuties = dutiesList

                        except Exception as e:
                            print("Failed to parse 'Related Duties'", e)
                pass

        except Exception as e:
            pass

        return self.item

    def __getBonusAttr__(self, htmlResult: Tag ):
        try:
            for b in htmlResult[1].contents[5].contents:
                if b == '\n':
                    pass
                elif b.contents[0].text == "Strength":
                    self.item.strength = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Vitality":
                    self.item.vitality = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Mind":
                    self.item.mind = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Intelligence":
                    self.item.intelligence = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Determination":
                    self.item.determination = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Skill Speed":
                    self.item.skillSpeed = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Spell Speed":
                    self.item.spellSpeed = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Dexterity":
                    self.item.dexterity = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == 'Critical Hit':
                    self.item.criticalHit = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Direct Hit Rate":
                    self.item.directHitRate = self.__cleanBonusAttr__(b.contents[1])
                elif b.contents[0].text == "Tenacity":
                    self.item.tenacity = self.__cleanBonusAttr__(b.contents[1])
        except Exception as e:
            raise UnableToFindValue("Failed to find BonusAttr, something is missing that is expected.",e)

    def __cleanBonusAttr__(self, value: str) -> int:
        value = value.replace('+', '').replace(' ','')
        return int(value)

    def __parseMateriaValues__(self, materiaCode: ResultSet):
        mslots: int = 0
        try:
            for m in materiaCode[0].contents:
                if m == '\n':
                    pass
                elif m.attrs['class'][1] == 'normal':
                    try:
                        mslots = mslots + 1
                    except:
                        mslots = 1

            self.item.materiaSlots = mslots
        except Exception as e:
            raise UnableToFindValue("HTML contained code for MateriaSlots but failed to parse.", e)

    def __getItemExtractable__(self, itemInfo2: ResultSet) -> bool:
        try:
            extractable: bool = False
            html = itemInfo2[0].contents[1]
            key = html.contents[0]
            value = html.contents[1].contents[0]
            if key == 'Extractable: ':
                if value == 'Yes':
                    extractable == True
                
            return extractable
        except:
            UnableToFindValue(
                "Unable to find 'Extractable: ' in the expected location."
                ,f"key: {key}"
                ,f"value: {value}"
            )
            pass

    def __getItemProjectable__(self, itemInfo2: ResultSet) -> bool:
        try:
            projectable: bool = False
            html = itemInfo2[0].contents[1].next_sibling
            if html.contents[0] == 'Projectable: ':
                if html.contents[1].contents[0] == 'Yes':
                    projectable = True

            return projectable
        except:
            raise UnableToFindValue(
                "Unable to find 'Projectable: ' in the expected location."
                ,f"key: {html.contents[0]}"
                ,f"value: {html.contents[1].contents[0]}"
            )

    def __getItemDesynthesizable__(self, itemInfo2: ResultSet) -> float:
        try:
            desynth: float = 0.0
            html = itemInfo2[0].contents[1].next_sibling.next_sibling
            key = html.contents[0]
            value = html.contents[1].contents[0]
            if key == 'Desynthesizable: ':
                if value == 'No':
                    return desynth
                else:
                    desynth = float(value)
            return desynth
        except:
            raise UnableToFindValue()

    def __getItemDyeable__(self, itemInfo2: ResultSet) -> bool:
        try:
            dyeable: bool = False
            html = itemInfo2[0].contents[1].next_sibling.next_sibling.next_sibling
            key = html.contents[0]
            value = html.contents[1].contents[0]
            if key == "Dyeable: ":
                if value == "Yes":
                    dyeable: bool = True
            return dyeable
        except Exception as e:
            raise UnableToFindValue(
            "Unable to find 'Dyeable: ' in the expected location."
            ,f"key: {key}"
            ,f"value: {value}"
            ,f'raw: {e}')
