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

        messager.add_message(self.name, f"{self.name} fully heals!")
        self.stats['HP'] = self.stats['MAXHP']

    def fully_recover_mp(self) -> None:
        """
        Fully recovers battler's MP

        :return: None.
        """

        messager.add_message(self.name, f"{self.name} fully recovers its MP!")
        self.stats['MP'] = self.stats['MAXMP']

    def heal(self, amount: int) -> None:
        """
        Battler is healed.

        :param amount: Amount of HP to heal.
        :return: None.
        """

        messager.add_message(self.name, f"{self.name} heals for {amount} HP!")
        new_hp = self.stats['HP'] + amount
        if new_hp > self.stats['MAXHP']:
            self.fully_heal()
        else:
            self.stats['HP'] = new_hp

    def recover_mp(self, amount: int) -> None:
        """
        Battler recovers mp.

        :param amount: Amount of MP to recover.
        :return: None.
        """

        messager.add_message(self.name, f"{self.name} recovers {amount} MP!")
        new_mp = self.stats['MP'] + amount
        if new_mp > self.stats['MAXMP']:
            self.fully_recover_mp()
        else:
            self.stats['MP'] = new_mp

    def take_dmg(self, dmg: int) -> None:
        """
        Battler takes damage from any source.
        Subtract damage from its health. Also checks if it dies.

        :param dmg: Damage about to be taken by the battler.
        :return: None.
        """

        dmg = max(0, dmg)  # We don't like negative numbers in these lands
        self.stats['HP'] -= dmg

        # Battler dies
        if self.stats['HP'] <= 0:
            self.alive = False
            self.die()

    def die(self) -> None:
        """
        Battler dies.

        :return: None
        """

        print(f"{self.name} has died.")

    def pay_mana_cost(self, cost: int) -> bool:
        """
        Pays the mana cost for a certain action.

        :param cost: Mana cost.
        :return: True if player has enough mana. False if not.
        """

        if self.stats['MP'] >= cost:
            self.stats['MP'] -= cost
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
