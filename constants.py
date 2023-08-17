"""
/////////////
/// PATHS ///
/////////////
"""

EQUIPMENT_PATH = "data/equipment/"
ENEMIES_PATH = "data/enemies/"
SKILLS_PATH = "data/skills/"

"""
/////////////
/// STATS ///
/////////////
"""

MAXHP_STATKEY = 'MAXHP'
HP_STATKEY = 'HP'
MAXMP_STATKEY = 'MAXMP'
MP_STATKEY = 'MP'
ATK_STATKEY = 'ATK'
DEF_STATKEY = 'DEF'
MATK_STATKEY = 'MATK'
MDEF_STATKEY = 'MDEF'
SPEED_STATKEY = 'SPEED'
CRITCH_STATKEY = 'CRITCH'
CRITDMG_STATKEY = 'CRITDMG'

INITIAL_STATS = {MAXHP_STATKEY: 25,
                 HP_STATKEY: 25,
                 MAXMP_STATKEY: 10,
                 MP_STATKEY: 10,
                 ATK_STATKEY: 10,
                 DEF_STATKEY: 10,
                 MATK_STATKEY: 10,
                 MDEF_STATKEY: 10,
                 SPEED_STATKEY: 10,
                 CRITCH_STATKEY: 10,
                 CRITDMG_STATKEY: 10
                 }
STATKEYS = [MAXHP_STATKEY, HP_STATKEY, MAXMP_STATKEY, MP_STATKEY, ATK_STATKEY, DEF_STATKEY,
            MATK_STATKEY, MDEF_STATKEY, SPEED_STATKEY, CRITCH_STATKEY, CRITDMG_STATKEY]

STATKEYS_NO_HP_MP = [ATK_STATKEY, DEF_STATKEY, MATK_STATKEY, MDEF_STATKEY, SPEED_STATKEY, CRITCH_STATKEY, CRITDMG_STATKEY]

"""
/////////////
/// ITEMS ///
/////////////
"""

HELMET_KEY = 'HELMET'
ARMOR_KEY = 'ARMOR'
WEAPON_KEY = 'WEAPON'
ACCESSORY_KEY = 'ACCESSORY'

EQUIPMENT_TYPES = [HELMET_KEY, ARMOR_KEY, WEAPON_KEY, ACCESSORY_KEY]
HELM_TYPES = ["PHYS_HELM", "MAG_HELM"]
ARMOR_TYPES = ["HEAVY_ARMOR", "LIGHT_ARMOR", "MAGIC_ARMOR"]
WEAPON_TYPES = ["SWORD", "AXE", "DAGGER", "SCYTHE", "STAFF", "BOW", "HAMMER", "BOOK", "SCEPTER", "KATANA"]

INITIAL_EQUIPMENT = {equipment: None for equipment in EQUIPMENT_TYPES}

"""
///////////////
/// OPTIONS ///
///////////////
"""

FULLY_RECOVER_WHEN_LEVELING_UP = True
STAT_UPGRADE_WHEN_LEVELING_UP = 1
STATS_NOT_UPGRADING_WHEN_LEVELING_UP = [CRITCH_STATKEY, CRITDMG_STATKEY]
NORMAL_ATTACK_OPTION = "NORMAL_ATTACK"
SKILL_OPTION = "SKILL"
POSSIBLE_PLAYER_ACTIONS = [NORMAL_ATTACK_OPTION, SKILL_OPTION]
POSSIBLE_ENEMY_ACTIONS = [NORMAL_ATTACK_OPTION, SKILL_OPTION]
LEECH_AMOUNT = 0.5
STATS_NOT_COPYING_AFTER_BATTLE = [MAXHP_STATKEY, MAXMP_STATKEY, HP_STATKEY, MP_STATKEY]
TREASURE_CHANCE_WHEN_FIGHTING = 10  # %
NUMBER_OF_ITEMS_IN_TREASURE = 1
MAX_INVENTORY_SLOTS = 25
PREFERRED_WEAPON_DAMAGE_BONUS = 1.20
ENEMY_AI_WEIGHTS = [1,3] # Chance weights of enemies using normal attack (25% default) or using skill if possible (75% default).
RAINBOW_ELEMENTAL_ATTACK = "RAINBOW"
WEAKNESS_DAMAGE_BONUS = 1.25
RESISTANCE_DAMAGE_REDUCTION = 0.75

"""
////////////
/// JOBS ///
////////////
"""

INITIAL_JOB_DICT = {"Name": "Novice", "lvl": 1, "xp": 0, "xp_to_next_lvl": 30}

"""
//////////////
/// SKILLS ///
//////////////
"""

SKILL_TAG_STANCE = "STANCE"
SKILL_TAG_DOES_NOT_SKIP_TURN = "DOES_NOT_SKIP_TURN"
SKILL_TAG_LEECH = "LEECH"
SKILL_TAG_SELF_INFLICT_BUFF_DEBUFF = "SELF_INFLICT_BUFF_DEBUFF"
SKILL_TAG_INFLICT_BUFF_DEBUFF = "INFLICT_BUFF_DEBUFF"
SKILL_TAG_PHYSICAL = "PHYSICAL"
SKILL_TAG_MAGICAL = "MAGICAL"
SKILL_TAG_ALTERATION = "ALTERATION"
SKILL_TAG_HEALING = "HEALING"
SKILL_TAG_RECOVER_MP = "RECOVER_MP"
SKILL_TAG_SHIELD = "SHIELD"
SKILL_TAG_RAINBOW = "RAINBOW"
SKILL_TAG_SELF_REMOVE_DEBUFFS = "SELF_REMOVE_DEBUFFS"
SKILL_TAG_REMOVE_DEBUFFS = "REMOVE_DEBUFFS"
SKILL_TAG_REMOVE_BUFFS = "REMOVE_BUFFS"
SKILL_TAG_DEBUFF_EXPLOIT = "DEBUFF_EXPLOIT"

"""
/////////////////////
/// BUFFS/DEBUFFS ///
/////////////////////
"""

BUFF_ATK_UP = "ATK_UP"
BUFF_DEF_UP = "DEF_UP"
BUFF_MATK_UP = "MATK_UP"
BUFF_MDEF_UP = "MDEF_UP"
BUFF_LUK_UP = "LUK_UP"

DEBUFF_ATK_DOWN = "ATK_DOWN"
DEBUFF_DEF_DOWN = "DEF_DOWN"
DEBUFF_MATK_DOWN = "MATK_DOWN"
DEBUFF_MDEF_DOWN = "MDEF_DOWN"
DEBUFF_LUK_DOWN = "LUK_DOWN"

ATK_BD = [BUFF_ATK_UP, DEBUFF_ATK_DOWN]
DEF_BD = [BUFF_DEF_UP, DEBUFF_DEF_DOWN]
MATK_BD = [BUFF_MATK_UP, DEBUFF_MATK_DOWN]
MDEF_BD = [BUFF_MDEF_UP, DEBUFF_MDEF_DOWN]
LUK_BD = [BUFF_LUK_UP, DEBUFF_LUK_DOWN]

BUFFS = [BUFF_ATK_UP, BUFF_DEF_UP, BUFF_MATK_UP, BUFF_MDEF_UP, BUFF_LUK_UP]
DEBUFFS = [DEBUFF_ATK_DOWN, DEBUFF_DEF_DOWN, DEBUFF_MATK_DOWN, DEBUFF_MDEF_DOWN, DEBUFF_LUK_DOWN]

BUFF_DEBUFF_CONTRARIES = {BUFF_ATK_UP: DEBUFF_ATK_DOWN,
                            BUFF_DEF_UP: DEBUFF_DEF_DOWN,
                            BUFF_MATK_UP: DEBUFF_MATK_DOWN,
                            BUFF_MDEF_UP: DEBUFF_MDEF_DOWN,
                            BUFF_LUK_UP: DEBUFF_LUK_DOWN,
                            DEBUFF_ATK_DOWN: BUFF_ATK_UP,
                            DEBUFF_DEF_DOWN: BUFF_DEF_UP,
                            DEBUFF_MATK_DOWN: BUFF_MATK_UP,
                            DEBUFF_MDEF_DOWN: BUFF_MDEF_UP,
                            DEBUFF_LUK_DOWN: BUFF_LUK_UP}

BUFF_DEBUFF_DURATION = 4

BUFF_MULTIPLIER = 1.35
DEBUFF_MULTIPLIER = 0.65

BUFF_DEBUFF_TO_MESSAGE = {BUFF_ATK_UP: "Attack increased",
                          BUFF_DEF_UP: "Defense increased",
                          BUFF_MATK_UP: "Magic attack increased",
                          BUFF_MDEF_UP: "Magic defense increased",
                          BUFF_LUK_UP: "Luck increased",
                          DEBUFF_ATK_DOWN: "Attack decreased",
                          DEBUFF_DEF_DOWN: "Defense decreased",
                          DEBUFF_MATK_DOWN: "Magic attack decreased",
                          DEBUFF_MDEF_DOWN: "Magic defense decreased",
                          DEBUFF_LUK_DOWN: "Luck decreased"}

"""
////////////
/// JSON ///
////////////
(These are the keys that are used in the JSON files)
"""

AREAS_KEYS = ["NAME", "NUMBER", "ENEMY_LIST", "BOSS", "DUNGEONS", "TREASURES"]
DUNGEON_KEYS = ["DUNGEON_NAME", "RECOMMENDED_LVL", "ENEMY_LIST", "BOSS", "ENEMY_COUNT", "LOOT_POOL"]
ENEMY_KEYS = ["NAME", "STATS", "DESCRIPTION", "XP_REWARD", "GOLD_REWARD", "POSSIBLE_LOOT", "LOOT_CHANCE", "SKILLS", "WEAKNESSES",
              "RESISTANCES", "IMAGE_URL", "IS_BOSS"]
EQUIPMENT_KEYS = ["NAME", "DESCRIPTION", "INDIV_VALUE", "OBJECT_TYPE", "EQUIPMENT_TYPE", "STAT_CHANGE_LIST"]
ITEM_KEYS = ["NAME", "DESCRIPTION", "INDIV_VALUE", "OBJECT_TYPE"]
JOB_KEYS = ["NAME", "DESCRIPTION", "SKILL_DICT", "REQUISITES", "XP_FACTOR", "PREFERRED_WEAPONS"]
SHOP_KEYS = ["AREA_NUMBER", "ITEM_LIST"]
SKILL_KEYS = ["NAME", "DESCRIPTION", "MP_COST", "POWER", "ELEMENT", "COOLDOWN", "TAGS", "PERCENTAGE_COST"]
BLESSING_KEYS = ["NAME", "STAT_CHANGE_LIST", "ESSENCE_COST"]
