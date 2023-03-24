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
        self._name = name
        self._number = number
        self._enemy_list = enemy_list
        self._boss = boss
        self._dungeons = dungeons

    """
    ///////////////
    /// METHODS ///
    ///////////////
    """

    def spawn_enemy(self) -> enemy.Enemy:
        enemy_inst = random.choice(self.enemy_list)
        stats = {'MAXHP': 25,
         'HP': 25,
         'MAXMP': 10,
         'MP': 10,
         'ATK': 10,
         'DEF': 10,
         'MATK': 10,
         'MDEF': 10,
         'SPEED': 10
         }
        return enemy.Enemy(enemy_inst.name, stats, enemy_inst.xp_reward,
                           enemy_inst.gold_reward, enemy_inst.dmg_weakness)

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
