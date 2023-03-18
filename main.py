import constants
from player import Player
from enemy import Enemy
import battle


def main():
    p = Player("Rodmar")
    stats = {'MAXHP': 25,
                     'HP': 25,
                     'MAXMP': 10,
                     'MP': 10,
                     'ATK': 10,
                     'DEF': 10,
                     'MATK': 10,
                     'MDEF': 10,
                     'SPEED': 10
                     }
    e = Enemy('Bat', stats, xp_reward=4, gold_reward=2, dmg_weaknesses=None)

    b = battle.start_battle(p, e)
    print(b.turn("NORMAL_ATTACK"))


if __name__ == '__main__':
    main()
