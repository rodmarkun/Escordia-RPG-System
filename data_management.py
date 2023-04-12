import csv

import area
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


def search_skill_by_name(skill_name: str) -> 'Skill':
    """
    Searchs for a skill in the skill cache.

    :param skill_name: Skill's name.
    :return: Skill instance. None if not found.
    """
    for s in SKILLS_CACHE:
        if s.name.lower() == skill_name.lower():
            return s
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


def load_items_from_csv() -> None:
    """
    Loads items from CSV file.

    :return: None.
    """
    with open("data/items.csv", 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=';')
        next(csv_reader)  # Skip header row

        for row in csv_reader:
            ITEM_CACHE.append(item.Item(row[0], row[1], int(row[2]), row[3]))


def load_equipment_from_csv() -> None:
    """
    Loads equipment from CSV file.

    :return: None.
    """
    with open("data/equipment.csv", 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=';')
        next(csv_reader)  # Skip header row

        for row in csv_reader:
            EQUIPMENT_CACHE.append(equipment.Equipment(row[0], row[1], int(row[2]), row[3], row[4], eval(row[5])))


def load_enemies_from_csv() -> None:
    """
    Loads enemies from CSV file.

    :return: None.
    """
    with open("data/enemies.csv", 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=';')
        next(csv_reader)  # Skip header row

        for row in csv_reader:
            print(row)
            ENEMIES_CACHE.append(enemy.Enemy(row[0], eval(row[1]), int(row[2]), int(row[3]), row[4], int(row[5]),
                                             row[6], bool(row[7])))


def load_areas_from_csv() -> None:
    """
    Loads areas from CSV file.

    :return: None.
    """
    with open("data/areas.csv", 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=';')
        next(csv_reader)  # Skip header row

        for row in csv_reader:
            AREAS_CACHE.update({int(row[1]): area.Area(row[0], int(row[1]), eval(row[2]), row[3], eval(row[4]))})


def load_dungeons_from_csv() -> None:
    """
    Loads dungeons from CSV file.

    :return: None.
    """
    pass


def load_jobs_from_csv() -> None:
    """
    Loads jobs from CSV file.

    :return: None.
    """
    with open("data/jobs.csv", 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=';')
        next(csv_reader)  # Skip header row

        for row in csv_reader:
            JOB_CACHE.append(job.Job(row[0], row[1], eval(row[2]), int(row[3])))


def load_shops_from_csv() -> None:
    """
    Loads shops from CSV file.

    :return: None.
    """
    with open("data/shops.csv", 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=';')
        next(csv_reader)  # Skip header row

        for row in csv_reader:
            SHOP_CACHE.append(shop.Shop(int(row[0]), eval(row[1])))


def load_skills_from_csv() -> None:
    """
    Loads skills from CSV file.

    :return: None.
    """
    with open("data/skills.csv", 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=';')
        next(csv_reader)  # Skip header row

        for row in csv_reader:
            if row[3] == "HEALING_MAGIC":
                SKILLS_CACHE.append(skill.HealingMagicalSkill(row[0], row[1], int(row[2]), int(row[4]), eval(row[5])))
            elif row[3] == "DAMAGING_MAGIC":
                SKILLS_CACHE.append(skill.DamagingMagicalSkill(row[0], row[1], int(row[2]), int(row[4]), int(row[5])))


def load_players_from_db() -> None:
    """
    Loads players from database.

    :return: None.
    """
    pass


def load_everything():
    print("Loading data...")
    load_items_from_csv()
    load_equipment_from_csv()
    load_enemies_from_csv()
    load_areas_from_csv()
    load_dungeons_from_csv()
    load_jobs_from_csv()
    load_shops_from_csv()
    load_skills_from_csv()
    load_players_from_db()
