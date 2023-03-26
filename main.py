import constants
from player import Player
from enemy import Enemy
import area
import data_management
import interface
import battle


def main():
    data_management.load_everything()
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
    player_name = "Rodmar"
    print(interface.create_player(player_name))
    print(data_management.search_cache_player(player_name).inventory.add_item("Novice Sword", 1))
    print(data_management.search_cache_player(player_name).equip_item("Novice Sword"))
    print(interface.begin_battle(player_name))
    print(interface.normal_attack(player_name))
    print(interface.player_rest(player_name))
    print(interface.normal_attack(player_name))
    print(interface.normal_attack(player_name))
    print(interface.normal_attack(player_name))
    print(interface.show_player_profile(player_name))
    print(interface.show_player_inventory(player_name))


if __name__ == '__main__':
    main()
