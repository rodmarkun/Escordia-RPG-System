class Item:
    """
    Class that represents Items in the game.
    """

    """
    ///////////////////
    /// CONSTRUCTOR ///
    ///////////////////
    """

    def __init__(self, name, description, individual_value, object_type):
        self.name = name
        self.description = description
        self.individual_value = individual_value
        self.object_type = object_type

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
        if not value:
            raise ValueError("Item name cannot be empty")
        self._name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if not value:
            raise ValueError("Item description cannot be empty")
        self._description = value
        
    @property
    def individual_value(self) -> int:
        return self._individual_value
    
    @individual_value.setter
    def individual_value(self, value: int) -> None:
        if value < 0:
            raise ValueError("Item's individual value cannot be negative")
        self._individual_value = value
        
    @property
    def object_type(self) -> str:
        return self._object_type
    
    @object_type.setter
    def object_type(self, value: str) -> None:
        self._object_type = value
