import data_management
import enemy
import random
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

    def __init__(self, name, number, enemy_list, boss, dungeons):
        self.name = name
        self.number = number
        self.enemy_list = enemy_list
        self.boss = boss
        self.dungeons = dungeons

    """
    ///////////////
    /// METHODS ///
    ///////////////
    """

    def spawn_enemy(self) -> enemy.Enemy:
        enemy_name = random.choice(self.enemy_list)
        enemy_inst = data_management.search_cache_enemy_by_name(enemy_name)
        return enemy.Enemy(enemy_inst.name, enemy_inst.stats.copy(), enemy_inst.xp_reward, enemy_inst.gold_reward,
                           enemy_inst.possible_loot, enemy_inst.loot_chance, enemy_inst.skills, enemy_inst.image_url,
                           enemy_inst.is_boss)

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
    def boss(self) -> enemy.Enemy:
        return self._boss

    @boss.setter
    def boss(self, value: enemy.Enemy) -> None:
        self._boss = value
