SPARKLER_EMOJI = '\U0001F387'
SKULL_EMOJI = '\U0001F480'

'''
///////////////////////////////// Escordia Original Icons/Emojis ////////////////////////////////////
'''

ESC_HELMET_ICON = "<:HelmetIcon:1011284502020112394>"
ESC_ARMOR_ICON = "<:ArmorIcon:1011284499314786388>"
ESC_WEAPON_ICON = "<:WeaponIcon:1011284505451057152>"
ESC_ACCESSORY_ICON = "<:AccessoryIcon:1011284498572394607>"
ESC_POTION_ICON = "<:PotionIcon:1011284504205340723>"
ESC_GRIMOIRE_ICON = "<:GrimoireIcon:1011284500875059260>"
ESC_MATERIAL_ICON = "<:MaterialIcon:1011284503177736332>"
ESC_CHEST_ICON = "<:ChestIcon:1011289459918131211>"
ESC_BAG_ICON = "<:BagIcon:1012287527123685426>"
ESC_MONEY_ICON = "<:MoneyIcon:1012287531070525480>"
ESC_SHOP_ICON = "<:ShopIcon:1016637098528362528>"

ESC_SWORD_ICON = "<:SwordIcon:1065228964320252014>"
# TODO - Spear Icon
ESC_DAGGER_ICON = "<:DaggerIcon:1065228959400333312>"
ESC_AXE_ICON = "<:HeavyIcon:1065228960499249162>"
ESC_BOW_ICON = "<:BowIcon:1065228957152190554>"
ESC_STAFF_ICON = "<:StaffIcon:1065228961627504701>"

ESC_FIRE_ICON = "<:FireIcon:1065215887344410664>"
ESC_ICE_ICON = "<:IceIcon:1065216648879022080>"
ESC_THUNDER_ICON = "<:ThunderIcon:1065216650649026581>"
ESC_WIND_ICON = "<:WindIcon:1065216653060743230>"
ESC_HOLY_ICON = "<:HolyIcon:1065216646437937223>"
ESC_DARK_ICON = "<:DarkIcon:1065216644810539059>"

equipment_to_emoji = {"HELMET": ESC_HELMET_ICON, "ARMOR": ESC_ARMOR_ICON, "ACCESSORY": ESC_ACCESSORY_ICON, "SWORD": ESC_SWORD_ICON, "AXE": ESC_AXE_ICON, "SPEAR": None, "DAGGER": ESC_DAGGER_ICON, "STAFF": ESC_STAFF_ICON, "BOW": ESC_BOW_ICON}
obj_to_emoji = {"POTION": ESC_POTION_ICON, "LOOT": ESC_MATERIAL_ICON}


FIRE_SKILLS = ["Small Fireball"]
HOLY_SKILLS = ["First Aid"]


def obj_emoji(item: 'Item') -> str:
    """
    Returns the emoji of an item.

    :param item: Item instance.
    :return: String with the emoji.
    """
    if item.object_type == "EQUIPMENT":
        return equipment_to_emoji[item.equipment_type]
    return obj_to_emoji[item.object_type]


def skill_emoji(skill: 'Skill') -> str:
    """
    Returns the emoji of a skill.

    :param skill: Skill instance.
    :return: String with the emoji.
    """
    if skill.name in FIRE_SKILLS:
        return ESC_FIRE_ICON
    elif skill.name in HOLY_SKILLS:
        return ESC_HOLY_ICON
    return ""
