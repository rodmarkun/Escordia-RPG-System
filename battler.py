import math

import constants
import formulas
import messager


class Battler:
    """
    Class that represents a Battler Character in the game (Player, enemies...)
    """

    """
    ///////////////////
    /// CONSTRUCTOR ///
    ///////////////////
    """

    def __init__(self, name: str, stats: dict):
        self.name = name
        self.stats = stats
        self.alive = True
        self.weaknesses = []
        self.resistances = []
        self.buffs_and_debuffs = {}

    """
    ///////////////
    /// METHODS ///
    ///////////////
    """

    def fully_heal(self) -> None:
        """
        Fully heals a battler

        :return: None.
        """

        self.stats[constants.HP_STATKEY] = self.stats[constants.MAXHP_STATKEY]

    def fully_recover_mp(self) -> None:
        """
        Fully recovers battler's MP

        :return: None.
        """

        self.stats[constants.MP_STATKEY] = self.stats[constants.MAXMP_STATKEY]

    def heal(self, amount: int) -> None:
        """
        Battler is healed.

        :param amount: Amount of HP to heal.
        :return: None.
        """

        new_hp = self.stats[constants.HP_STATKEY] + amount
        if new_hp > self.stats[constants.MAXHP_STATKEY]:
            self.fully_heal()
        else:
            self.stats[constants.HP_STATKEY] = new_hp

    def recover_mp(self, amount: int) -> None:
        """
        Battler recovers mp.

        :param amount: Amount of MP to recover.
        :return: None.
        """

        new_mp = self.stats[constants.MP_STATKEY] + amount
        if new_mp > self.stats[constants.MAXMP_STATKEY]:
            self.fully_recover_mp()
        else:
            self.stats['MP'] = new_mp

    def take_damage(self, dmg: int, damage_type: str) -> int:
        """
        Battler takes damage from any source.
        Subtract damage from its health. Also checks if it dies.

        :param dmg: Damage about to be taken by the battler.
        :param damage_type: Type of damage.
        :return: Damage dealt.
        """

        # Check weaknesses and resistances
        if damage_type in self.weaknesses:
            dmg = round(dmg * 1.35)
        elif damage_type in self.resistances:
            dmg = round(dmg * 0.65)
        dmg = max(0, dmg)  # We don't like negative numbers in these lands
        self.stats[constants.HP_STATKEY] -= dmg

        # Battler dies
        if self.stats[constants.HP_STATKEY] <= 0:
            self.alive = False
            self.die()

        return dmg

    def die(self) -> None:
        """
        Battler dies.

        :return: None
        """

        print(f"{self.name} has died.")

    def add_buff_debuff(self, buff_debuff: str) -> None:
        """
        Adds a buff or debuff to the battler.

        :return: None.
        """
        if buff_debuff in constants.BUFFS or constants.DEBUFFS:
            self.buffs_and_debuffs[buff_debuff] = 3
            self.stat_change_on_buff_debuff(buff_debuff, expires=False)
        else:
            raise ValueError(f"{buff_debuff} is not a valid buff or debuff.")

    def stat_change_on_buff_debuff(self, buff_debuff: str, expires: bool = False) -> None:
        """
        Changes the stats of the battler based on the buff/debuff.

        :param buff_debuff: Buff/debuff to be applied.
        :param expires: False if buff/debuff is applied, True if it expires.
        :return: None.
        """
        stat_affected = None
        if buff_debuff in constants.ATK_BD:
            stat_affected = constants.ATK_STATKEY
        elif buff_debuff in constants.DEF_BD:
            stat_affected = constants.DEF_STATKEY
        elif buff_debuff in constants.MATK_BD:
            stat_affected = constants.MATK_STATKEY
        elif buff_debuff in constants.MDEF_BD:
            stat_affected = constants.MDEF_STATKEY
        elif buff_debuff in constants.LUK_BD:
            stat_affected = constants.CRITCH_STATKEY

        if buff_debuff in constants.BUFFS:
            is_buff = True
        else:
            is_buff = False

        if is_buff:
            if not expires:
                self.stats[stat_affected] = math.ceil(self.stats[stat_affected] * 1.35)
                print(1)
            else:
                self.stats[stat_affected] = math.floor(self.stats[stat_affected] / 1.35)
                print(2)
        else:
            if not expires:
                self.stats[stat_affected] = math.floor(self.stats[stat_affected] * 0.65)
                print(3)
            else:
                self.stats[stat_affected] = math.ceil(self.stats[stat_affected] / 0.65)
                print(4)

    def pay_mana_cost(self, cost: int) -> bool:
        """
        Pays the mana cost for a certain action.

        :param cost: Mana cost.
        :return: True if player has enough mana. False if not.
        """

        if self.stats[constants.MP_STATKEY] >= cost:
            self.stats[constants.MP_STATKEY] -= cost
            return True
        return False

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
            raise ValueError("Battler name cannot be empty.")
    
    @property
    def stats(self) -> dict:
        return self._stats
    
    @stats.setter
    def stats(self, value: dict) -> None:
        for stat in value:
            if stat not in constants.STAT_NAMES:
                raise ValueError(f"You specified a stat not found in your defined stat names: {stat}")
        self._stats = value

    @property
    def alive(self) -> bool:
        return self._alive

    @alive.setter
    def alive(self, value: bool) -> None:
        self._alive = value
