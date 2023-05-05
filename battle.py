import random

import constants
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
        self.skills_in_cooldown = {}
        self.player_stats_before_battle = self.player.stats.copy()

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

        no_enemy_turn = False
        # Normal attack
        if player_action["ACTION"] == "NORMAL_ATTACK":
            normal_attack(attacker=self.player, target=self.enemy, player_name=self.player.name)

        # Skill
        elif player_action["ACTION"] == "SKILL":
            skill = data_management.search_cache_skill_by_name(player_action["SKILL"])
            target = self.skill_based_target_selection(skill, self.player)
            perform_skill(self.player, target, skill, self.player.name)
            self.skills_in_cooldown.update({skill.name: skill.cooldown})
            if constants.SKILL_TAG_DOES_NOT_SKIP_TURN in skill.tags:
                no_enemy_turn = True

        # Enemy turn
        if self.enemy.alive:
            if not no_enemy_turn:
                enemy_action = random.choice(constants.POSSIBLE_ENEMY_ACTIONS)
                if enemy_action == "NORMAL_ATTACK" or len(self.enemy.skills) == 0:
                    normal_attack(attacker=self.enemy, target=self.player, player_name=self.player.name)
                elif enemy_action == "SKILL":
                    skill = data_management.search_cache_skill_by_name(random.choice(self.enemy.skills))
                    target = self.skill_based_target_selection(skill, self.enemy)
                    perform_skill(self.enemy, target, skill, self.player.name)

                # Player dies
                if not self.player.alive:
                    self.is_over = True

        # Player wins
        else:
            messager.add_message(self.player.name, f"{self.enemy.name} has been slain.")
            self.is_over = True
        self.decrease_cooldowns()
        self.decrease_buff_debuff_duration()
        return messager.empty_queue(self.player.name)

    # def apply_buff_debuffs(self):

    def win_battle(self) -> None:
        """
        Player wins the battle.

        :return: None
        """

        # Delete battle from cache
        data_management.delete_cache_battle_by_player(self.player.name)

        messager.add_message(self.player.name, f"{self.player.name} won the battle! You obtain {self.enemy.xp_reward} XP and "
                             f"{self.enemy.gold_reward} G")

        self.battle_is_over()

        # Combat rewards
        self.player.add_exp(self.enemy.xp_reward)
        self.player.add_money(self.enemy.gold_reward)

        loot = self.enemy.loot()
        if loot:
            messager.add_message(self.player.name, f"You looted a {loot}")
            self.player.inventory.add_item(loot, 1)
        else:
            messager.add_message(self.player.name, f"You find nothing to loot")

        del self.enemy

    def lose_battle(self) -> None:
        """
        Player loses the battle.

        :return: None
        """

        # Delete battle from cache
        data_management.delete_cache_battle_by_player(self.player.name)

        messager.add_message(self.player.name, f"{self.player.name} lost the battle! You are brought back to safety, "
                                               f"but half your gold is long gone...")

        # Player loses money and respawns
        self.player.money //= 2
        self.battle_is_over()
        del self.enemy
        self.player.respawn()

    def decrease_buff_debuff_duration(self) -> None:
        """
        Decreases the duration of all buffs and debuffs by 1.

        :return: None.
        """
        # Player buffs and debuffs
        for bd in list(self.player.buffs_and_debuffs):
            if self.player.buffs_and_debuffs[bd] == 0:
                self.player.buffs_and_debuffs.pop(bd)
                self.player.stat_change_on_buff_debuff(bd, expires=True)
            else:
                self.player.buffs_and_debuffs[bd] -= 1
        # Enemy buffs and debuffs
        for bd in list(self.enemy.buffs_and_debuffs):
            if self.enemy.buffs_and_debuffs[bd] == 0:
                self.enemy.buffs_and_debuffs.pop(bd)
                self.enemy.stat_change_on_buff_debuff(bd, expires=True)
            else:
                self.enemy.buffs_and_debuffs[bd] -= 1

    def reset_buff_and_debuffs(self) -> None:
        """
        Erases all buffs and debuffs from the player and the enemy.

        :return: None.
        """

        for bd in self.player.buffs_and_debuffs:
            self.player.stat_change_on_buff_debuff(bd, expires=True)
        for bd in self.enemy.buffs_and_debuffs:
            self.enemy.stat_change_on_buff_debuff(bd, expires=True)

        self.player.buffs_and_debuffs = {}
        self.enemy.buffs_and_debuffs = {}

    def battle_is_over(self) -> None:
        """
        Resets the player's stats and buffs and debuffs.
        :return: None.
        """
        self.reset_buff_and_debuffs()
        self.player.stats.update({key: self.player_stats_before_battle[key] for key in self.player_stats_before_battle
                                  if key not in constants.STATS_NOT_COPYING_AFTER_BATTLE})

    def skill_based_target_selection(self, skill: 'Skill', caster: 'Battler') -> 'Battler':
        """
        Selects the target of a skill based on its type.
        :param skill: Skill to be executed.
        :return: Target of the skill.
        """

        # Damage skills targets enemy
        if skill.type == constants.SKILL_TYPE_DMG:
            if type(caster) == Player:
                return self.enemy
            return self.player
        # Heal skills targets caster
        elif skill.type == constants.SKILL_TYPE_HEAL:
            if type(caster) == Player:
                return self.player
            return self.enemy

    def decrease_cooldowns(self) -> None:
        """
        Decreases the cooldown of all skills in cooldown by 1.
        If the cooldown reaches 0, the skill is removed from the dictionary.

        :return: None
        """
        for skill in list(self.skills_in_cooldown):
            if self.skills_in_cooldown[skill] == 0:
                self.skills_in_cooldown.pop(skill)
            else:
                self.skills_in_cooldown[skill] -= 1

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

    @enemy.deleter
    def enemy(self):
        del self._enemy


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
    # Check if attack hits
    if not check_miss(attacker.stats['SPEED'], target.stats['SPEED']):
        dmg = formulas.normal_attack_dmg(attacker.stats['ATK'], target.stats['DEF'])
        # Check for critical damage
        dmg, is_crit = formulas.check_for_critical_damage(attacker, dmg)
        if is_crit:
            messager.add_message(player_name, f"Critical hit! {attacker.name} attacks {target.name} and deals {dmg} "
                                              f"damage!")
        else:
            messager.add_message(player_name, f"{attacker.name} attacks {target.name} and deals {dmg} damage!")
        target.take_damage(dmg, None)
    else:
        messager.add_message(player_name, f"{attacker.name}'s attack missed!")


def perform_skill(attacker: 'Battler', target: 'Battler', skill: 'Skill', player_name: str) -> None:
    """
    Battler executes a skill.

    :param attacker: Battler executing the skill.
    :param target: Battler to attack.
    :param skill: Skill to be executed.
    :param player_name: Name of the player.
    :return: None.
    """
    if type(attacker) == Enemy or attacker.pay_mana_cost(skill.mp_cost):
        skill.effect(player_name, attacker, target)
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
