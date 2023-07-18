from battle import Battle
from player import Player


class Duel(Battle):
    """
    Class that represents a battle between two players.
    """

    """
    ///////////////////
    /// CONSTRUCTOR ///
    ///////////////////
    """

    def __init__(self, player1: Player, player2: Player):
        super().__init__(player1, player2)
        self.enemy_stats_before_battle = player2.stats.copy()


