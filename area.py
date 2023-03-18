import enemy


class Area:
    """
    Stores information about areas in the game.
    """

    """
    ///////////////////
    /// CONSTRUCTOR ///
    ///////////////////
    """

    def __init__(self, name, number, enemy_list, boss, dungeons):
        self._name = name
        self._number = number
        self._enemy_list = enemy_list
        self._boss = boss
        self._dungeons = dungeons

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
            raise ValueError("An area's name cannot be empty")
