# /// YOUR ICON DICTIONARY HERE /// #
ICON_DICT = {}

'''
Normal Icons/Emojis
'''

SPARKLER_EMOJI = '\U0001F387'
SKULL_EMOJI = '\U0001F480'
CHARACTER_EMOJI = '\U0001F9D9'
CROSSED_SWORDS_EMOJI = '\U00002694'
CASTLE_EMOJI = '\U0001F3F0'
MAGE_EMOJI = '\U0001F9D9'
CRYSTAL_BALL_EMOJI = '\U0001F52E'
BED_EMOJI = '\U0001F6CF'
SHOP_EMOJI = '\U0001F6D2'
EXTRACT_ESSENCE_EMOJI = '\U0001F48E'
MAP_EMOJI = '\U0001F4CD'
SHIELD_EMOJI = '\U0001F6E1'
DAGGER_EMOJI = '\U0001F5E1'
HEART_EMOJI = '\U00002764'

'''
Escordia Icons
'''

ESC_GOLD_ICON = ICON_DICT["GoldIcon"]
ESC_ESSENCE_ICON = ICON_DICT["EssenceIcon"]
ESC_DUNGEON_ICON = ICON_DICT["DungeonIcon"]

ESC_SWORD_ICON = ICON_DICT["SwordIcon"]
ESC_DAGGER_ICON = ICON_DICT["DaggerIcon"]
ESC_AXE_ICON = ICON_DICT["AxeIcon"]
ESC_BOW_ICON = ICON_DICT["BowIcon"]
ESC_STAFF_ICON = ICON_DICT["StaffIcon"]
ESC_SCYTHE_ICON = ICON_DICT["ScytheIcon"]
ESC_HAMMER_ICON = ICON_DICT["HammerIcon"]
ESC_BOOK_ICON = ICON_DICT["BookIcon"]
ESC_SCEPTER_ICON = ICON_DICT["ScepterIcon"]
ESC_KATANA_ICON = ICON_DICT["KatanaIcon"]

ESC_PHYS_HELMET_ICON = ICON_DICT["PhysHelmIcon"]
ESC_MAGIC_HELMET_ICON = ICON_DICT["MagicHelmIcon"]
ESC_HEAVY_ARMOR_ICON = ICON_DICT["HeavyArmorIcon"]
ESC_LIGHT_ARMOR_ICON = ICON_DICT["LightArmorIcon"]
ESC_MAGIC_ARMOR_ICON = ICON_DICT["MagicArmorIcon"]
ESC_ACCESSORY_ICON = ICON_DICT["AccesoryIcon"]

ESC_FIRE_ICON = ICON_DICT["FireIcon"]
ESC_ICE_ICON = ICON_DICT["IceIcon"]
ESC_THUNDER_ICON = ICON_DICT["ThunderIcon"]
ESC_WIND_ICON = ICON_DICT["WindIcon"]
ESC_HOLY_ICON = ICON_DICT["HolyIcon"]
ESC_DARK_ICON = ICON_DICT["DarkIcon"]

ESC_ATK_DOWN_ICON = ICON_DICT["AtkDownIcon"]
ESC_ATK_UP_ICON = ICON_DICT["AtkUpIcon"]
ESC_DEF_DOWN_ICON = ICON_DICT["DefDownIcon"]
ESC_DEF_UP_ICON = ICON_DICT["DefUpIcon"]
ESC_MAT_DOWN_ICON = ICON_DICT["MatDownIcon"]
ESC_MAT_UP_ICON = ICON_DICT["MatUpIcon"]
ESC_MDEF_DOWN_ICON = ICON_DICT["MdfDownIcon"]
ESC_MDEF_UP_ICON = ICON_DICT["MdfUpIcon"]
ESC_LUK_DOWN_ICON = ICON_DICT["LukDownIcon"]
ESC_LUK_UP_ICON = ICON_DICT["LukUpIcon"]

ESC_NOVICE_ICON = ICON_DICT["NoviceIcon"]
ESC_WARRIOR_ICON = ICON_DICT["WarriorIcon"]
ESC_ROGUE_ICON = ICON_DICT["RogueIcon"]
ESC_MAGE_ICON = ICON_DICT["MageIcon"]
ESC_HUNTER_ICON = ICON_DICT["HunterIcon"]
ESC_WARLOCK_ICON = ICON_DICT["WarlockIcon"]
ESC_GLADIATOR_ICON = ICON_DICT["GladiatorIcon"]
ESC_CLERIC_ICON = ICON_DICT["ClericIcon"]


'''
///////////////////////////////// Transforming Dictionaries ////////////////////////////////////
'''

equipment_to_emoji = {"PHYS_HELM": ESC_PHYS_HELMET_ICON, "MAG_HELM": ESC_MAGIC_HELMET_ICON,
                      "HEAVY_ARMOR": ESC_HEAVY_ARMOR_ICON, "LIGHT_ARMOR": ESC_LIGHT_ARMOR_ICON, "MAGIC_ARMOR": ESC_MAGIC_ARMOR_ICON, "ACCESSORY": ESC_ACCESSORY_ICON,
                      "SWORD": ESC_SWORD_ICON, "AXE": ESC_AXE_ICON, "DAGGER": ESC_DAGGER_ICON, "SCYTHE": ESC_SCYTHE_ICON,
                      "STAFF": ESC_STAFF_ICON, "BOW": ESC_BOW_ICON, "HAMMER": ESC_HAMMER_ICON, "BOOK": ESC_BOOK_ICON,
                      "SCEPTER": ESC_SCEPTER_ICON, "KATANA": ESC_KATANA_ICON}
job_to_emoji = {"Novice": ESC_NOVICE_ICON, "Warrior": ESC_WARRIOR_ICON, "Rogue": ESC_ROGUE_ICON, "Mage": ESC_MAGE_ICON,
                "Hunter": ESC_HUNTER_ICON, "Warlock": ESC_WARLOCK_ICON, "Gladiator": ESC_GLADIATOR_ICON, "Cleric": ESC_CLERIC_ICON}
element_to_emoji = {"FIRE": ESC_FIRE_ICON, "ICE": ESC_ICE_ICON, "THUNDER": ESC_THUNDER_ICON, "WIND": ESC_WIND_ICON,
                    "HOLY": ESC_HOLY_ICON, "DARK": ESC_DARK_ICON}
buff_debuff_to_emoji = {"ATK_UP": ESC_ATK_UP_ICON, "ATK_DOWN": ESC_ATK_DOWN_ICON, "DEF_UP": ESC_DEF_UP_ICON,
                        "DEF_DOWN": ESC_DEF_DOWN_ICON, "MATK_UP": ESC_MAT_UP_ICON, "MATK_DOWN": ESC_MAT_DOWN_ICON,
                        "MDEF_UP": ESC_MDEF_UP_ICON, "MDEF_DOWN": ESC_MDEF_DOWN_ICON, "LUK_UP": ESC_LUK_UP_ICON,
                        "LUK_DOWN": ESC_LUK_DOWN_ICON}


def obj_emoji(item: 'Item') -> str:
    """
    Returns the emoji of an item.

    :param item: Item instance.
    :return: String with the emoji.
    """

    try:
        if item.object_type == "EQUIPMENT":
            return equipment_to_emoji[item.equipment_type]
        return ""
    except Exception:
        return ""


def skill_emoji(skill: 'Skill', skill_job: str) -> str:
    """
    Returns the emoji of a skill.

    :param skill: Skill instance.
    :param skill_job: Name of the job the skill belongs to.
    :return: String with the emoji.
    """

    try:
        return element_to_emoji[skill.element]
    except Exception:
        # If skill has no element, it has the same emoji as the job.
        return job_to_emoji[skill_job]
