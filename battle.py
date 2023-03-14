from player import Player
from enemy import Enemy


class Battle:

    def __init__(self, player: Player, enemy: Enemy):
        self.player = player
        self.enemy = enemy