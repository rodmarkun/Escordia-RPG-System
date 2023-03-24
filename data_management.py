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
BATTLE_CACHE = []

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

"""
//////////////////
/// DELETES ///
//////////////////
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
