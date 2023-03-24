import constants
from player import Player
from enemy import Enemy
import area
import data_management
import interface
import battle


def main():
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
    e = Enemy('Bat', stats, xp_reward=4, gold_reward=2, dmg_weakness=None)
    a = area.Area("Area 1", 1, [e], None, None)
    data_management.AREAS_CACHE.update({1: a})

    player_name = "Rodmar"
    print(interface.create_player(player_name))
    print(interface.begin_battle(player_name))
    print(interface.normal_attack(player_name))
    print(interface.player_rest(player_name))
    print(interface.normal_attack(player_name))
    print(interface.normal_attack(player_name))
    print(interface.normal_attack(player_name))
    print(interface.begin_battle(player_name))
    print(interface.normal_attack(player_name))


if __name__ == '__main__':
    main()
