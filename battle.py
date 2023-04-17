import random

import data_management
import emojis
import formulas
import messager
from player import Player
from enemy import Enemy


class Battle:
    """
    Stores information of an ongoing fight.
    """

    """
    ///////////////////
    /// CONSTRUCTOR ///
    ///////////////////
    """

    def __init__(self, player: Player, enemy: Enemy):
        print(f"Initializing battle with Player: {player.name} and Enemy: {enemy.name}")
        self.player = player
        self.enemy = enemy
        self.is_over = False

    """
    ///////////////
    /// METHODS ///
    ///////////////
    """

    def turn(self, player_action: dict) -> list:
        """
        Turn logic.

        :param player_action: Dictionary with player actions.
        :return: List of information strings about turn's events.
        """

        if player_action["ACTION"] == "NORMAL_ATTACK":
            normal_attack(attacker=self.player, target=self.enemy, player_name=self.player.name)
        elif player_action["ACTION"] == "SKILL":
            perform_skill(self.player, self.enemy, player_action["SKILL"], self.player.name)
        if self.enemy.alive:
            normal_attack(attacker=self.enemy, target=self.player, player_name=self.player.name)
            if not self.player.alive:
                self.is_over = True
        else:
            messager.add_message(self.player.name, f"{self.enemy.name} has been slain.")
            self.is_over = True
        return messager.empty_queue(self.player.name)

    def win_battle(self) -> None:
        """
        Player wins the battle.

        :return: None
        """
        data_management.delete_cache_battle_by_player(self.player.name)

        messager.add_message(self.player.name, f"{self.player.name} won the battle! You obtain {self.enemy.xp_reward} XP and "
                             f"{self.enemy.gold_reward} G")

        self.player.add_exp(self.enemy.xp_reward)
        self.player.add_money(self.enemy.gold_reward)

        loot = self.enemy.loot()
        if loot:
            messager.add_message(self.player.name, f"You looted a {loot}")
            self.player.inventory.add_item(loot, 1)
        else:
            messager.add_message(self.player.name, f"You find nothing to loot")

    def lose_battle(self) -> None:
        """
        Player loses the battle.

        :return: None
        """
        data_management.delete_cache_battle_by_player(self.player.name)

        messager.add_message(self.player.name, f"{self.player.name} lost the battle! You are brought back to safety, "
                                               f"but half your gold is long gone...")

        self.player.money //= 2
        self.player.respawn()


    """
    //////////////////
    /// PROPERTIES ///
    //////////////////
    """

    @property
    def player(self) -> Player:
        return self._player

    @player.setter
    def player(self, value: Player) -> None:
        self._player = value

    @property
    def enemy(self) -> Enemy:
        return self._enemy

    @enemy.setter
    def enemy(self, value: Enemy) -> None:
        self._enemy = value

    @property
    def is_over(self) -> bool:
        return self._is_over

    @is_over.setter
    def is_over(self, value: bool) -> None:
        self._is_over = value


def start_battle(player: Player, enemy: Enemy):
    """
    Starts a battle between a Player and an Enemy.

    :param player: Player about to fight.
    :param enemy: Enemy to be fighted.
    :return: Battle instance.
    """

    messager.add_message(player.name, f'You are fighting a **{enemy.name}**')
    return Battle(player, enemy)


def normal_attack(attacker: 'Battler', target: 'Battler', player_name: str) -> None:
    """
    Battler executes a normal attack.

    :param target: Battler to attack.
    :return: None.
    """
    if not check_miss(attacker.stats['SPEED'], target.stats['SPEED']):
        dmg = formulas.normal_attack_dmg(attacker.stats['ATK'], target.stats['DEF'])
        dmg, is_crit = formulas.check_for_critical_damage(attacker, dmg)
        if is_crit:
            messager.add_message(player_name, f"Critical hit! {attacker.name} attacks {target.name} and deals {dmg} "
                                              f"damage!")
        else:
            messager.add_message(player_name, f"{attacker.name} attacks {target.name} and deals {dmg} damage!")
        target.take_dmg(dmg)
    else:
        messager.add_message(player_name, f"{attacker.name}'s attack missed!")


def perform_skill(attacker: 'Battler', target: 'Battler', skill: str, player_name: str) -> None:
    """
    Battler executes a skill.

    :param attacker: Battler executing the skill.
    :param target: Battler to attack.
    :param skill: Skill to be executed.
    :param player_name: Name of the player.
    :return: None.
    """
    skill = data_management.search_cache_skill_by_name(skill)
    if attacker.pay_mana_cost(skill.mp_cost):
        skill.effect(attacker, target)
    else:
        messager.add_message(player_name, f"{attacker.name} doesn't have enough mana to use {skill.name}!")


def check_miss(atk_speed: int, def_speed: int) -> bool:
    """
    Formula for rolling if an attack misses or not. Depends on attacker's and defender's speed.

    :param atk_speed: Attacker's speed.
    :param def_speed: Defender's speed.
    :return: True if attack misses. False if not.
    """

    chance = formulas.miss_formula(atk_speed, def_speed)
    return chance > random.randint(0, 100)