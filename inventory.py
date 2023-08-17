import constants
import data_management
import emojis
import messager


class Inventory:
    """
    Class that manages the player's inventory
    """

    def __init__(self, player_name, *, items: dict = {}):
        self.player_name = player_name
        self.items = items

    def add_item(self, item, quantity) -> None:
        """
        Adds X quantity of an item to the inventory.

        :param item: Item's name.
        :param quantity: Quantity to add.
        :return: None
        """

        if item in self.items:
            self.items.update({item: self.items[item] + quantity})
        else:
            if self.has_space_available():
                self.items.update({item: quantity})

    def destroy_item_for_essence(self, item: str):
        """
        Destroys an item for essence.

        :param item:
        :return: Essence amount and quantity of items destroyed
        """

        i = data_management.search_cache_item_by_name(item)
        quantity = self.items[item]
        self.remove_item(item, quantity)
        messager.add_message(self.player_name, f"You destroyed {quantity} {i.name} for {int(i.individual_value // 2 * quantity)} {emojis.ESC_ESSENCE_ICON}")
        return int(i.individual_value // 2 * quantity), quantity


    def has_space_available(self) -> bool:
        """
        Checks if the inventory has space available.

        :return: Boolean, True if has space available. False if it does not.
        """

        return len(self.items) < constants.MAX_INVENTORY_SLOTS

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

    def item_exists(self, item: str) -> 'Item':
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

        inventory_str = f"[{len(self.items)}/{constants.MAX_INVENTORY_SLOTS}]\n\n"
        if len(self.items) == 0:
            return "You have no items in your inventory."
        for item in self.items:
            i = data_management.search_cache_item_by_name(item)
            inventory_str += f"x{self.items[item]} **{i.name}** {emojis.obj_emoji(i)}\n"
        return inventory_str

    def get_equipment_from_type(self, item_type: str) -> list:
        """
        Returns a list of equipment from a certain type.

        :param item_type: Item type.
        :return: List with items.
        """

        items = []
        for item in self.items:
            i = data_management.search_cache_item_by_name(item)
            if i.object_type == "EQUIPMENT" and equipment_equivalences(item_type, i):
                items.append(i)
        return items


def equipment_equivalences(equipment_type: str, equipment: 'Equipment') -> bool:
    """
    Checks if a certain item has a type equivalent to the specified (ex: ARMOR is equivalent to HEAVY_ARMOR)

    :param equipment_type: Equipment to compare
    :return: True if equivalent, False if not
    """

    if equipment_type == "ARMOR" and equipment.equipment_type in constants.ARMOR_TYPES:
        return True
    elif equipment_type == "WEAPON" and equipment.equipment_type in constants.WEAPON_TYPES:
        return True
    elif equipment_type == "HELMET" and equipment.equipment_type in constants.HELM_TYPES:
        return True
    elif equipment_type == "ACCESSORY" and equipment.equipment_type == "ACCESSORY":
        return True
    return False
