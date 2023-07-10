import discord

import data_management
import emojis
import formulas

from StringProgressBar import progressBar

import info_msgs


def embed_help_msg(ctx):
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

def embed_fight_msg(ctx, player_obj, enemy):
    '''
    Sends embed used while fighting

    :param ctx: Discord CTX
    :param enemy: Enemy object
    :param player_obj: Player object
    '''
    # Progress bars for HP and MP
    hp_bar = progressBar.filledBar(enemy.stats['MAXHP'], enemy.stats['HP'], size=10)
    player_hp_bar = progressBar.filledBar(player_obj.stats['MAXHP'], player_obj.stats['HP'], size=10)
    player_mp_bar = progressBar.filledBar(player_obj.stats['MAXMP'], player_obj.stats['MP'], size=10)

    embed = discord.Embed(
        # General info
        title=f'Fight - {ctx.author.name.capitalize()}',
        description=f'You are fighting a **{enemy.name}**.\n'
                    f'HP: {hp_bar[0]} - {enemy.stats["HP"]}/{enemy.stats["MAXHP"]}',
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

    if len(enemy.buffs_and_debuffs.keys()) > 0:
        embed.add_field(name="Enemy alterations:", value=" ".join([emojis.buff_debuff_to_emoji[bd] for bd in enemy.buffs_and_debuffs]), inline=True)
    if len(player_obj.buffs_and_debuffs.keys()) > 0:
        embed.add_field(name=f"Your alterations:", value=" ".join([emojis.buff_debuff_to_emoji[bd] for bd in player_obj.buffs_and_debuffs]), inline=True)

    # Player stats
    embed.set_footer(
        text=f'{player_obj.name}\nHP: {player_obj.stats["HP"]}/{player_obj.stats["MAXHP"]} | {player_hp_bar[0]}\nMP: '
             f'{player_obj.stats["MP"]}/{player_obj.stats["MAXMP"]} | {player_mp_bar[0]}\nHit chance: '
             f'{100 - formulas.miss_formula(player_obj.stats["SPEED"], enemy.stats["SPEED"])}% | Critical chance: '
             f'{player_obj.stats["CRITCH"]}%')
    return embed


def embed_victory_msg(ctx, msg: str):
    '''
    Sends an embed when victorious in combat

    :param ctx: Discord CTX
    :param msg: Victory message
    '''
    embed = discord.Embed(
        title=f'{emojis.SPARKLER_EMOJI} Victory! {emojis.SPARKLER_EMOJI}',
        description=msg,
        color=discord.Colour.red()
    )
    embed.set_image(url=ctx.author.avatar.url)
    return embed


def embed_death_msg(ctx):
    '''
    Sends an embed when player dies

    :param ctx: Discord CTX
    '''
    embed = discord.Embed(
        title=f'{emojis.SKULL_EMOJI} Death {emojis.SKULL_EMOJI}',
        description='You have died.',
        color=discord.Colour.red()
    )
    embed.set_image(url=ctx.author.avatar.url)
    return embed


def embed_enemy_info(ctx, enemy: 'Enemy') -> discord.Embed:
    """
    Sends an embed with enemy info

    :param ctx: Discord's CTX
    :param enemy: Enemy instance
    :return:
    """
    bd_str = ''
    if len(enemy.buffs_and_debuffs) > 0:
        bd_str = f"\n**Alterations**\n{' '.join([emojis.buff_debuff_to_emoji[bd] for bd in enemy.buffs_and_debuffs])}\n\n"
    enemy_skills_str = '\n'.join([f'- **{s}** {emojis.element_to_emoji[data_management.search_cache_skill_by_name(s).element]}' for s in enemy.skills])
    embed = discord.Embed(
        title=f'Enemy - {enemy.name}',
        description=f'_{enemy.description}_\n\n{enemy.show_enemy_info()}\n{bd_str}'
                    f'**Weaknesses**\n{" ".join([emojis.element_to_emoji[e] for e in enemy.weaknesses])}\n'
                    f'**Resistances**\n{" ".join([emojis.element_to_emoji[e] for e in enemy.resistances])}\n'
                    f'**Skills**\n{enemy_skills_str}',
        color=discord.Colour.red()
    )
    embed.set_image(url=enemy.image_url)
    return embed


def embed_player_profile(ctx, player_name: str, player_inst: 'Player', job_inst: 'Job') -> discord.Embed:
    """
    Embed for whenever the player checks their profile.

    :param player_name: Player's name
    :param msgs: Message to be displayed containing the player's profile info
    :param ctx: Discord's CTX
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


def embed_treasure_found(ctx, item_list: list) -> discord.Embed:
    """
    Embed for whenever the player finds treasure.

    :param ctx: Discord's CTX
    :param item_list: List of item names found
    """
    embed = discord.Embed(
        title=f'{emojis.ESC_CHEST_ICON} Treasure found! {emojis.ESC_CHEST_ICON}',
        description=f'You found:\n\n' + '\n'.join([f'- {item} {emojis.obj_emoji(data_management.search_cache_item_by_name(item))}' for item in item_list]),
        color=discord.Colour.red()
    )
    return embed


def embed_current_job(ctx, job: str, msgs: str) -> discord.Embed:
    """
    Embed for whenever the player checks their current job.

    :param ctx: Discord's CTX
    :param msgs: Message to be displayed containing the player's current job info
    :param job: Job name
    :return: Embed
    """
    job_inst = data_management.search_cache_job_by_name(job)
    job_reqs_str = ""
    for job in data_management.search_all_jobs():
        other_job_reqs_list = []
        for other_job in job.requisites:
            other_job_reqs_list.append(f"{other_job} - lvl {job.requisites[other_job]}")
        if len(other_job_reqs_list) == 0:
            str_displayed = "None"
        else:
            str_displayed = ", ".join(other_job_reqs_list)
        job_reqs_str += f"- {job.name} {emojis.job_to_emoji[job.name]}: Requires {str_displayed}\n"

    embed = discord.Embed(
        title=f"{job_inst.name} - {emojis.job_to_emoji[job_inst.name]}",
        description=f'{msgs}\n' \
                    f'--- Job Requirements ---\n' \
                    f'{job_reqs_str}\n',
        color=discord.Colour.red()
    )
    return embed
