
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
        