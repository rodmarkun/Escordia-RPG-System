import data_management
import error_msgs
import formulas
import inventory
import messager
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
        self.xp_rate = 1
        self.money: int = 50
        self.inventory: inventory.Inventory = inventory.Inventory(self.name)
        self.equipment: dict = {equipment: None for equipment in constants.EQUIPMENT_TYPES}
        self.skills: list = ["Small Fireball"]
        self.passives: list = []
        self.current_area: int = 1
        self.in_fight: bool = False
        self.in_dungeon: bool = False
        self.defeated_bosses: list = []
        self.job_dict_list: list = []
        self.current_job_dict: dict = constants.INITIAL_JOB_DICT
        self.current_job = 'Novice'

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

        # Exp for the job is not affected by Player's XP rate given by passives (change?)
        self.add_exp_job(exp)

        exp *= self.xp_rate
        self.xp += exp
        leveled_up = False

        # Leveling up
        while self.xp >= self.xp_to_next_lvl:
            self.xp -= self.xp_to_next_lvl
            self.lvl += 1
            leveled_up = True
            self.xp_to_next_lvl = formulas.xp_next_lvl_formula(self.xp_to_next_lvl, self._lvl)
            for stat in self.stats:
                if stat not in constants.STATS_NOT_UPGRADING_WHEN_LEVELING_UP:
                    self.stats[stat] += constants.STAT_UPGRADE_WHEN_LEVELING_UP
            if constants.FULLY_RECOVER_WHEN_LEVELING_UP:
                self.recover()

            messager.add_message(self.name, f"You leveled up! You are now level {self.lvl}")
        return leveled_up

    def add_exp_job(self, exp: int) -> bool:
        """
        Adds a certain amount of XP to the player's job.
        :param exp: Amount of XP to be added.
        :return: True if player levels up, False if it does not.
        """
        curr_job = data_management.search_cache_job_by_name(self.current_job)
        exp *= curr_job.xp_factor
        self.current_job_dict['xp'] += exp
        leveled_up = False

        while self.current_job_dict['xp'] >= self.current_job_dict['xp_to_next_lvl']:
            self.current_job_dict['xp'] -= self.current_job_dict['xp_to_next_lvl']
            self.current_job_dict['lvl'] += 1
            new_level_str = str(self.current_job_dict['lvl'])
            leveled_up = True
            self.current_job_dict['xp_to_next_lvl'] = formulas.xp_next_lvl_job_formula(self.current_job_dict['xp_to_next_lvl'], self.current_job_dict['lvl'])
            messager.add_message(self.name,
                                 f"Your job has leveled up! You are now a level {self.current_job_dict['lvl']} {self.current_job}")
            if new_level_str in curr_job.skill_dict:
                # TODO - Check if passive
                self.skills.append(curr_job.skill_dict[new_level_str])
                messager.add_message(self.name,
                                     f"You learnt {curr_job.skill_dict[new_level_str]}!")
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

        stat_string = ''.join([f'**{stat}**: {self.stats[stat]}\n' for stat in constants.STATKEYS])
        equipment_string = ''.join([f"**{e}**: {self.equipment[e]}\n" if self.equipment[e] is not None else
                                    f"**{e}**: None\n" for e in self.equipment])

        return f'**Player Name**: {self.name}\n' \
               f'**Level**: {self.lvl}\n' \
               f'**Xp**: {self.xp}\n' \
               f'**Xp to next level**: {self.xp_to_next_lvl - self.xp}\n' \
               f'**---STATS---**\n' \
               f'{stat_string}' \
               f'**---EQUIPMENT---**\n' \
               f'{equipment_string}' \
               f'**----------------**\n' \
               f'**Money**: {self.money}\n' \
               f'**Bosses Defeated**: {self._defeated_bosses}\n'

    def show_player_info_job(self) -> str:
        """
        Shows all the current info (profile) about the player's job.

        :return: String containing the player's information.
        """
        job = data_management.search_cache_job_by_name(self.current_job)
        skills_to_learn_str = '\n'
        for lvl in job.skill_dict:
            skills_to_learn_str += f'Level {lvl}: {job.skill_dict[lvl]}\n'

        return f'**Job**: {self.current_job}\n' \
               f'**Level**: {self.current_job_dict["lvl"]}\n' \
               f'**Xp to next level**: {self.current_job_dict["xp_to_next_lvl"] - self.current_job_dict["xp"]}\n' \
               f'**Skills to learn** {skills_to_learn_str}'

    def equip_item(self, equipment: str) -> (bool, list):
        """
        Equips an item from the player's inventory.

        :param equipment: Equipment name.
        :return: Boolean and list. True if player was able to equip the item. False if it was not. List
        contains messages.
        """

        e = self.inventory.item_exists(equipment)
        if e is not None:
            if e.object_type != "EQUIPMENT":
                return False, [error_msgs.ERROR_CANNOT_EQUIP_THAT_ITEM]
            self.inventory.remove_item(equipment, 1)
            if e.equipment_type in constants.WEAPON_TYPES:
                if self.equipment["WEAPON"] is not None:
                    self.unequip_item(self.equipment["WEAPON"])
                self.equipment.update({"WEAPON": e.name})
            else:
                if self.equipment[e.equipment_type] is not None:
                    self.unequip_item(self.equipment[e.equipment_type])
                self.equipment.update({e.equipment_type: e.name})

            # Adds stats to player
            for stat in e.stat_change_list:
                self.stats[stat] += e.stat_change_list[stat]
            messager.add_message(self.name, f'You have equipped your {equipment}.')
            return True, [f'You have successfully equipped your {equipment}.']
        return False, [error_msgs.ERROR_CHARACTER_DOES_NOT_HAVE_THAT_ITEM]

    def unequip_item(self, equipment) -> None:
        """
        Unequips an item.

        :param equipment: Equipment to unequip.
        :return: None.
        """
        self.inventory.add_item(equipment, 1)
        for stat in equipment.stat_change_list:
            self.stats[stat] -= equipment.stat_change_list[stat]

    def change_job(self, job_name: str) -> bool:
        """
        Changes the player's job.

        :param job_name: Job name.
        :return: True if job was changed, False if it was not.
        """

        if data_management.search_cache_job_by_name(job_name) is not None:
            # TODO - Add job change requirements logic
            self.current_job = job_name
            messager.add_message(self.name, f'Your job is now {job_name}!')
            return True
        return False

    def die(self) -> None:
        """
        Performs all actions needed whenever a player dies.

        :return: None.
        """

        messager.add_message(self.name, f"You have died. You are brought back to safety, but half your gold is"
                                        f" long gone...")
        self._in_dungeon = False
        self.money = formulas.money_lost_when_dying(self.money)

    def respawn(self) -> None:
        """
        Respawns a dead player.

        :return: None.
        """

        if not self.alive:
            self.alive = True
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
        return self._lvl

    @lvl.setter
    def lvl(self, value: int) -> None:
        if value < 0:
            raise ValueError("Player's level cannot be set to a value below 0.")
        self._lvl = value

    @property
    def xp(self) -> int:
        return self._xp

    @xp.setter
    def xp(self, value: int) -> None:
        if value < 0:
            raise ValueError("Player's XP cannot be set to a value below 0.")
        self._xp = value

    @property
    def xp_to_next_lvl(self) -> int:
        return self._xp_to_next_lvl

    @xp_to_next_lvl.setter
    def xp_to_next_lvl(self, value: int) -> None:
        if value < 0:
            raise ValueError("Player's XP to next level cannot be set to a value below 0.")
        self._xp_to_next_lvl = value

    @property
    def xp_rate(self) -> float:
        return self._xp_rate

    @xp_rate.setter
    def xp_rate(self, value: float) -> None:
        if value < 0:
            raise ValueError("Player's XP rate cannot be set to a value below 0.")
        self._xp_rate = value

    @property
    def money(self) -> int:
        return self._money

    @money.setter
    def money(self, value: int) -> None:
        if value < 0:
            raise ValueError("Player's money cannot be set to a value below 0.")
        self._money = value

    @property
    def equipment(self) -> dict:
        return self._equipment

    @equipment.setter
    def equipment(self, value: dict) -> None:
        self._equipment = value

    @property
    def skills(self) -> list:
        return self._skills

    @skills.setter
    def skills(self, value: list) -> None:
        self._skills = value

    @property
    def passives(self) -> list:
        return self._passives

    @passives.setter
    def passives(self, value: list) -> None:
        self._passives = value

    @property
    def current_area(self) -> int:
        return self._current_area

    @current_area.setter
    def current_area(self, value: int) -> None:
        self._current_area = value

    @property
    def in_fight(self) -> bool:
        return self._in_fight

    @in_fight.setter
    def in_fight(self, value: bool) -> None:
        self._in_fight = value

    @property
    def in_dungeon(self) -> bool:
        return self._in_dungeon

    @in_dungeon.setter
    def in_dungeon(self, value: bool) -> None:
        self._in_dungeon = value

    @property
    def defeated_bosses(self) -> list:
        return self._defeated_bosses

    @defeated_bosses.setter
    def defeated_bosses(self, value: list) -> None:
        self._defeated_bosses = value

    @property
    def job_dict_list(self) -> list:
        return self._job_dict_list
    
    @job_dict_list.setter
    def job_dict_list(self, value: list) -> None:
        self._job_dict_list = value

    @property
    def current_job(self) -> str:
        return self._current_job

    @current_job.setter
    def current_job(self, value: str) -> None:
        if value is None:
            raise ValueError(f"A player must always have a valid Job.")
        self._current_job = value
