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

    def __init__(self, name, stats, xp_reward, gold_reward, possible_loot=None, loot_chance=0,
                 skills=[], weaknesses=[], resistances=[], image_url='', is_boss=False):
        super().__init__(name, stats)

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
        self.alive = False

    def loot(self) -> str:
        if self.possible_loot is not None and random.randint(0, 100) <= self.loot_chance:
            return self.possible_loot
        return ''

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
