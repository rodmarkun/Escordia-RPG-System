import constants
import data_management
import messager
import player

class Blessing:
    """
    Class that represents a Blessing in the game (bought with essences)
    """

    """
    ///////////////////
    /// CONSTRUCTOR ///
    ///////////////////
    """

    def __init__(self, name: str, stat_change_list: list, essence_cost: int):
        """
        Constructor of the Blessing class.

        :param name: Blessing's name.
        :param stat_change_list: List of stat changes the blessing gives.
        :param essence_cost: Essence cost of the blessing.
        """

        self.name = name
        self.stat_change_list = stat_change_list
        self.essence_cost = essence_cost

"""
///////////////
/// METHODS ///
///////////////
"""

def purchase_blessing(player_inst: player.Player, blessing_name: str) -> bool:
    """
    Player purchases a blessing.

    :param player_inst: Player instance.
    :param blessing_name: Purchased blessing's name.
    :return: True if the player successfully purchased the blessing, False otherwise.
    """

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

"""
//////////////////
/// PROPERTIES ///
//////////////////
"""


@property
def name(self) -> str:
    return self._name

@name.setter
def name(self, value: str) -> None:
    if value:
        self._name = value
    else:
        raise ValueError("Blessing's name cannot be empty.")

@property
def stat_change_list(self) -> dict:
    return self._stat_change_list

@stat_change_list.setter
def stat_change_list(self, value: dict) -> None:
    for stat in value:
        if stat not in constants.STATKEYS:
            raise ValueError(f"You specified a stat not found in your defined stat names: {stat}")
    self._stat_change_list = value

@property
def essence_cost(self) -> int:
    return self._essence_cost

@essence_cost.setter
def essence_cost(self, value: int) -> None:
    if value < 0:
        raise ValueError("Blessing's essence cost cannot be negative.")
    else:
        self._essence_cost = value
