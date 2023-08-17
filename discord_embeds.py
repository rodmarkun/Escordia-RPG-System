import discord
import data_management
import emojis
import formulas
import enemy
import player
import job
import info_msgs

from StringProgressBar import progressBar


def embed_help_msg(ctx) -> discord.Embed:
    """
    Sends embed used for !help command

    :param ctx: Discord CTX
    :return: Embed
    """
    embed = discord.Embed(
        # General info
        title=f'Escordia Help',
        description=f'{info_msgs.HELP_MSG}',
        color=discord.Colour.red()
    )
    return embed

def embed_fight_msg(ctx, player_obj, enemy) -> discord.Embed:
    """
    Sends embed used while fighting

    :param ctx: Discord CTX
    :param player_obj: Player object
    :param enemy: Enemy object
    :return: Embed
    """

    # Progress bars for HP and MP
    hp_bar = progressBar.filledBar(enemy.stats['MAXHP'], enemy.stats['HP'], size=10)
    player_hp_bar = progressBar.filledBar(player_obj.stats['MAXHP'], player_obj.stats['HP'], size=10)
    player_mp_bar = progressBar.filledBar(player_obj.stats['MAXMP'], player_obj.stats['MP'], size=10)
    # Shields
    player_shield = f"SHIELD: {player_obj.shield}{emojis.SHIELD_EMOJI}\n"
    enemy_shield = f"SHIELD: {enemy.shield}{emojis.SHIELD_EMOJI}\n"

    embed = discord.Embed(
        # General info
        title=f'Fight - {ctx.author.name.capitalize()}',
        description=f'You are fighting a **{enemy.name}**.\n'
                    f'{enemy_shield if enemy.shield > 0 else ""}HP: {hp_bar[0]} - {enemy.stats["HP"]}/{enemy.stats["MAXHP"]}',
        color=discord.Colour.red()
    )
    # Images
    embed.set_thumbnail(url=enemy.image_url)
    embed.set_image(url=ctx.author.avatar.url)

    """
    # Weaknesses, resistances, and buffs/debuffs
    embed.add_field(name="Weak to:", value=" ".join([emojis.element_to_emoji[e] for e in enemy.weaknesses]), inline=True)
    embed.add_field(name="Resists:", value=" ".join([emojis.element_to_emoji[e] for e in enemy.resistances]), inline=True)
    """

    # Buffs and debuffs
    if len(enemy.buffs_and_debuffs.keys()) > 0:
        embed.add_field(name="Enemy alterations:", value=" ".join([emojis.buff_debuff_to_emoji[bd] for bd in enemy.buffs_and_debuffs]), inline=True)
    if len(player_obj.buffs_and_debuffs.keys()) > 0:
        embed.add_field(name=f"Your alterations:", value=" ".join([emojis.buff_debuff_to_emoji[bd] for bd in player_obj.buffs_and_debuffs]), inline=True)

    # Player stats
    embed.set_footer(
        text=f'{player_obj.name}\n{player_shield if player_obj.shield > 0 else ""}HP: {player_obj.stats["HP"]}/{player_obj.stats["MAXHP"]} | {player_hp_bar[0]}\nMP: '
             f'{player_obj.stats["MP"]}/{player_obj.stats["MAXMP"]} | {player_mp_bar[0]}\nHit chance: '
             f'{100 - formulas.miss_formula(player_obj.stats["SPEED"], enemy.stats["SPEED"])}% | Critical chance: '
             f'{player_obj.stats["CRITCH"]}%')

    return embed


def embed_victory_msg(ctx, msg: str) -> discord.Embed:
    """
    Sends an embed when victorious in combat

    :param ctx: Discord CTX
    :param msg: Victory message
    :return: Embed
    """

    embed = discord.Embed(
        title=f'{emojis.SPARKLER_EMOJI} Victory! {emojis.SPARKLER_EMOJI}',
        description=msg,
        color=discord.Colour.red()
    )
    embed.set_image(url=ctx.author.avatar.url)

    return embed


def embed_death_msg(ctx) -> discord.Embed:
    """
    Sends an embed when player dies

    :param ctx: Discord CTX
    :return: Embed
    """
    embed = discord.Embed(
        title=f'{emojis.SKULL_EMOJI} Death {emojis.SKULL_EMOJI}',
        description='You have died.',
        color=discord.Colour.red()
    )
    embed.set_image(url=ctx.author.avatar.url)

    return embed


def embed_duel_msg(ctx, enemy_name: str) -> discord.Embed:
    """
    Sends an embed when player is dueled by another

    :param ctx: Discord CTX
    :param enemy_name: Enemy name
    :return: Embed
    """

    embed = discord.Embed(
        title=f'{emojis.CROSSED_SWORDS_EMOJI} Duel {emojis.CROSSED_SWORDS_EMOJI}',
        description=f'@{enemy_name}, {ctx.author.name.capitalize()} has challenged you to a duel! To decide who goes first, a coin will be flipped. Choose **heads** or **tails**.',
        color=discord.Colour.red()
    )
    embed.set_thumbnail(url=ctx.author.avatar.url)

    return embed


def embed_enemy_info(ctx, enemy_inst: enemy.Enemy) -> discord.Embed:
    """
    Sends an embed with enemy info

    :param ctx: Discord's CTX
    :param enemy_inst: Enemy instance
    :return: Embed
    """

    # Enemy Alterations
    bd_str = ''
    if len(enemy_inst.buffs_and_debuffs) > 0:
        bd_str = f"\n**Alterations**\n{' '.join([emojis.buff_debuff_to_emoji[bd] for bd in enemy_inst.buffs_and_debuffs])}\n\n"

    # Enemy Skills
    enemy_skills_str = "\n"
    for s in enemy_inst.skills:
        skill_inst = data_management.search_cache_skill_by_name(s)
        if skill_inst is not None:
            enemy_skills_str += f"- **{s}** - {emojis.skill_emoji(skill_inst, None)}\n_{skill_inst.description}_\nPower: {skill_inst.power} | MP Cost: {skill_inst.mp_cost}{'%' if skill_inst.percentage_cost else ''} | Cooldown: {skill_inst.cooldown}\n\n"

    # Enemy Loot
    if enemy_inst.possible_loot is None:
        loot_str = 'None'
    else:
        loot_str = f'{enemy_inst.possible_loot} {emojis.obj_emoji(data_management.search_cache_item_by_name(enemy_inst.possible_loot))} - {enemy_inst.loot_chance}%'

    embed = discord.Embed(
        title=f'Enemy - {enemy_inst.name}',
        description=f'_{enemy_inst.description}_\n\n{enemy_inst.show_enemy_info()}\n{bd_str}'
                    f'**Weaknesses**\n{" ".join([emojis.element_to_emoji[e] for e in enemy_inst.weaknesses])}\n'
                    f'**Resistances**\n{" ".join([emojis.element_to_emoji[e] for e in enemy_inst.resistances])}\n'
                    f'**Possible Loot**\n{loot_str}\n'
                    f'**\nSkills**{enemy_skills_str}',
        color=discord.Colour.red()
    )
    embed.set_image(url=enemy_inst.image_url)

    return embed


def embed_player_profile(ctx, player_name: str, player_inst: player.Player, job_inst: job.Job) -> discord.Embed:
    """
    Embed for whenever the player checks their profile.

    :param ctx: Discord's CTX
    :param player_name: Player's name
    :param player_inst: Player's instance
    :param job_inst: Player's job instance
    :return: Embed
    """

    embed = discord.Embed(
        title=f'Profile - {player_name.capitalize()}',
        description=player_inst.show_player_info(),
        color=discord.Colour.red()
    )

    embed.add_field(name='Job',
                    value=f"{job_inst.name} {emojis.job_to_emoji[job_inst.name]}\n" + player_inst.show_player_info_job(
                        False) + player_inst.show_current_skills_as_list(), inline=True)
    embed.add_field(name='Stats', value=player_inst.show_player_stats(), inline=True)
    embed.add_field(name='Inventory', value=f'{player_inst.inventory.show_inventory()}', inline=True)
    embed.add_field(name='Currencies',
                    value=f'{player_inst.money} {emojis.ESC_GOLD_ICON}  {player_inst.essence} {emojis.ESC_ESSENCE_ICON}',
                    inline=True)
    embed.set_thumbnail(url=ctx.author.avatar.url)

    return embed


def embed_skills_info(ctx, player_name: str, skills_str: str) -> discord.Embed:
    """
    Embed for whenever the player checks their profile.

    :param ctx: Discord's CTX
    :param player_name: Player's name
    :param skills_str: Player's skills
    :return: Embed
    """

    embed = discord.Embed(
        title=f'{emojis.SPARKLER_EMOJI} Skills - {player_name.capitalize()}',
        description=skills_str,
        color=discord.Colour.red()
    )
    embed.set_thumbnail(url=ctx.author.avatar.url)

    return embed


def embed_treasure_found(ctx, item_list: list) -> discord.Embed:
    """
    Embed for whenever the player finds treasure.

    :param ctx: Discord's CTX
    :param item_list: List of item names found
    :return: Embed
    """

    embed = discord.Embed(
        title=f'{emojis.ESC_CHEST_ICON} Treasure found! {emojis.ESC_CHEST_ICON}',
        description=f'You found:\n\n' + '\n'.join([f'- {item} {emojis.obj_emoji(data_management.search_cache_item_by_name(item))}' for item in item_list]),
        color=discord.Colour.red()
    )

    return embed


def embed_current_job(ctx, job_name: str, msgs: str) -> discord.Embed:
    """
    Embed for whenever the player checks their current job.

    :param ctx: Discord's CTX
    :param job_name: Job name
    :param msgs: Message to be displayed containing the player's current job info
    :return: Embed
    """

    job_inst = data_management.search_cache_job_by_name(job_name)
    job_reqs_str = ""
    for job_name in data_management.search_all_jobs():
        other_job_reqs_list = []
        for other_job in job_name.requisites:
            other_job_reqs_list.append(f"{other_job} - lvl {job_name.requisites[other_job]}")
        if len(other_job_reqs_list) == 0:
            str_displayed = "None"
        else:
            str_displayed = ", ".join(other_job_reqs_list)
        job_reqs_str += f"- {job_name.name} {emojis.job_to_emoji[job_name.name]}: Requires {str_displayed}\n"

    embed = discord.Embed(
        title=f"{job_inst.name} - {emojis.job_to_emoji[job_inst.name]}",
        description=f'{msgs}\n' \
                    f'--- Job Requirements ---\n' \
                    f'{job_reqs_str}\n',
        color=discord.Colour.red()
    )

    return embed
