import constants
import data_management
import messager
import player

class Blessing:
    """
    Class that represents a Blessing in the game (bought with essences)
    """

    def __init__(self, name: str, stat_change_list: list, essence_cost: int):
        """
        Constructor of the Blessing class.
        """
        self.name = name
        self.stat_change_list = stat_change_list
        self.essence_cost = essence_cost


def purchase_blessing(player_inst: player.Player, blessing_name: str) -> bool:
    blessing_inst = data_management.search_cache_blessing(blessing_name)
    if blessing_inst.essence_cost > player_inst.essence:
        messager.add_message(player_inst.name, f"{player_inst.name} you do not have enough essence to purchase {blessing_name}.")
        return False
    if blessing_inst.name not in player_inst.blessings:
        player_inst.essence -= blessing_inst.essence_cost
        player_inst.blessings.append(blessing_name)
        for stat in blessing_inst.stat_change_list:
            splitted_str = stat.split(' ')
            if len(splitted_str) == 2 and splitted_str[1] in constants.STATKEYS:
                player_inst.stats[splitted_str[1]] += int(splitted_str[0].replace('+', ''))
        messager.add_message(player_inst.name, f"You successfully purchased {blessing_name}.")
        return True
    else:
        messager.add_message(player_inst.name, f"You already have {blessing_name}.")
        return False