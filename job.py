class Job:
    """
    Class that represents a Job in the game. Players can switch jobs in order to obtain new abilities.
    """

    """
    ///////////////////
    /// CONSTRUCTOR ///
    ///////////////////
    """

    def __init__(self, name: str, description: str, skill_dict: dict, requisites: list,
                 xp_factor: int = 1, preferred_weapons: list = None):
        self.name = name
        self.description = description
        self.skill_dict = skill_dict
        self.requisites = requisites
        self.xp_factor = xp_factor
        self.preferred_weapons = preferred_weapons

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
            raise ValueError(f"Jobs cannot have empty names.")
        self._name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if not value:
            raise ValueError(f"Jobs cannot have empty descriptions.")
        self._description = value

    @property
    def skill_dict(self) -> dict:
        return self._skill_dict

    @skill_dict.setter
    def skill_dict(self, value: dict) -> None:
        self._skill_dict = value
        
    @property
    def xp_factor(self) -> int:
        return self._xp_factor
    
    @xp_factor.setter
    def xp_factor(self, value: int) -> None:
        self._xp_factor = value
