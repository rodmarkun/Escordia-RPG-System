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


def load_items_from_csv():
    """
    Loads items from CSV file.

    :return: None.
    """
    pass


def load_equipment_from_csv():
    """
    Loads equipment from CSV file.

    :return: None.
    """
    pass


def load_areas_from_csv():
    """
    Loads areas from CSV file.

    :return: None.
    """


def load_dungeons_from_csv():
    """
    Loads dungeons from CSV file.

    :return: None.
    """
    pass


def load_jobs_from_csv():
    """
    Loads jobs from CSV file.

    :return: None.
    """
    pass


def load_players_from_db():
    """
    Loads players from database.

    :return: None
    """
    pass


def load_everything():
    print("Loading data...")
    load_items_from_csv()
    load_equipment_from_csv()
    load_areas_from_csv()
    load_dungeons_from_csv()
    load_jobs_from_csv()
    load_players_from_db()
