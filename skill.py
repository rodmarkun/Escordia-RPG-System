import constants
import formulas
import messager
from battler import Battler


class Skill:
    """
    Class that represents a skill inside the game.
    """

    """
    ///////////////////
    /// CONSTRUCTOR ///
    ///////////////////
    """

    def __init__(self, name: str, description: str, mp_cost: int, type: str, power: int, element: str = None,
                 status_effect: str = None, activation_times: int = 1):
        self.name = name
        self.description = description
        self.mp_cost = mp_cost
        self.type = type
        self.power = power
        self.element = element
        self.status_effect = status_effect
        self.activation_times = activation_times

    """
    ///////////////
    /// METHODS ///
    ///////////////
    """

    def effect(self, player_name: str, caster: Battler, target: Battler):
        if self.type == "DAMAGING_MAGIC":
            messager.add_message(player_name, f"{caster.name} casts {self.name}!")
            for i in range(self.activation_times):
                damage = formulas.damage_spell_power(caster.stats[constants.MATK_STATKEY],
                                                     target.stats[constants.MDEF_STATKEY], self.power)
                target.take_damage(damage)
                messager.add_message(player_name, f"{target.name} takes {damage} damage!")
        elif self.type == "HEALING_MAGIC":
            amount = formulas.healing_spell_power(self.power, caster.stats[constants.MATK_STATKEY])
            if caster.name == target.name:
                messager.add_message(caster.name, f"{caster.name} heals himself for {amount} HP!")
            else:
                messager.add_message(caster.name, f"{caster.name} heals {target.name} for {amount} HP!")
            target.heal(amount)

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
        self._name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def mp_cost(self) -> int:
        return self._mp_cost

    @mp_cost.setter
    def mp_cost(self, value: int) -> None:
        self._mp_cost = value
        
    @property
    def type(self) -> str:
        return self._type
    
    @type.setter
    def type(self, value: str) -> None:
        self._type = value
    
    @property
    def power(self) -> int:
        return self._power
    
    @power.setter
    def power(self, value: int) -> None:
        self._power = value

    @property
    def element(self) -> str:
        return self._element
    
    @element.setter
    def element(self, value: str) -> None:
        self._element = value
        
    @property
    def status_effect(self) -> str:
        return self._status_effect
    
    @status_effect.setter
    def status_effect(self, value: str) -> None:
        self._status_effect = value


# class HealingMagicalSkill(Skill):
#     """
#     Class that represents a healing skill inside the game.
#     """
# 
#     def __init__(self, name: str, description: str, mp_cost: int, heal_power: int, is_percent: bool = False):
#         super().__init__(name, description, mp_cost)
#         self.heal_power = heal_power
#         self.is_percent = is_percent
# 
#     """
#     ///////////////
#     /// METHODS ///
#     ///////////////
#     """
# 
#     def effect(self, caster: Battler, target: Battler) -> None:
#         """
#         Effect of the skill.
# 
#         :param caster: Battler that casted the skill.
#         :param target: Battler that is the target of the skill.
#         :return: None.
#         """
#         # TODO: Change this to a select target
#         target = caster
# 
#         messager.add_message(caster.name, f"{caster.name} casts {self.name}!")
#         if self.is_percent:
#             amount = int(target.stats['MAXHP'] * (self.heal_power / 100))
#         else:
#             amount = formulas.healing_spell_power(self.heal_power, caster.stats['MATK'])
#         if caster.name == target.name:
#             messager.add_message(caster.name, f"{caster.name} heals himself for {amount} HP!")
#         else:
#             messager.add_message(caster.name, f"{caster.name} heals {target.name} for {amount} HP!")
#         target.heal(amount)
# 
#     """
#     //////////////////
#     /// PROPERTIES ///
#     //////////////////
#     """
# 
#     @property
#     def heal_power(self) -> int:
#         return self._heal_amount
# 
#     @heal_power.setter
#     def heal_power(self, value: int) -> None:
#         self._heal_amount = value
# 
#     @property
#     def is_percent(self) -> bool:
#         return self._is_percent
# 
#     @is_percent.setter
#     def is_percent(self, value: bool) -> None:
#         self._is_percent = value
# 
# 
# class DamagingMagicalSkill(Skill):
#     """
#     Class that represents a damaging skill inside the game.
#     """
# 
#     def __init__(self, name: str, description: str, mp_cost: int, damage_power: int, activation_times: int = 1):
#         super().__init__(name, description, mp_cost)
#         self.damage_power = damage_power
#         self.activation_times = activation_times
# 
#     """
#     ///////////////
#     /// METHODS ///
#     ///////////////
#     """
# 
#     def effect(self, caster: Battler, target: Battler) -> None:
#         """
#         Effect of the skill.
# 
#         :param caster: Battler that casted the skill.
#         :param target: Battler that is the target of the skill.
#         :return: None.
#         """
#         messager.add_message(caster.name, f"{caster.name} casts {self.name}!")
#         amount = formulas.damage_spell_power(self.damage_power, caster.stats['MATK'], target.stats['MDEF'])
#         for i in range(self.activation_times):
#             messager.add_message(caster.name, f"{caster.name} deals {amount} damage to {target.name}!")
#             target.take_dmg(amount)
# 
# 
#     """
#     //////////////////
#     /// PROPERTIES ///
#     //////////////////
#     """
# 
#     @property
#     def damage_power(self) -> int:
#         return self._damage_power
# 
#     @damage_power.setter
#     def damage_power(self, value: int) -> None:
#         self._damage_power = value
# 
#     @property
#     def activation_times(self) -> int:
#         return self._activation_times
# 
#     @activation_times.setter
#     def activation_times(self, value: int) -> None:
#         self._activation_times = value
