
from typing import List

class Item():
    def __init__(self):
        self.url: str
        self.pictureUrl: str
        self.name: str
        self.rarity: str
        self.untradable: bool = False
        self.unique: bool = False

        self.itemLevel: int = 0
        self.physicalDamage: int = 0
        self.autoAttack: float = 0.0
        self.delay: float = 0.0

        self.sellPrice: str = ''
        self.buyPrice: str = ''
        self.buyFrom: List = ()
        self.marketProhibited: bool = False

class Equipment(Item):
    def __init__(self):
        self.slot: str = "main"
        self.itemLevel: int = 0
        self.jobs: List = []
        self.level: int = 0

        self.strength: int = 0        
        self.vitality: int = 0
        self.dexterity: int = 0
        self.intelligence: int = 0
        self.mind: int = 0

        self.determination: int = 0
        self.skillSpeed: int = 0
        self.spellSpeed: int = 0
        self.criticalHit: int = 0
        self.directHitRate: int = 0
        self.tenacity: int = 0
        
        self.companyCrest: bool = False
        self.armorie: bool = False
        self.glamourChest: bool = False
        
        self.dyeable: bool
        self.extractable: bool = False
        self.projectable: bool = False
        self.desynth: float = 0.0

        self.repairClass: str = ''
        self.repairClassLevel: int = 0
        self.repairMaterial: str = ''

        self.materiaSlots: int = 0
        self.materiaMelderClass: str = ''
        self.materiaMelderLevel: int = 0
        self.advancedMelding: bool = True

        self.relatedDuties: List = []
        self.requiredItems: List = []
        pass

class Weapon(Equipment):
    def __init__(self):
        self.physicalDamage: int = 0
        self.magicDamage: int = 0
        self.autoAttack: float = 0.0
        self.delay: float = 0.0
        
class Armor(Item):
    def __init__(self):
        self.defense: int = 0
        self.magicDefense: int = 0

class Tool():
    pass


