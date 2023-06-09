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

'''
///////////////////////////////// Escordia Original Icons/Emojis ////////////////////////////////////
'''

ESC_POTION_ICON = "<:PotionIcon:1011284504205340723>"
ESC_GRIMOIRE_ICON = "<:GrimoireIcon:1011284500875059260>"
ESC_MATERIAL_ICON = "<:MaterialIcon:1011284503177736332>"
ESC_CHEST_ICON = "<:ChestIcon:1011289459918131211>"
ESC_BAG_ICON = "<:BagIcon:1012287527123685426>"
ESC_GOLD_ICON = "<:GoldIcon:1127957365925367909>"
ESC_ESSENCE_ICON = "<:EssenceIcon:1127956174034194503>"
ESC_SHOP_ICON = "<:ShopIcon:1016637098528362528>"
ESC_DUNGEON_ICON = "<:DungeonIcon:1115934734023929946>"

ESC_SWORD_ICON = "<:SwordIcon:1100057957078679595>"
ESC_DAGGER_ICON = "<:DaggerIcon:1065228959400333312>"
ESC_AXE_ICON = "<:AxeIcon:1100057368630415441>"
ESC_BOW_ICON = "<:BowIcon:1065228957152190554>"
ESC_STAFF_ICON = "<:StaffIcon:1065228961627504701>"
ESC_SCYTHE_ICON = "<:ScytheIcon:1100057367456010250>"
ESC_HAMMER_ICON = "<:HammerIcon:1100057372300431411>"
ESC_BOOK_ICON = "<:BookIcon:1100057370912108594>"
ESC_SCEPTER_ICON = "<:ScepterIcon:1100057375844610108>"
ESC_KATANA_ICON = "<:KatanaIcon:1100057374313693215>"

ESC_PHYS_HELMET_ICON = "<:PhysHelmIcon:1116377327841054814>"
ESC_MAGIC_HELMET_ICON = "<:MagicHelmIcon:1116377850212270150>"
ESC_HEAVY_ARMOR_ICON = "<:HeavyArmorIcon:1116379318726168626>"
ESC_LIGHT_ARMOR_ICON = "<:LightArmorIcon:1116379859082555542>"
ESC_MAGIC_ARMOR_ICON = "<:MagicArmorIcon:1116380094957621319>"
ESC_ACCESSORY_ICON = "<:AccessoryIcon:1116379593864118343>"

ESC_FIRE_ICON = "<:FireIcon:1065215887344410664>"
ESC_ICE_ICON = "<:IceIcon:1065216648879022080>"
ESC_THUNDER_ICON = "<:ThunderIcon:1065216650649026581>"
ESC_WIND_ICON = "<:WindIcon:1065216653060743230>"
ESC_HOLY_ICON = "<:HolyIcon:1065216646437937223>"
ESC_DARK_ICON = "<:DarkIcon:1065216644810539059>"

ESC_ATK_DOWN_ICON = "<:AtkDownIcon:1113040647021146153>"
ESC_ATK_UP_ICON = "<:AtkUpIcon:1113040648237494373>"
ESC_DEF_DOWN_ICON = "<:DefDownIcon:1113040649332211814>"
ESC_DEF_UP_ICON = "<:DefUpIcon:1113040651697782804>"
ESC_MAT_DOWN_ICON = "<:MatDownIcon:1113040639265886319>"
ESC_MAT_UP_ICON = "<:MatUpIcon:1113040641987989515>"
ESC_MDEF_DOWN_ICON = "<:MdefDownIcon:1113040643367895130>"
ESC_MDEF_UP_ICON = "<:MdefUpIcon:1113040644886237255>"
ESC_LUK_DOWN_ICON = "<:LukDownIcon:1113040653300011059>"
ESC_LUK_UP_ICON = "<:LukUpIcon:1113040655845961728>"

'''
///////////////////////////////// Job Icons ////////////////////////////////////
'''

ESC_NOVICE_ICON = "<:NoviceIcon:1098328110316916737>"
ESC_WARRIOR_ICON = "<:WarriorIcon:1098328108551131186>"
ESC_ROGUE_ICON = "<:RogueIcon:1098328107284439170>"
ESC_MAGE_ICON = "<:MageIcon:1098328105199865916>"

'''
///////////////////////////////// Transforming Dictionaries ////////////////////////////////////
'''

equipment_to_emoji = {"PHYS_HELM": ESC_PHYS_HELMET_ICON, "MAG_HELM": ESC_MAGIC_HELMET_ICON,
                      "HEAVY_ARMOR": ESC_HEAVY_ARMOR_ICON, "LIGHT_ARMOR": ESC_LIGHT_ARMOR_ICON, "MAGIC_ARMOR": ESC_MAGIC_ARMOR_ICON, "ACCESSORY": ESC_ACCESSORY_ICON,
                      "SWORD": ESC_SWORD_ICON, "AXE": ESC_AXE_ICON, "DAGGER": ESC_DAGGER_ICON, "SCYTHE": ESC_SCYTHE_ICON,
                      "STAFF": ESC_STAFF_ICON, "BOW": ESC_BOW_ICON, "HAMMER": ESC_HAMMER_ICON, "BOOK": ESC_BOOK_ICON,
                      "SCEPTER": ESC_SCEPTER_ICON, "KATANA": ESC_KATANA_ICON}
obj_to_emoji = {"POTION": ESC_POTION_ICON, "LOOT": ESC_MATERIAL_ICON}
job_to_emoji = {"Novice": ESC_NOVICE_ICON, "Warrior": ESC_WARRIOR_ICON, "Rogue": ESC_ROGUE_ICON, "Mage": ESC_MAGE_ICON}
element_to_emoji = {"FIRE": ESC_FIRE_ICON, "ICE": ESC_ICE_ICON, "THUNDER": ESC_THUNDER_ICON, "WIND": ESC_WIND_ICON,
                    "HOLY": ESC_HOLY_ICON, "DARK": ESC_DARK_ICON}
buff_debuff_to_emoji = {"ATK_UP": ESC_ATK_UP_ICON, "ATK_DOWN": ESC_ATK_DOWN_ICON, "DEF_UP": ESC_DEF_UP_ICON,
                        "DEF_DOWN": ESC_DEF_DOWN_ICON, "MAT_UP": ESC_MAT_UP_ICON, "MAT_DOWN": ESC_MAT_DOWN_ICON,
                        "MDEF_UP": ESC_MDEF_UP_ICON, "MDEF_DOWN": ESC_MDEF_DOWN_ICON, "LUK_UP": ESC_LUK_UP_ICON,
                        "LUK_DOWN": ESC_LUK_DOWN_ICON}


def obj_emoji(item: 'Item') -> str:
    """
    Returns the emoji of an item.

    :param item: Item instance.
    :return: String with the emoji.
    """
    if item.object_type == "EQUIPMENT":
        return equipment_to_emoji[item.equipment_type]
    return obj_to_emoji[item.object_type]


def skill_emoji(skill: 'Skill', skill_job) -> str:
    """
    Returns the emoji of a skill.

    :param skill: Skill instance.
    :return: String with the emoji.
    """
    try:
        return element_to_emoji[skill.element]
    except Exception:
        # If skill has no element, it has the same emoji as the job.
        return job_to_emoji[skill_job]
