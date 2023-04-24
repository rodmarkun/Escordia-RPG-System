import json
import json

import area
import constants
import enemy
import equipment
import item
import job
import messager
import player
import shop
import skill

"""
//////////////////
/// CACHE DATA ///
//////////////////
"""
ITEM_CACHE = []
EQUIPMENT_CACHE = []
AREAS_CACHE = {}
DUNGEON_CACHE = []
JOB_CACHE = []
PLAYER_CACHE = []
ENEMIES_CACHE = []
BATTLE_CACHE = []
SHOP_CACHE = []
SKILLS_CACHE = []


"""
///////////////
/// CREATES ///
///////////////
"""


def create_new_player(player_name: str) -> None:
    """
    Records and creates a new player in the system.

    :param player_name: Player's name.
    :return: None.
    """
    PLAYER_CACHE.append(player.Player(player_name))
    messager.messager_add_player(player_name)


"""
///////////////
/// SEARCHS ///
///////////////
"""


def search_cache_player(player_name: str) -> 'Player':
    """
    Searchs a player by name in the player cache.

    :param player_name: Player's name.
    :return: Player if found. Else None.
    """
    for p in PLAYER_CACHE:
        if p.name == player_name:
            return p
    return None


def search_cache_battle_by_player(player_name: str) -> 'Battle':
    """
    Searchs a battle by the name of the player currently fighting on it.

    :param player_name: Player's name.
    :return: Battle if found. Else None.
    """
    for b in BATTLE_CACHE:
        if b.player.name == player_name:
            return b
    return None


def search_cache_enemy_by_name(enemy_name: str) -> 'Enemy':
    """
    Searchs for an enemy in the enemy cache.

    :param enemy_name: Enemy's name.
    :return: Enemy instance. None if not found.
    """
    for e in ENEMIES_CACHE:
        if e.name.lower() == enemy_name.lower():
            return e
    return None


def search_cache_item_by_name(item_name: str) -> 'Item':
    """
    Searchs for an item in the item and equipment cache.

    :param item_name: Item's name.
    :return: Item instance. None if not found.
    """
    for i in ITEM_CACHE:
        if i.name.lower() == item_name.lower():
            return i
    for e in EQUIPMENT_CACHE:
        if e.name.lower() == item_name.lower():
            return e
    return None


def search_cache_shop_by_area(area_index: int) -> 'Shop':
    """
    Searchs for a shop in the shop cache.

    :param area_index: Area's index.
    :return: Shop instance. None if not found.
    """

    for s in SHOP_CACHE:
        if s.area_number == area_index:
            return s
    return None


def search_cache_skill_by_name(skill_name: str) -> 'Skill':
    """
    Searchs for a skill in the skill cache.

    :param skill_name: Skill's name.
    :return: Skill instance. None if not found.
    """
    for s in SKILLS_CACHE:
        if s.name.lower() == skill_name.lower():
            return s
    return None


def search_cache_job_by_name(job_name: str) -> 'Job':
    """
    Searchs for a job in the job cache.

    :param job_name: Job's name.
    :return: Job instance. None if not found.
    """
    for j in JOB_CACHE:
        if j.name.lower() == job_name.lower():
            return j
    return None


"""
///////////////
/// DELETES ///
///////////////
"""


def delete_cache_battle_by_player(player_name: str) -> None:
    """
    Deletes a battle searching by the player's name.

    :param player_name: Player's name.
    :return: None.
    """
    b = search_cache_battle_by_player(player_name)
    if b is not None:
        BATTLE_CACHE.remove(b)


"""
/////////////
/// LOADS ///
/////////////
"""


def load_items_from_json() -> None:
    """
    Loads items from JSON file.

    :return: None.
    """
    with open("data/items.json", 'r', encoding='utf-8') as f:
        json_file = json.load(f)

        for i in json_file:
            param_list = [i[key] for key in constants.ITEM_KEYS]
            ITEM_CACHE.append(item.Item(*param_list))


def load_equipment_from_json() -> None:
    """
    Loads equipment from JSON file.

    :return: None.
    """
    with open("data/equipment.json", 'r', encoding='utf-8') as f:
        json_file = json.load(f)

        for e in json_file:
            param_list = [e[key] for key in constants.EQUIPMENT_KEYS]
            EQUIPMENT_CACHE.append(equipment.Equipment(*param_list))


def load_enemies_from_json() -> None:
    """
    Loads enemies from JSON file.

    :return: None.
    """
    with open("data/enemies.json", 'r', encoding='utf-8') as f:
        json_file = json.load(f)

        for e in json_file:
            # why does this not work ¿?¿?¿?
            param_list = [e[key] for key in constants.ENEMY_KEYS]
            print(*param_list)
            ENEMIES_CACHE.append(enemy.Enemy(*param_list))
            #ENEMIES_CACHE.append(enemy.Enemy(e["NAME"], e["STATS"], e["XP_REWARD"], e["GOLD_REWARD"], e["POSSIBLE_LOOT"],
            #                                 e["LOOT_CHANCE"], e["SKILLS"], e["IMAGE_URL"], e["IS_BOSS"]))


def load_areas_from_json() -> None:
    """
    Loads areas from JSON file.

    :return: None.
    """
    with open("data/areas.json", 'r', encoding='utf-8') as f:
        json_file = json.load(f)

        for a in json_file:
            param_list = [a[key] for key in constants.AREAS_KEYS]
            AREAS_CACHE.update({a["NUMBER"]: area.Area(*param_list)})


def load_dungeons_from_json() -> None:
    """
    Loads dungeons from JSON file.

    :return: None.
    """
    pass


def load_jobs_from_json() -> None:
    """
    Loads jobs from JSON file.

    :return: None.
    """
    with open("data/jobs.json", 'r', encoding='utf-8') as f:
        json_file = json.load(f)

        for j in json_file:
            param_list = [j[key] for key in constants.JOB_KEYS]
            JOB_CACHE.append(job.Job(*param_list))


def load_shops_from_json() -> None:
    """
    Loads shops from JSON file.

    :return: None.
    """
    with open("data/shops.json", 'r', encoding='utf-8') as f:
        json_file = json.load(f)

        for s in json_file:
            param_list = [s[key] for key in constants.SHOP_KEYS]
            print(param_list)
            SHOP_CACHE.append(shop.Shop(*param_list))


def load_skills_from_json() -> None:
    """
    Loads skills from JSON file.

    :return: None.
    """
    with open("data/skills.json", 'r', encoding='utf-8') as f:
        json_file = json.load(f)

        for s in json_file:
            param_list = [s[key] for key in constants.SKILL_KEYS]
            SKILLS_CACHE.append(skill.Skill(*param_list))


def load_players_from_db() -> None:
    """
    Loads players from database.

    :return: None.
    """
    pass


def load_everything():
    print("Loading data...")
    load_items_from_json()
    load_equipment_from_json()
    load_enemies_from_json()
    load_areas_from_json()
    load_dungeons_from_json()
    load_jobs_from_json()
    load_shops_from_json()
    load_skills_from_json()
    load_players_from_db()
