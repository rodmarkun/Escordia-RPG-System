import data_management
import messager
import player

class Shop:
    """
    Class that represents a shop in the game. Players can buy and sell items in here.
    """
    
    """
    ///////////////////
    /// CONSTRUCTOR ///
    ///////////////////
    """
    
    def __init__(self, area_number: int, item_list: list):
        self.area_number = area_number
        self.item_list = item_list

    """
    ///////////////
    /// METHODS ///
    ///////////////
    """

    def show_items(self) -> str:
        """
        Shows shop's items

        :return: String with all items available in the shop.
        """

        shop_str = ""
        for item in self.item_list:
            i = data_management.search_cache_item_by_name(item)
            shop_str += f"**{i.name}** ({i.object_type} - {i.individual_value})\n"
        return shop_str

    """
    //////////////////
    /// PROPERTIES ///
    //////////////////
    """
    
    @property
    def area_number(self) -> int:
        return self._area_number
    
    @area_number.setter
    def area_number(self, value: int) -> None:
        self._area_number = value
    
    @property
    def item_list(self) -> list:
        return self._item_list
    
    @item_list.setter
    def item_list(self, value: list) -> None:
        self._item_list = value

"""
///////////////////
/// AUX METHODS ///
///////////////////
"""
def buy_item(player: player.Player, item_name: str) -> bool:
    """
    Certain player buys an item.

    :param player: Player which buys the item.
    :param item_name: Item's name.
    :return: True if player was able to buy the item. False if they did not have enough money.
    """

    item = data_management.search_cache_item_by_name(item_name)
    if item.individual_value > player.money:
        messager.add_message(player.name, f"{player.name} you do not have enough money to buy a {item.name}.")
        return False
    player.money -= item.individual_value
    player.inventory.add_item(item.name, 1)
    messager.add_message(player.name, f"You successfully purchased a {item.name}.")
    return True
