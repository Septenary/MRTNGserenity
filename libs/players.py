import dataclasses
import aenum
import enum
from collections import namedtuple
from typing import Tuple
from xmlrpc.client import Boolean

class GameClass(str, enum.Enum):
    WARRIOR = "WARRIOR"
    PALADIN = "PALADIN"
    HUNTER = "HUNTER"
    ROGUE = "ROGUE"
    PRIEST = "PRIEST"
    DEATHKNIGHT = "DEATHKNIGHT"
    SHAMAN = "SHAMAN"
    MAGE = "MAGE"
    WARLOCK = "WARLOCK"
    MONK = "MONK"
    DRUID = "DRUID"
    DEMONHUNTER = "DEMONHUNTER"


class Spec(str, aenum.MultiValueEnum):
    # Warrior
    PROTECTION = "PROTECTION", "PROTECTION1"
    ARMS = "ARMS"
    FURY = "FURY"
    # DK
    FROST = "FROST"
    UNHOLY = "UNHOLY"
    BLOOD = "BLOOD"
    # Paladin (prot from warrior)
    HOLY = "HOLY"
    RETRIBUTION = "RETRIBUTION"
    # Hunter
    MARKSMANSHIP = "MARKSMANSHIP"
    SURVIVAL = "SURVIVAL"
    BEASTMASTER = "BEASTMASTER"
    # Shaman
    RESTORATION = "RESTORATION"
    ENHANCEMENT = "ENHANCEMENT"
    ELEMENTAL = "ELEMENTAL"
    # Druid (resto from shamana)
    BEAR = "BEAR"
    CAT = "CAT"
    BALANCE = "BALANCE"
    # Rogue
    ASSASSINATION = "ASSASSINATION"
    COMBAT = "COMBAT"
    SUBTLETY = "SUBTLETY"
    # Mage (frost from DK)
    FIRE = "FIRE"
    ARCANE = "ARCANE"
    # Warlock
    DEMONOLOGY = "DEMONOLOGY"
    DESTRUCTION = "DESTRUCTION"
    AFFLICTION = "AFFLICTION"
    # Priest (Holy from Paladin)
    SHADOW = "SHADOW"
    DISCIPLINE = "DISCIPLINE"

@dataclasses.dataclass
class Role:
    gameclass: GameClass
    spec: Spec
    rh_name: str
    is_healer: Boolean = False
    is_tank: Boolean = False
    is_melee_dps: Boolean = False
    is_caster_dps: Boolean = False
    is_hunter_dps: Boolean = False
    is_ranged_dps: Boolean = False
    can_dispel_magic: Boolean = False
    can_dispel_curse: Boolean = False
    can_dispel_poison: Boolean = False
    can_dispel_disease: Boolean = False
    can_purge: Boolean = False
    has_unholy_frenzy: Boolean = False
    has_focus_magic: Boolean = False
    has_misdirect: Boolean = False
    has_power_infusion: Boolean = False
    has_tricks: Boolean = False
    has_innervate: Boolean = False
    has_raidsac: Boolean = False
    
    def __post_init__(self):
        if self.is_caster_dps or self.is_hunter_dps:
            self.is_ranged_dps = True
    

roles = {
    # Warrior
    (Spec.PROTECTION, GameClass.WARRIOR): Role(gameclass=GameClass.WARRIOR, 
                                                    spec=Spec.PROTECTION, 
                                                    is_tank=True,
                                                    rh_name="Protection"),
    (Spec.ARMS, GameClass.WARRIOR): Role(gameclass=GameClass.WARRIOR, 
                                                    spec=Spec.ARMS, 
                                                    is_melee_dps=True,
                                                    rh_name="Arms"),
    (Spec.FURY, GameClass.WARRIOR): Role(gameclass=GameClass.WARRIOR, 
                                                    spec=Spec.FURY, 
                                                    is_melee_dps=True,
                                                    rh_name="Fury"),
    # DeathKnight
    (Spec.BLOOD, GameClass.DEATHKNIGHT): Role(gameclass=GameClass.DEATHKNIGHT, 
                                                    spec=Spec.BLOOD, 
                                                    is_tank=True,
                                                    has_unholy_frenzy=True,
                                                    rh_name="Blood_Tank"),
    (Spec.UNHOLY, GameClass.DEATHKNIGHT): Role(gameclass=GameClass.DEATHKNIGHT, 
                                                    spec=Spec.UNHOLY, 
                                                    is_melee_dps=True,
                                                    rh_name="Unholy_DPS"),
    (Spec.FROST, GameClass.DEATHKNIGHT): Role(gameclass=GameClass.DEATHKNIGHT, 
                                                    spec=Spec.FROST, 
                                                    is_melee_dps=True,
                                                    rh_name="Frost_DPS"),

    # Paladin
    (Spec.HOLY, GameClass.PALADIN): Role(gameclass=GameClass.PALADIN, 
                                                    spec=Spec.HOLY, 
                                                    is_healer=True,
                                                    can_dispel_magic=True,
                                                    can_dispel_disease=True,
                                                    can_dispel_poison=True,
                                                    rh_name="Holy1"),
    (Spec.PROTECTION, GameClass.PALADIN): Role(gameclass=GameClass.PALADIN, 
                                                    spec=Spec.PROTECTION, 
                                                    is_tank=True,
                                                    rh_name="Protection1"),
    (Spec.RETRIBUTION, GameClass.PALADIN): Role(gameclass=GameClass.PALADIN, 
                                                    spec=Spec.RETRIBUTION, 
                                                    is_melee_dps=True,
                                                    can_dispel_magic=True,
                                                    can_dispel_disease=True,
                                                    can_dispel_poison=True,
                                                    rh_name="Retribution"),

    # Shaman
    (Spec.RESTORATION, GameClass.SHAMAN): Role(gameclass=GameClass.SHAMAN, 
                                                    spec=Spec.RESTORATION, 
                                                    is_healer=True,
                                                    can_dispel_disease=True,
                                                    can_dispel_poison=True,
                                                    can_dispel_curse=True,
                                                    rh_name="Restoration1"),
    (Spec.ENHANCEMENT, GameClass.SHAMAN): Role(gameclass=GameClass.SHAMAN, 
                                                    spec=Spec.ENHANCEMENT, 
                                                    is_melee_dps=True,
                                                    rh_name="Enhancement"),
    (Spec.ELEMENTAL, GameClass.SHAMAN): Role(gameclass=GameClass.SHAMAN, 
                                                    spec=Spec.ELEMENTAL, 
                                                    is_caster_dps=True,
                                                    rh_name="Elemental"),

    # Hunter
    (Spec.MARKSMANSHIP, GameClass.HUNTER): Role(gameclass=GameClass.HUNTER, 
                                                    spec=Spec.MARKSMANSHIP, 
                                                    is_hunter_dps=True,
                                                    rh_name="Marksmanship"),
    (Spec.SURVIVAL, GameClass.HUNTER): Role(gameclass=GameClass.HUNTER, 
                                                    spec=Spec.SURVIVAL, 
                                                    is_hunter_dps=True,
                                                    rh_name="Survival"),
    (Spec.BEASTMASTER, GameClass.HUNTER): Role(gameclass=GameClass.HUNTER, 
                                                    spec=Spec.BEASTMASTER, 
                                                    is_hunter_dps=True,
                                                    rh_name="Beastmaster"),

    # Druid
    (Spec.CAT, GameClass.DRUID): Role(gameclass=GameClass.DRUID, 
                                                    spec=Spec.CAT, 
                                                    is_melee_dps=True,
                                                    rh_name="Feral"),
    (Spec.BEAR, GameClass.DRUID): Role(gameclass=GameClass.DRUID, 
                                                    spec=Spec.BEAR, 
                                                    is_tank=True,
                                                    rh_name="Guardian"),
    (Spec.BALANCE, GameClass.DRUID): Role(gameclass=GameClass.DRUID, 
                                                    spec=Spec.BALANCE, 
                                                    is_caster_dps=True,
                                                    rh_name="Balance"),
    (Spec.RESTORATION, GameClass.DRUID): Role(gameclass=GameClass.DRUID, 
                                                    spec=Spec.RESTORATION, 
                                                    is_healer=True,
                                                    can_dispel_curse=True,
                                                    can_dispel_poison=True,
                                                    rh_name="Restoration"),

     # Rogue
    (Spec.ASSASSINATION, GameClass.ROGUE): Role(gameclass=GameClass.ROGUE, 
                                                    spec=Spec.ASSASSINATION, 
                                                    is_melee_dps=True,
                                                    has_tricks=True,
                                                    rh_name="Assassination"),
    (Spec.COMBAT, GameClass.ROGUE): Role(gameclass=GameClass.ROGUE, 
                                                    spec=Spec.COMBAT, 
                                                    is_melee_dps=True,
                                                    has_tricks=True,
                                                    rh_name="Combat"),
    (Spec.SUBTLETY, GameClass.ROGUE): Role(gameclass=GameClass.ROGUE, 
                                                    spec=Spec.SUBTLETY, 
                                                    is_melee_dps=True,
                                                    has_tricks=True,
                                                    rh_name="Subtlety"),
    
    # Mage
    (Spec.FROST, GameClass.MAGE): Role(gameclass=GameClass.MAGE, 
                                                    spec=Spec.FROST, 
                                                    is_caster_dps=True,
                                                    can_dispel_curse=True,
                                                    rh_name="Frost"),
    (Spec.FIRE, GameClass.MAGE): Role(gameclass=GameClass.MAGE, 
                                                    spec=Spec.FIRE, 
                                                    is_caster_dps=True,
                                                    can_dispel_curse=True,
                                                    rh_name="Fire"),
    (Spec.ARCANE, GameClass.MAGE): Role(gameclass=GameClass.MAGE, 
                                                    spec=Spec.ARCANE, 
                                                    is_caster_dps=True,
                                                    can_dispel_curse=True,
                                                    has_focus_magic=True,
                                                    rh_name="Arcane"),
                                                
    # Warlock
    (Spec.DEMONOLOGY, GameClass.WARLOCK): Role(gameclass=GameClass.WARLOCK, 
                                                    spec=Spec.DEMONOLOGY, 
                                                    is_caster_dps=True,
                                                    rh_name="Demonology"),
    (Spec.AFFLICTION, GameClass.WARLOCK): Role(gameclass=GameClass.WARLOCK, 
                                                    spec=Spec.AFFLICTION, 
                                                    is_caster_dps=True,
                                                    rh_name="Affliction"),
    (Spec.DESTRUCTION, GameClass.WARLOCK): Role(gameclass=GameClass.WARLOCK, 
                                                    spec=Spec.DESTRUCTION, 
                                                    is_caster_dps=True,
                                                    rh_name="Destruction"),
    
    # Priest
    (Spec.HOLY, GameClass.PRIEST): Role(gameclass=GameClass.PRIEST, 
                                                    spec=Spec.HOLY, 
                                                    is_healer=True,
                                                    can_dispel_magic=True,
                                                    can_dispel_disease=True,
                                                    rh_name="Holy"),
    (Spec.DISCIPLINE, GameClass.PRIEST): Role(gameclass=GameClass.PRIEST, 
                                                    spec=Spec.DISCIPLINE,
                                                    can_dispel_magic=True,
                                                    can_dispel_disease=True, 
                                                    is_healer=True,
                                                    rh_name="Discipline"),
    (Spec.SHADOW, GameClass.PRIEST): Role(gameclass=GameClass.PRIEST, 
                                                    spec=Spec.SHADOW,
                                                    can_dispel_magic=True,
                                                    can_dispel_disease=True, 
                                                    is_caster_dps=True,
                                                    rh_name="Shadow")
}


# raidhelper_spec_to_class_spec = {
#     # Warrior
#     "Protection": (Spec.PROTECTION, GameClass.WARRIOR),
#     "Arms": (Spec.ARMS, GameClass.WARRIOR),
#     "Fury": (Spec.FURY, GameClass.WARRIOR),
#     # Paladin
#     "Protection1": (Spec.PROTECTION, GameClass.PALADIN),
#     "Holy1": (Spec.HOLY, GameClass.PALADIN),
#     "Retribution": (Spec.RETRIBUTION, GameClass.PALADIN),
#     # DK
#     "Blood": (Spec.BLOOD, GameClass.DEATHKNIGHT),
#     "Unholy_DPS": (Spec.UNHOLY, GameClass.DEATHKNIGHT),
#     "Frost1": (Spec.FROST, GameClass.DEATHKNIGHT),

#     # Hunter
#     "Marksmanship": (Spec.MARKSMANSHIP, GameClass.HUNTER),
#     "Survival": (Spec.SURVIVAL, GameClass.HUNTER),
#     "Beastmaster": (Spec.BEASTMASTER, GameClass.HUNTER),
#     # Shaman
#     "Restoration1": (Spec.RESTORATION, GameClass.SHAMAN),
#     "Enhancement": (Spec.ENHANCEMENT, GameClass.SHAMAN),
#     "Elemental": (Spec.ELEMENTAL, GameClass.SHAMAN),

#     # Rogue
#     "Assassination": (Spec.ASSASSINATION, GameClass.ROGUE),
#     "Combat": (Spec.COMBAT, GameClass.ROGUE),
#     "Subtlety": (Spec.SUBTLETY, GameClass.ROGUE),
#     # Druid
#     "Feral": (Spec.CAT, GameClass.DRUID),
#     "Bear": (Spec.BEAR, GameClass.DRUID),
#     "Restoration": (Spec.RESTORATION, GameClass.DRUID),
#     "Balance": (Spec.BALANCE, GameClass.DRUID),

#     # Priest
#     "Holy": (Spec.HOLY, GameClass.PRIEST),
#     "Discipline": (Spec.DISCIPLINE, GameClass.PRIEST),
#     "Shadow": (Spec.SHADOW, GameClass.PRIEST),
#     # Mage
#     "Fire": (Spec.FIRE, GameClass.MAGE),
#     "Frost": (Spec.FROST, GameClass.MAGE),
#     "Arcane": (Spec.ARCANE, GameClass.MAGE),
#     # Warlock
#     "Demonology": (Spec.DEMONOLOGY, GameClass.WARLOCK),
#     "Afflication": (Spec.AFFLICTION, GameClass.WARLOCK),
#     "Destruction": (Spec.DESTRUCTION, GameClass.WARLOCK)
# }

class_colors = {
    GameClass.DEATHKNIGHT: "c41e3a",
    GameClass.DRUID: "ff7c0a",
    GameClass.HUNTER: "aad372",
    GameClass.MAGE: "3fc7eb",
    GameClass.PALADIN: "f48cba",
    GameClass.PRIEST: "ffffff",
    GameClass.ROGUE: "fff468",
    GameClass.SHAMAN: "0070dd",
    GameClass.WARLOCK: "8788ee",
    GameClass.WARRIOR: "c69b6d"
}

class Player:
    def __init__(self, name: str, spec: Spec = None, gameclass: GameClass = None, rh_string: str = None):
        self.name = name
        match name:
            case "Crowdcontrol/Safeword/Thornball":
                self.name = "Crowdcontrol"
            case "Scard/Jatia/Darge/UtesDad":
                self.name = "Scard"
            case "Backstab/Pink":
                self.name = "Backstab"
            case "meroe":
                self.name = "Meroe"
            case "halint":
                self.name = "Halint"
            case "rizz":
                self.name = "Rizz"
            case "AppleCandy":
                self.name = "Applecandy"
            case "DrPew":
                self.name = "Drpew"
            case "JeanClaudius":
                self.name = "Jeanclaudius"
            case "NorthFreeze":
                self.name = "Northfreeze"
            case "Foot":
                self.name = "Footlover"

        # Construction with a name and a class
        if isinstance(gameclass, GameClass) and isinstance(spec, Spec):
            self.spec = spec
            self.gameclass = gameclass

        # Construction with a string for the spec (from raid-helper)
        elif rh_string:
            for role in roles.values():
                if role.rh_name == rh_string:
                    self.spec = role.spec
                    self.gameclass = role.gameclass

    def color_name(self):
        # print(self.name)
        return f"|cff{class_colors[self.gameclass]}{self.name}|r" 

    @property
    def role(self):
        return roles[self.spec, self.gameclass]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    # def __repr__(self):
    #     return f"Player(name={self.name}, spec={self.spec}, gameclass={self.gameclass})"
            