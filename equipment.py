import constants
from item import Item


class Equipment(Item):

    def __init__(self, name, description, individual_value, object_type, equipment_type, stat_change_list):
        super().__init__(name, description, individual_value, object_type)
        self.equipment_type = equipment_type
        self.stat_change_list = stat_change_list

    def translate_equipment_type(self) -> str:
        """
        Translates the sub-equipment types to equipment types

        :return: String containing the equipment type
        """

        if self.equipment_type in constants.HELM_TYPES:
            return constants.HELMET_KEY
        elif self.equipment_type in constants.ARMOR_TYPES:
            return constants.ARMOR_KEY
        elif self.equipment_type in constants.WEAPON_TYPES:
            return constants.WEAPON_KEY
        else:
            return constants.ACCESSORY_KEY

    def stat_list_formatted(self) -> str:
        """
        Returns a readable, formatted string with the stat changes of this equipment

        :return: Formatted string
        """
        stat_list = []
        for stat in self.stat_change_list:
            if self.stat_change_list[stat] >= 0:
                stat_list.append(f"{stat} +{self.stat_change_list[stat]}")
            else:
                stat_list.append(f"{stat} {self.stat_change_list[stat]}")
        return ', '.join(stat_list)
