import messager
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

    def __init__(self, name, stats, xp_reward, gold_reward, dmg_weakness, possible_loot=None, loot_chance=0,
                 image_url='', is_boss=False):
        super().__init__(name, stats)

        self._xp_reward = xp_reward
        self._gold_reward = gold_reward
        self._dmg_weakness = dmg_weakness
        self._possible_loot = possible_loot
        self._loot_chance = loot_chance
        self._image_url = image_url
        self._is_boss = is_boss

    """
    ///////////////
    /// METHODS ///
    ///////////////
    """

    def die(self) -> None:
        messager.add_message(f"{self.name} has been slain.")
        self.alive = False

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
    def dmg_weakness(self) -> list:
        return self._dmg_weakness

    @dmg_weakness.setter
    def dmg_weakness(self, value: list) -> None:
        self._dmg_weakness = value
