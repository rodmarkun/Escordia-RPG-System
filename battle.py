import data_management
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

        if player_action == "NORMAL_ATTACK":
            self.player.normal_attack(self._enemy)
            if self.enemy.alive:
                self.enemy.normal_attack(self._player)
            else:
                self.win_battle()
        return messager.empty_queue()

    def win_battle(self) -> None:
        data_management.delete_cache_battle_by_player(self.player.name)

        messager.add_message(f"{self.player.name} won the battle! You obtain {self.enemy.xp_reward} XP and "
                             f"{self.enemy.gold_reward} G")

        self.player.add_exp(self.enemy.xp_reward)
        self.player.add_money(self.enemy.gold_reward)

        loot = self.enemy.loot()
        if loot:
            messager.add_message(f"You looted a {loot}")


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


def start_battle(player: Player, enemy: Enemy):
    """
    Starts a battle between a Player and an Enemy.

    :param player: Player about to fight.
    :param enemy: Enemy to be fighted.
    :return: Battle instance.
    """

    messager.add_message(f'You are fighting a **{enemy.name}**')
    return Battle(player, enemy)


