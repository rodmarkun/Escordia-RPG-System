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

    def __init__(self, name, stats, xp_reward, gold_reward, dmg_weaknesses, possible_loot=None, loot_chance=0,
                 image_url='', is_boss=False):
        super().__init__(name, stats)

        self._xp_reward = xp_reward
        self._gold_reward = gold_reward
        self._dmg_weakness = dmg_weaknesses
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
