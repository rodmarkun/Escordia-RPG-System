from battler import Battler


class Enemy(Battler):

    def __init__(self, name, stats, xp_reward, gold_reward, dmg_weaknesses, possible_loot=None, loot_chance=0,
                 image_url='', is_boss=False):
        super().__init__(name, stats)

        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.dmg_weakness = dmg_weaknesses
        self.possible_loot = possible_loot
        self.loot_chance = loot_chance
        self.image_url = image_url
        self.is_boss = is_boss