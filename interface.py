import messager
import player
import data_management
import battle
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
        data_management.PLAYER_CACHE.append(player.Player(name))
        print(f"Created character with name: {name}")
        return True, ['']
    return False, [ERROR_CHARACTER_ALREADY_CREATED]


def begin_battle(name: str) -> (bool, list):
    """
    Creates a new Battle in the system.

    :param name: Player's name.
    :return: Bool and List. True if Battle was created, False if it was not. String contains info messages.
    """
    player_inst = data_management.search_cache_player(name)

    if player_inst is None:
        return False, [ERROR_CHARACTER_DOES_NOT_EXIST]

    if data_management.search_cache_battle_by_player(name) is None:
        area = data_management.AREAS_CACHE[player_inst.current_area]
        enemy_inst = area.spawn_enemy()
        data_management.BATTLE_CACHE.append(battle.Battle(player_inst, enemy_inst))
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
        return True, battle_inst.turn("NORMAL_ATTACK")
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
        return True, messager.empty_queue()

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
