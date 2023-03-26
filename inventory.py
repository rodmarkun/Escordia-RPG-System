import data_management


class Inventory:
    """
    Class that manages the player's inventory
    """

    def __init__(self, player_name):
        self.player_name = player_name
        self.items = {}

    def add_item(self, item, quantity) -> None:
        """
        Adds an item to the inventory.

        :param item: Item's name.
        :param quantity: Quantity to add.
        :return: None
        """
        if item in self.items:
            self.items.update({item: self.items[item] + quantity})
        else:
            self.items.update({item: quantity})

    def remove_item(self, item, quantity) -> bool:
        """
        Removes an item from the inventory.

        :param item: Item's name.
        :param quantity: Quantity to add.
        :return: Boolean, True if was able to remove. False if it was not.
        """
        if item in self.items:
            if self.items[item] == quantity:
                del self.items[item]
                return True
            elif self.items[item] > quantity:
                self.items.update({item: self.items[item] - quantity})
                return True
        return False

    def item_exists(self, item) -> 'Item':
        """
        Checks if an item exists in this inventory and returns its instance.

        :param item: Item to search for.
        :return: Item instance, None if not found.
        """
        if item in self.items:
            return data_management.search_cache_item_by_name(item)
        return None

    def show_inventory(self) -> str:
        """
        Shows player's inventory

        :return: Str containing all item's info
        """
        inventory_str = ""
        for item in self.items:
            i = data_management.search_cache_item_by_name(item)
            inventory_str += f"[x{self.items[item]}] **{i.name}** ({i.object_type})\n"
        return inventory_str
