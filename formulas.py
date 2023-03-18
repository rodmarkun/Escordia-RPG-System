def xp_next_lvl_formula(xp_to_next_lvl: int, lvl: int) -> int:
    """
    Formula for calculating how much XP is needed for next level.

    :param xp_to_next_lvl: Current XP to reach next level.
    :param lvl: Current Player's lvl
    :return: Integer containing XP necessary to reach next level.
    """

    return round(xp_to_next_lvl * 1.25 + 10 * lvl * lvl / 2)


def money_lost_when_dying(money: int) -> int:
    """
    Formula for calculating how much money the player loses when dying.

    :param money: Money the player currently has.
    :return: Money the player loses.
    """

    return money // 2


def normal_attack_dmg(atk_value: int, def_value: int) -> int:
    """
    Formula for calculating the damage.

    :param atk_value: ATK of attacking Battler.
    :param def_value: DEF of defending Battler.
    :return: DMG of normal attack.
    """

    return round(atk_value * (100 / (100 + def_value * 2.5)))
