import data_management
import enemy
import random
import copy
import dungeon


class Area:
    """
    Stores information about areas in the game.
    """

    """
    ///////////////////
    /// CONSTRUCTOR ///
    ///////////////////
    """

    def __init__(self, name, number, enemy_list, boss, dungeons, treasures):
        """
        Area constructor.

        :param name: Area's name.
        :param number: Area's identifying number.
        :param enemy_list: Possible enemies to spawn in the area.
        :param boss: Boss of the area.
        :param dungeons: Dungeons found in the area.
        """
        self.name = name
        self.number = number
        self.enemy_list = enemy_list
        self.boss = boss
        self.dungeons = dungeons
        self.treasures = treasures

    """
    ///////////////
    /// METHODS ///
    ///////////////
    """

    def spawn_random_enemy(self) -> enemy.Enemy:
        """
        Spawns a random enemy from the area's enemy list.

        :return: Enemy instance.
        """
        enemy_name = random.choice(self.enemy_list)
        enemy_inst = data_management.search_cache_enemy_by_name(enemy_name)
        return copy.deepcopy(enemy_inst)

    def spawn_boss(self) -> enemy.Enemy:
        """
        Spawns the area's boss.

        :return: Boss instance.
        """
        enemy_inst = data_management.search_cache_enemy_by_name(self.boss)
        return copy.deepcopy(enemy_inst)

    def spawn_random_treasure(self) -> str:
        """
        Spawns a random treasure from the area's treasure list.

        :return: Item instance.
        """
        return random.choice(self.treasures)

    """
    //////////////////
    /// PROPERTIES ///
    //////////////////
    """

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if value:
            self._name = value
        else:
            raise ValueError("An area's name cannot be empty.")

    @property
    def number(self) -> int:
        return self._number

    @number.setter
    def number(self, value: int) -> None:
        if value >= 0:
            self._number = value
        else:
            raise ValueError("Area's number cannot be negative.")

    @property
    def enemy_list(self) -> list:
        return self._enemy_list

    @enemy_list.setter
    def enemy_list(self, value: list) -> None:
        self._enemy_list = value

    @property
    def boss(self) -> str:
        return self._boss

    @boss.setter
    def boss(self, value: str) -> None:
        self._boss = value
