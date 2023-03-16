import formulas
from battler import Battler
import constants


class Player(Battler):
    """
    Class that represents a Player in the game.
    """

    """
    ///////////////////
    /// CONSTRUCTOR ///
    ///////////////////
    """
    
    def __init__(self, name: str):
        super().__init__(name, constants.INITIAL_STATS)

        self.lvl: int = 1
        self.xp: int = 0
        self.xp_to_next_lvl: int = 15
        self.money: int = 50
        # Inventory
        self.equipment: dict = {equipment: None for equipment in constants.EQUIPMENT_NAMES}
        # Skills
        self.current_area: int = 1
        self.in_fight: bool = False
        self.in_dungeon: bool = False
        self.defeated_bosses: list = []

    """
    ///////////////
    /// METHODS ///
    ///////////////
    """

    def add_exp(self, exp: int) -> bool:
        """
        Adds a certain amount of XP to the player. Handles leveling up.
        If constant "FULLY_RECOVER_WHEN_LEVELING_UP" is True, the Player recovers all HP and MP when levelling up.

        :param exp: Experience points to be added to the player.
        :return: True if player levels up, False if it does not.
        """

        self.xp += exp
        leveled_up = False

        # Leveling up
        while self.xp >= self.xp_to_next_lvl:
            self.xp -= self.xp_to_next_lvl
            self.lvl += 1
            leveled_up = True
            # You can change this formula for different exp progression
            self.xp_to_next_lvl = formulas.xp_next_lvl_formula(self.xp_to_next_lvl, self.lvl)
            for stat in self.stats:
                self.stats[stat] += constants.STAT_UPGRADE_WHEN_LEVELING_UP
            if constants.FULLY_RECOVER_WHEN_LEVELING_UP:
                self.recover()
        return leveled_up

    def add_money(self, money: int) -> None:
        """
        Adds a certain amount of money to the player.

        :param money: Money to be added.
        :return: None.
        """

        self.money += money

    def show_player_info(self) -> str:
        """
        Shows all the current info (profile) about the player.

        :return: String containing the player's information.
        """

        stat_string = ''.join([f'**{stat}**: {self.stats[stat]}\n' for stat in constants.STAT_NAMES])

        return f'**Player Name**: {self.name}\n' \
               f'**Level**: {self.lvl}\n' \
               f'**Xp**: {self.xp}\n' \
               f'**Xp to next level**: {self.xp_to_next_lvl - self.xp}\n' \
               f'**---STATS---**\n' \
               f'{stat_string}' \
               f'**---EQUIPMENT---**\n' \
               f'**TODO**: TODO\n' \
               f'**----------------**\n' \
               f'**Money**: {self.money}\n' \
               f'**Bosses Defeated**: {self.defeated_bosses}\n'

    def die(self) -> None:
        """
        Performs all actions needed whenever a player dies.

        :return: None.
        """

        self.in_dungeon = False
        self.alive = True
        self.money = formulas.money_lost_when_dying(self.money)
        self.recover()

    def recover(self) -> None:
        """
        Makes the player recover all its HP and MP.

        :return: None.
        """
        super().fully_heal()
        super().fully_recover_mp()

    """
    //////////////////
    /// PROPERTIES ///
    //////////////////
    """

    @property
    def lvl(self) -> int:
        return self.lvl

    @lvl.setter
    def lvl(self, value: int) -> None:
        if value < 0:
            raise ValueError("Player's level cannot be set to a value below 0.")
        self.lvl = value

    @property
    def xp(self) -> int:
        return self.xp

    @xp.setter
    def xp(self, value: int) -> None:
        if value < 0:
            raise ValueError("Player's XP cannot be set to a value below 0.")
        self.xp = value

    @property
    def xp_to_next_lvl(self) -> int:
        return self.xp_to_next_lvl

    @xp_to_next_lvl.setter
    def xp_to_next_lvl(self, value: int) -> None:
        if value < 0:
            raise ValueError("Player's XP to next level cannot be set to a value below 0.")
        self.xp_to_next_lvl = value

    @property
    def money(self) -> int:
        return self.money

    @money.setter
    def money(self, value: int) -> None:
        if value < 0:
            raise ValueError("Player's money cannot be set to a value below 0.")
        self.money = value

    @property
    def equipment(self) -> dict:
        return self.equipment

    @equipment.setter
    def equipment(self, value: dict) -> None:
        self.equipment = value

    @property
    def current_area(self) -> int:
        return self.current_area

    @current_area.setter
    def current_area(self, value: int) -> None:
        self.current_area = value

    @property
    def in_fight(self) -> bool:
        return self.in_fight

    @in_fight.setter
    def in_fight(self, value: bool) -> None:
        self.in_fight = value

    @property
    def in_dungeon(self) -> bool:
        return self.in_dungeon

    @in_dungeon.setter
    def in_dungeon(self, value: bool) -> None:
        self.in_dungeon = value

    @property
    def defeated_bosses(self) -> list:
        return self.defeated_bosses

    @defeated_bosses.setter
    def defeated_bosses(self, value: list) -> None:
        self.defeated_bosses = value
