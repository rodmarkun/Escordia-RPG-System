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

    def turn(self, player_action: dict) -> None:
        """
        Turn logic.

        :param player_action: Dictionary with player actions.
        :return: None.
        """

        if player_action['ACTION'] == "NORMAL_ATTACK":
            self.player.normal_attack(self.enemy)
