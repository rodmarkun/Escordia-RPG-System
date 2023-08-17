import random
from battler import Battler


class Enemy(Battler):
    """
    Class that represent enemies player can encounter.
    """

    """
    ///////////////////
    /// CONSTRUCTOR ///
    ///////////////////
    """

    def __init__(self, name, stats, description, xp_reward, gold_reward, possible_loot=None, loot_chance=0,
                 skills=[], weaknesses=[], resistances=[], image_url='', is_boss=False):
        super().__init__(name, stats)

        self.description = description
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.possible_loot = possible_loot
        self.loot_chance = loot_chance
        self.skills = skills
        self.weaknesses = weaknesses
        self.resistances = resistances
        self.image_url = image_url
        self.is_boss = is_boss

    """
    ///////////////
    /// METHODS ///
    ///////////////
    """

    def die(self) -> None:
        """
        Enemy dies.

        :return: None
        """

        self.alive = False

    def loot(self) -> str:
        """
        Rolls for loot, used when enemy dies.

        :return: String with item looted. Empty string if no item was looted.
        """

        if self.possible_loot is not None and random.randint(0, 100) <= self.loot_chance:
            return self.possible_loot
        # Returns an empty string for message convenience
        return ''

    def show_enemy_info(self) -> str:
        """
        Returns a string with all of this enemy's information.

        :return: Info string
        """

        return ''.join([f'**{stat}**: {self.stats[stat]}\n' for stat in self.stats])

    """
    //////////////////
    /// PROPERTIES ///
    //////////////////
    """

    @property
    def xp_reward(self) -> int:
        return self._xp_reward

    @xp_reward.setter
    def xp_reward(self, value: int) -> None:
        if value < 0:
            raise ValueError(f"XP Reward of enemy cannot be negative.")
        self._xp_reward = value

    @property
    def gold_reward(self) -> int:
        return self._gold_reward

    @gold_reward.setter
    def gold_reward(self, value: int) -> None:
        if value < 0:
            raise ValueError(f"Gold Reward of enemy cannot be negative.")
        self._gold_reward = value

    @property
    def possible_loot(self) -> str:
        return self._possible_loot

    @possible_loot.setter
    def possible_loot(self, value: str) -> None:
        self._possible_loot = value

    @property
    def loot_chance(self) -> int:
        return self._loot_chance

    @loot_chance.setter
    def loot_chance(self, value: int) -> None:
        self._loot_chance = value

    @property
    def skills(self) -> list:
        return self._skills

    @skills.setter
    def skills(self, value: list) -> None:
        self._skills = value

    @property
    def weaknesses(self) -> list:
        return self._weaknesses

    @weaknesses.setter
    def weaknesses(self, value: list) -> None:
        self._weaknesses = value

    @property
    def resistances(self) -> list:
        return self._resistances

    @resistances.setter
    def resistances(self, value: list) -> None:
        self._resistances = value

    @property
    def image_url(self) -> str:
        return self._image_url

    @image_url.setter
    def image_url(self, value: str) -> None:
        self._image_url = value

    @property
    def is_boss(self) -> bool:
        return self._is_boss

    @is_boss.setter
    def is_boss(self, value: bool) -> None:
        self._is_boss = value
