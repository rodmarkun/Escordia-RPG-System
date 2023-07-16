import copy
import random

import blessing
import messager
import player
import data_management
import battle
import shop
from error_msgs import *

"""
////////////////
/// COMMANDS ///
////////////////
"""


def create_player(name: str) -> (bool, list):
    """
    Creates a new Player in the system.

    :param name: Player's name.
    :return: Bool and List. True if character was created, False if it was not. String contains info messages.
    """
    if data_management.search_cache_player(name) is None:
        data_management.create_new_player(name)
        print(f"Created character with name: {name}")
        return True, [f"Created character with name: {name}"]
    return False, [ERROR_CHARACTER_ALREADY_CREATED]


def begin_battle(name: str, boss: bool, *, enemy: str = None) -> (bool, list):
    """
    Creates a new Battle in the system.

    :param name: Player's name.
    :param boss: True if the player wants to fight a boss, False if he wants to fight a normal enemy.
    :return: Bool and List. True if Battle was created, False if it was not. String contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    if data_management.search_cache_battle_by_player(name) is None:
        area = data_management.AREAS_CACHE[player_inst.current_area]
        if enemy is None:
            if boss:
                enemy_inst = area.spawn_boss()
            else:
                enemy_inst = area.spawn_random_enemy()
        else:
            enemy_inst = copy.deepcopy(data_management.ENEMIES_CACHE[enemy])
        data_management.update_player_info(player_inst.name)
        data_management.BATTLE_CACHE.update({player_inst.name: battle.Battle(player_inst, enemy_inst)})
        return True, ['']
    return False, [ERROR_CHARACTER_ALREADY_IN_FIGHT]


def normal_attack(name: str) -> (bool, list):
    """
    Player performs a normal attack against the enemy.

    :param name: Player's name.
    :return: Bool and List. True if attack was performed. False if there were errors. String contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    battle_inst = data_management.search_cache_battle_by_player(name)
    if battle_inst is not None:
        return True, battle_inst.turn({"ACTION": "NORMAL_ATTACK"})
    return False, [ERROR_CHARACTER_NOT_IN_FIGHT]


def check_battle_is_over(name: str) -> (bool, list):
    """
    Checks if a battle is over.

    :param name: Player's name.
    :return: Bool and List. True if battle is over. False if there were errors. String contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    battle_inst = data_management.search_cache_battle_by_player(name)
    if battle_inst is not None:
        if battle_inst.is_over:
            battle_inst.win_battle()
            data_management.update_player_info(player_inst.name)
            return True, messager.empty_queue(name)
        return False, ["Battle is not over yet."]
    return False, [ERROR_CHARACTER_NOT_IN_FIGHT]


def skill_attack(name: str, skill_name: str) -> (bool, list):
    """
    Player performs a skill attack against the enemy.

    :param name: Player's name.
    :param skill_name: Skill's name.
    :return: Bool and List. True if attack was performed. False if there were errors. String contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    battle_inst = data_management.search_cache_battle_by_player(name)
    if battle_inst is not None:
        return True, battle_inst.turn({"ACTION": "SKILL", "SKILL": skill_name})
    return False, [ERROR_CHARACTER_NOT_IN_FIGHT]


def show_player_profile(name: str) -> (bool, list):
    """
    Shows a player's profile.

    :param name: Player's name.
    :return: Bool and list. True if player was found. False if there were errors. String contains info message.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]
    return True, [player_inst.show_player_info()]


def player_rest(name: str) -> (bool, list):
    """
    Player rests and fully recovers HP/MP

    :param name: Player's name.
    :return: Bool and List. True if rest was performed. False if there were errors. String contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    if data_management.search_cache_battle_by_player(name) is None:
        player_inst.recover()
        data_management.update_player_info(player_inst.name)
        return True, [f"{name}, you are now rested and fully recovered your HP/MP."]

    return False, [ERROR_CANNOT_DO_WHILE_IN_FIGHT]


def show_player_inventory(name: str) -> (bool, list):
    """
    Shows player's inventory.

    :param name: Player's name.
    :return: Bool and list. True if player was found. False if there were errors. List contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    return True, [player_inst.inventory.show_inventory()]


def show_shop_inventory(name: str) -> (bool, list):
    """
    Shows shop's inventory.
    :param name: Player's name.
    :return: Bool and list. True if player was found. False if there were errors. List contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    if data_management.search_cache_battle_by_player(name) is not None:
        return False, [ERROR_CANNOT_DO_WHILE_IN_FIGHT]

    return True, [data_management.search_cache_shop_by_area(player_inst.current_area).show_items()]


def buy_item(name: str, item_name: str) -> (bool, list):
    """
    Player buys an item from the shop.

    :param name: Player's name.
    :param item_name: Item's name.
    :return: Bool and list. True if item was bought. False if there were errors. List contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    if data_management.search_cache_battle_by_player(name) is not None:
        return False, [ERROR_CANNOT_DO_WHILE_IN_FIGHT]

    # TODO - Check if item exists in shop of current area

    shop.buy_item(player_inst, item_name)
    data_management.update_player_info(player_inst.name)
    return True, messager.empty_queue(name)


def purchase_blessing(name: str, blessing_name: str) -> (bool, list):
    """
    Player purchases a blessing from the shop.

    :param name: Player's name.
    :param blessing_name: Blessing's name.
    :return: Bool and list. True if blessing was purchased. False if there were errors. List contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    if data_management.search_cache_battle_by_player(name) is not None:
        return False, [ERROR_CANNOT_DO_WHILE_IN_FIGHT]

    blessing.purchase_blessing(player_inst, blessing_name)
    data_management.update_player_info(player_inst.name)
    return True, messager.empty_queue(name)


def show_area(name: str) -> (bool, list):
    """
    Shows the current area.

    :param name: Player's name.
    :return: Bool and list. True if area was shown. False if there were errors. List contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    area_inst = data_management.search_cache_area_by_number(player_inst.current_area)

    return True, [f"You are currently in **{area_inst.name}** (Area {area_inst.number}). To unlock the next area you need to this area's boss: **{area_inst.boss}**."]


def travel_to_area(name: str, area_number: int) -> (bool, list):
    """
    Player travels to an area.

    :param name: Player's name.
    :param area_number: Area to travel to.
    :return:
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    if data_management.search_cache_battle_by_player(name) is not None:
        return False, [ERROR_CANNOT_DO_WHILE_IN_FIGHT]

    if area_number == player_inst.current_area:
        return False, [ERROR_ALREADY_IN_AREA]

    player_inst.current_area = area_number
    data_management.update_player_info(player_inst.name)
    return True, [f"You have traveled to {data_management.search_cache_area_by_number(area_number).name}."]


def destroy_item_for_essence(name: str, item_name: str) -> (bool, list):
    """
    Player destroys an item for essence.

    :param name: Player's name.
    :param item_name: Item's name.
    :return: Bool and list. True if item was destroyed. False if there were errors. List contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    if data_management.search_cache_battle_by_player(name) is not None:
        return False, [ERROR_CANNOT_DO_WHILE_IN_FIGHT]

    if item_name not in player_inst.inventory.items.keys():
        return False, [ERROR_ITEM_ALREADY_DESTROYED]
    essence, quantity_destroyed = player_inst.inventory.destroy_item_for_essence(item_name)
    player_inst.essence += essence
    data_management.update_player_info(player_inst.name)
    return True, messager.empty_queue(name)


def equip_item(name: str, item_name: str) -> (bool, list):
    """
    Player equips an item from their inventory.

    :param name: Player's name.
    :param item_name: Item's name.
    :return: Bool and list. True if item was equipped. False if there were errors. List contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    if data_management.search_cache_battle_by_player(name) is not None:
        return False, [ERROR_CANNOT_DO_WHILE_IN_FIGHT]

    player_inst.equip_item(item_name)
    data_management.update_player_info(player_inst.name)
    return True, messager.empty_queue(name)


def show_player_job(name: str, show_skills = True) -> (bool, list):
    """
    Shows player's job.

    :param name: Player's name.
    :return: Bool and list. True if player was found. False if there were errors. List contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    if data_management.search_cache_battle_by_player(name) is not None:
        return False, [ERROR_CANNOT_DO_WHILE_IN_FIGHT]

    return True, [player_inst.show_player_info_job(show_skills)]


def essence_crafting(name: str) -> (bool, list):
    """
    Player crafts essence.

    :param name: Player's name.
    :return: Bool and list. True if player was found. False if there were errors. List contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    if data_management.search_cache_battle_by_player(name) is not None:
        return False, [ERROR_CANNOT_DO_WHILE_IN_FIGHT]

    return True, []


def receive_treasure(name: str, item_amount: int) -> (bool, list):
    """
    Player receives treasure from a defeated enemy.

    :param name: Player's name.
    :param item_amount: Amount of items to receive.
    :return: Bool and list. True if player was found. False if there were errors. List contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    if player_inst.in_dungeon:
        items = data_management.search_cache_dungeon_inst_by_player(name).loot_pool
    else:
        items = data_management.search_cache_area_by_number(player_inst.current_area).treasures

    given_items = []

    for _ in range(item_amount):
        item = random.choice(items)
        given_items.append(item)
        player_inst.inventory.add_item(item, 1)

    data_management.update_player_info(player_inst.name)
    return True, given_items


def show_dungeons(name: str) -> (bool, list):
    """
    Shows dungeons available in player's current area.
    :param name: Player's name.
    :return: Bool and list. True if player was found. False if there were errors. List contains dungeon names.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    if data_management.search_cache_battle_by_player(name) is not None:
        return False, [ERROR_CANNOT_DO_WHILE_IN_FIGHT]

    if player_inst.in_dungeon:
        return False, [ERROR_ALREADY_IN_DUNGEON]

    return True, data_management.search_cache_area_by_number(player_inst.current_area).dungeons


def start_dungeon(name: str, dungeon_name: str) -> (bool, list):
    """
    Starts a dungeon.

    :param name: Player's name.
    :param dungeon_name: Dungeon's name.
    :return: Bool and list. True if dungeon was started. False if there were errors. List contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    if data_management.search_cache_battle_by_player(name) is not None:
        return False, [ERROR_CANNOT_DO_WHILE_IN_FIGHT]

    if player_inst.in_dungeon:
        return False, [ERROR_ALREADY_IN_DUNGEON]

    if dungeon_name not in data_management.search_cache_area_by_number(player_inst.current_area).dungeons:
        return False, [ERROR_DUNGEON_NOT_IN_AREA]

    dungeon_inst = data_management.search_cache_dungeon_by_name(dungeon_name)

    if dungeon_inst is None:
        return False, [ERROR_DUNGEON_DOES_NOT_EXIST]

    player_inst.in_dungeon = True
    data_management.create_new_dungeon_inst(player_inst, dungeon_inst)

    return True, messager.empty_queue(name)


def change_player_job(name: str, job_name: str) -> (bool, list):
    """
    Changes player's job.

    :param name: Player's name.
    :param job_name: Job's name.
    :return: Bool and list. True if job was changed. False if there were errors. List contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    if data_management.search_cache_battle_by_player(name) is not None:
        return False, [ERROR_CANNOT_DO_WHILE_IN_FIGHT]

    if player_inst.change_job(job_name):
        data_management.update_player_info(player_inst.name)
        return True, messager.empty_queue(name)
    return False, [ERROR_JOB_DOES_NOT_EXIST]
