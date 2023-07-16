import constants
import emojis
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

    def __init__(self, name: str, description: str, mp_cost: int, power: int, element: str = None,
                 cooldown: int = 1, tags: list = [], percentage_cost: bool = False):
        self.name = name
        self.description = description
        self.mp_cost = mp_cost
        self.power = power
        self.element = element
        self.cooldown = cooldown
        self.tags = tags
        self.percentage_cost = percentage_cost

    """
    ///////////////
    /// METHODS ///
    ///////////////
    """

    def effect(self, player_name: str, caster: Battler, target: Battler) -> None:
        """
        Applies the effect of the skill to the target.

        :param player_name: Player's name.
        :param caster: Caster of the skill.
        :param target: Target of the skill.
        :return: None.
        """
        # Message
        messager.add_message(player_name, f"{caster.name} casts \"{self.name}\" {emojis.element_to_emoji[self.element] if self.element is not None else get_job_emoji(player_name, caster)}!")
        # Damaging Skills
        if constants.SKILL_TAG_PHYSICAL in self.tags or constants.SKILL_TAG_MAGICAL in self.tags:
            # Done in this way to allow skills that deal both physical and magical damage
            damage = 0
            skill_power = self.power
            if constants.SKILL_TAG_PHYSICAL in self.tags:
                damage += formulas.damage_physical_spell(skill_power, caster.stats[constants.ATK_STATKEY],
                                                  target.stats[constants.DEF_STATKEY])
            if constants.SKILL_TAG_MAGICAL in self.tags:
                if constants.SKILL_TAG_DEBUFF_EXPLOIT in self.tags:
                    skill_power += skill_power//2 * target.get_number_of_debbufs()
                damage += formulas.damage_spell_power(skill_power, caster.stats[constants.MATK_STATKEY],
                                                 target.stats[constants.MDEF_STATKEY])
            if constants.SKILL_TAG_RAINBOW in self.tags:
                damage = target.take_damage(damage, "RAINBOW")
            else:
                damage = target.take_damage(damage, self.element)
            messager.add_message(player_name, f"{target.name} takes {damage} damage!")
            if constants.SKILL_TAG_LEECH in self.tags:
                caster.heal(formulas.leech_calculation(damage))
                messager.add_message(player_name, f"{caster.name} heals himself for {formulas.leech_calculation(damage)} HP!")
        # Healing Skills
        if constants.SKILL_TAG_HEALING in self.tags:
            amount = formulas.healing_spell_power(self.power, caster.stats[constants.MATK_STATKEY])
            if caster.name == target.name:
                messager.add_message(player_name, f"{caster.name} heals himself for {amount} HP!")
            else:
                messager.add_message(player_name, f"{caster.name} heals {target.name} for {amount} HP!")
            target.heal(amount)
        # Recover MP Skills
        if constants.SKILL_TAG_RECOVER_MP in self.tags:
            amount = formulas.healing_spell_power(self.power, caster.stats[constants.MATK_STATKEY])
            messager.add_message(player_name, f"{caster.name} recovers {amount} MP!")
            caster.recover_mp(amount)
        # Shield Skills
        if constants.SKILL_TAG_SHIELD in self.tags:
            amount = int(caster.stats[constants.MAXHP_STATKEY] * self.power / 100)
            caster.shield = amount
            messager.add_message(player_name, f"{caster.name} gains a shield of {amount}!")

        # Buffs and Debuffs
        if constants.SKILL_TAG_INFLICT_BUFF_DEBUFF in self.tags:
            self.buff_debuff_logic(player_name, target)
        if constants.SKILL_TAG_SELF_INFLICT_BUFF_DEBUFF in self.tags:
            self.buff_debuff_logic(player_name, caster)

        if constants.SKILL_TAG_SELF_REMOVE_DEBUFFS in self.tags:
            caster.remove_all_debuffs()
            messager.add_message(player_name, f"{caster.name} has its debuffs removed!")
        if constants.SKILL_TAG_REMOVE_DEBUFFS in self.tags:
            target.remove_all_debuffs()
            messager.add_message(player_name, f"{target.name} has its debuffs removed!")

    def buff_debuff_logic(self, player_name: str, who: Battler):
        buffs_and_debuffs = list(set(constants.BUFFS) & set(self.tags) | set(constants.DEBUFFS) & set(self.tags))
        for bd in buffs_and_debuffs:
            who.add_buff_debuff(bd)
            messager.add_message(player_name,
                                 f"{who.name} stats are altered! {constants.BUFF_DEBUFF_TO_MESSAGE[bd]} {emojis.buff_debuff_to_emoji[bd]}!")

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


def get_job_emoji(player_name: str, caster: Battler) -> str:
    """
    If the caster is the player, returns the emoji of the job of the caster.
    This is for skills that do not have an element.

    :param player_name: Player's name
    :param caster: Caster battler
    :return: Emoji of the job of the caster.
    """
    if player_name == caster.name:
        return emojis.job_to_emoji[caster.current_job]
    else:
        return ''
