import math
import random
import constants


def xp_next_lvl_formula(xp_to_next_lvl: int, lvl: int) -> int:
    """
    Formula for calculating how much XP is needed for next level.

    :param xp_to_next_lvl: Current XP to reach next level.
    :param lvl: Current Player's lvl
    :return: Integer containing XP necessary to reach next level.
    """

    return round(xp_to_next_lvl * 1.25 + 5 * lvl * lvl / 2)


def xp_next_lvl_job_formula(xp_to_next_lvl: int, lvl: int) -> int:
    """
    Formula for calculating how much XP is needed for next job level.

    :param xp_to_next_lvl: Current XP to reach next job level.
    :param lvl: Current Player's job lvl
    :return: Integer containing XP necessary to reach next level.
    """

    return round(xp_to_next_lvl * 1.5 + 5 * lvl * lvl / 2)


def money_lost_when_dying(money: int) -> int:
    """
    Formula for calculating how much money the player loses when dying.

    :param money: Money the player currently has.
    :return: Money the player loses.
    """

    return money // 2


def miss_formula(atk_speed: int, def_speed: int) -> int:
    """
    Formula for calculating the chance of missing an attack.

    :param atk_speed: Attacker's speed.
    :param def_speed: Defender's speed.
    :return: Chance of missing an attack.
    """

    return math.floor(math.sqrt(max(0, (5 * def_speed - atk_speed * 2))))


def check_for_critical_damage(attacker: 'Battler', dmg: int) -> (int, bool):
    """
    Formula for rolling if an attack turns to be critical or not. Depends on attacker's critch.

    :param attacker: Attacking battler.
    :param dmg: Damage the attacking is currently doing.
    :return: New damage after checking for critical hit. Also boolean with result of roll.
    """

    if 'CRITCH' in attacker.stats:
        if random.randint(0, 100) <= attacker.stats['CRITCH']:
            return int(dmg + dmg * attacker.stats['CRITDMG']/100), True  # Apply crit dmg %
    return dmg, False


def normal_attack_dmg(atk_value: int, def_value: int) -> int:
    """
    Formula for calculating the damage.

    :param atk_value: ATK of attacking Battler.
    :param def_value: DEF of defending Battler.
    :return: DMG of normal attack.
    """

    return round(atk_value * (100 / (100 + def_value * 1.5)))


def healing_spell_power(spell_power: int, matk_value: int) -> int:
    """
    Formula for calculating the healing power of a spell.

    :param spell_power: Spell's power.
    :param matk_value: Magic ATK of casting Battler.
    :return:
    """

    return int(spell_power * (100 + matk_value * 1.5)/ 100)


def damage_spell_power(spell_power: int, matk_value: int, mdef_value: int) -> int:
    """
    Formula for calculating the damage power of a spell.

    :param spell_power: Spell's power.
    :param matk_value: Magic ATK of casting Battler.
    :param mdef_value: Magic DEF of defending Battler.
    :return:
    """
    return int(spell_power * matk_value / 10 * (100 / (100 + mdef_value * 1.5)))


def damage_physical_spell(spell_power: int, atk_value: int, def_value: int) -> int:
    """
    Formula for calculating the damage power of a spell.

    :param spell_power: Spell's power.
    :param atk_value: ATK of casting Battler.
    :param def_value: DEF of defending Battler.
    :return:
    """
    return int(spell_power * atk_value / 10 * (100 / (100 + def_value * 1.5)))


def leech_calculation(damage: int) -> int:
    """
    Formula for calculating the heal amount caused by leeching.

    :param damage: Damage dealt.
    :return: Heal amount.
    """

    return round(damage * constants.LEECH_AMOUNT)
