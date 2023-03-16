def xp_next_lvl_formula(xp_to_next_lvl: int, lvl: int) -> int:
    return round(xp_to_next_lvl * 1.25 + 10 * lvl * lvl / 2)


def money_lost_when_dying(money: int) -> int:
    return money // 2


def normal_attack_dmg(atk_value: int, def_value: int) -> int:
    return round(atk_value * (100 / (100 + def_value * 2.5)))
