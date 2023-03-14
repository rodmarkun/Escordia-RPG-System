from item import Item


class Equipment(Item):

    def __init__(self, name, description, individual_value, object_type, equipment_type, stat_change_list):
        super().__init__(name, description, individual_value, object_type)
        self.equipment_type = equipment_type
        self.stat_change_list = stat_change_list
