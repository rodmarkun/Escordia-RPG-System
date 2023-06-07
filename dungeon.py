class Dungeon:
    """
    Class holding all info related to dungeons.
    """

    """
    ///////////////////
    /// CONSTRUCTOR ///
    ///////////////////
    """

    def __init__(self, dungeon_name: str, recommended_lvl: int, enemy_list: list, boss: str, enemy_count: int, loot_pool: list):
        """
        Creates a new dungeon.

        :param dungeon_name: Name of the dungeon
        :param recommended_lvl: Recommended level for this dungeon. Will be displayed to the player.
        :param enemy_list: List of enemies that will appear in the dungeon
        :param boss: Dungeon's boss
        :param enemy_count: Amount of enemies that will appear in the dungeon (aside from boss)
        :param loot_pool: Objects that will appear in the dungeon
        """
        self.dungeon_name = dungeon_name
        self.recommended_lvl = recommended_lvl
        self.enemy_list = enemy_list
        self.boss = boss
        self.enemy_count = enemy_count
        self.loot_pool = loot_pool
        self.current_enemies_defeated = 0
        self.boss_defeated = False
