import math
import constants


class Battler:
    """
    Class that represents a Battler Character in the game (Player & Enemies)
    """

    """
    ///////////////////
    /// CONSTRUCTOR ///
    ///////////////////
    """

    def __init__(self, name: str, stats: dict):
        """
        Constructor of the Battler class.

        :param name: Battler's name.
        :param stats: Battler's stats.
        """

        self.name = name
        self.stats = stats
        self.alive = True  # Is the battler currently alive?
        self.weaknesses = []  # List of elemental weaknesses
        self.resistances = []  # List of elemental resistances
        self.buffs_and_debuffs = {}  # Dictionary of buffs and debuffs the Battler currently has
        self.shield = 0 # Shield the battler currently has

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
            self.stats[constants.MP_STATKEY] = new_mp

    def take_damage(self, dmg: int, damage_element: str) -> int:
        """
        Battler takes damage from any source.
        Subtract damage from its health. Also checks if it dies.

        :param dmg: Damage about to be taken by the battler.
        :param damage_element: Element of the damage dealt.
        :return: Damage dealt.
        """

        # Check weaknesses and resistances
        if damage_element in self.weaknesses or damage_element == constants.RAINBOW_ELEMENTAL_ATTACK:
            dmg = round(dmg * constants.WEAKNESS_DAMAGE_BONUS)
        elif damage_element in self.resistances:
            dmg = round(dmg * constants.RESISTANCE_DAMAGE_REDUCTION)

        dmg = max(0, dmg)  # We don't like negative numbers in these lands

        # Shield absorbs damage first
        if self.shield > 0:
            damage_left = self.shield - dmg
            if damage_left < 0:
                self.shield = 0
                dmg = abs(damage_left)
            else:
                self.shield = damage_left
                dmg = 0

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

        :param buff_debuff: Buff or debuff name to be added.
        :return: None.
        """

        if buff_debuff in constants.BUFFS or constants.DEBUFFS:
            # If alteration was not already applied, change stats
            if buff_debuff not in self.buffs_and_debuffs:
                # If buff/debuff is contrary to another active one, remove it
                if constants.BUFF_DEBUFF_CONTRARIES[buff_debuff] in self.buffs_and_debuffs:
                    self.stat_change_on_buff_debuff(constants.BUFF_DEBUFF_CONTRARIES[buff_debuff], expires=True)
                    del self.buffs_and_debuffs[constants.BUFF_DEBUFF_CONTRARIES[buff_debuff]]
                else:
                    self.stat_change_on_buff_debuff(buff_debuff, expires=False)
            # Add buff/debuff to the dictionary or reset its duration if already there
            self.buffs_and_debuffs[buff_debuff] = constants.BUFF_DEBUFF_DURATION
        else:
            raise ValueError(f"{buff_debuff} is not a valid buff or debuff.")


    def remove_all_debuffs(self) -> None:
        """
        Removes all debuffs from the battler.

        :return: None.
        """

        for debuff in constants.DEBUFFS:
            if debuff in self.buffs_and_debuffs:
                self.stat_change_on_buff_debuff(debuff, expires=True)
                del self.buffs_and_debuffs[debuff]


    def remove_all_buffs(self) -> None:
        """
        Removes all buffs from the battler.

        :return: None.
        """

        for buff in constants.BUFFS:
            if buff in self.buffs_and_debuffs:
                self.stat_change_on_buff_debuff(buff, expires=True)
                del self.buffs_and_debuffs[buff]


    def get_number_of_debbufs(self):
        """
        Returns the number of debuffs the battler has.

        :return: Number of debuffs.
        """

        return len([bd for bd in self.buffs_and_debuffs if bd in constants.DEBUFFS])


    def stat_change_on_buff_debuff(self, buff_debuff: str, expires: bool = False) -> None:
        """
        Changes the stats of the battler based on the buff/debuff.

        :param buff_debuff: Buff/debuff to be applied.
        :param expires: False if buff/debuff is applied, True if it expires.
        :return: None.
        """

        # Find affected stat
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

        # Find if buff or debuff
        if buff_debuff in constants.BUFFS:
            is_buff = True
        else:
            is_buff = False

        # Apply/Remove buff/debuff
        if is_buff:
            if not expires:
                self.stats[stat_affected] = math.ceil(self.stats[stat_affected] * constants.BUFF_MULTIPLIER)
            else:
                self.stats[stat_affected] = math.floor(self.stats[stat_affected] / constants.BUFF_MULTIPLIER)
        else:
            if not expires:
                self.stats[stat_affected] = math.floor(self.stats[stat_affected] * constants.DEBUFF_MULTIPLIER)
            else:
                self.stats[stat_affected] = math.ceil(self.stats[stat_affected] / constants.DEBUFF_MULTIPLIER)

    def pay_mana_cost(self, cost: int, percentage_cost: bool) -> bool:
        """
        Pays the mana cost for a certain action.

        :param cost: Mana cost.
        :param percentage_cost: True if cost is a percentage of the battler's MP.
        :return: True if battler has enough mana. False if not.
        """

        if percentage_cost:
            cost = int(math.ceil(self.stats[constants.MAXMP_STATKEY] * cost/100))
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
            if stat not in constants.STATKEYS:
                raise ValueError(f"You specified a stat not found in your defined stat names: {stat}")
        self._stats = value

    @property
    def alive(self) -> bool:
        return self._alive

    @alive.setter
    def alive(self, value: bool) -> None:
        self._alive = value

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
    def buffs_and_debuffs(self) -> dict:
        return self._buffs_and_debuffs

    @buffs_and_debuffs.setter
    def buffs_and_debuffs(self, value: dict) -> None:
        self._buffs_and_debuffs = value

    @property
    def shield(self) -> int:
        return self._shield

    @shield.setter
    def shield(self, value: int) -> None:
        if value < 0:
            raise ValueError("Shield cannot be negative.")
        else:
            self._shield = value
