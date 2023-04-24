import discord
from StringProgressBar import progressBar

import emojis
import formulas
import messager


def embed_fight_msg(ctx, player_obj, enemy):
    '''
    Sends embed used while fighting

    :param ctx: Discord CTX
    :param enemy: Enemy object
    :param player_obj: Player object
    '''
    hp_bar = progressBar.filledBar(enemy.stats['MAXHP'], enemy.stats['HP'], size=10)
    player_hp_bar = progressBar.filledBar(player_obj.stats['MAXHP'], player_obj.stats['HP'], size=10)
    player_mp_bar = progressBar.filledBar(player_obj.stats['MAXMP'], player_obj.stats['MP'], size=10)
    embed = discord.Embed(
        title=f'Fight - {ctx.author}',
        description=f'You are fighting a **{enemy.name}**.\n'
                    f'HP: {hp_bar[0]} - {enemy.stats["HP"]}/{enemy.stats["MAXHP"]}\n'
                    f'Weak to: {" ".join([emojis.element_to_emoji[e] for e in enemy.weaknesses])}\n'
                    f'Resists: {" ".join([emojis.element_to_emoji[e] for e in enemy.resistances])}\n'
                    f'What will you do?\n\n',
        color=discord.Colour.red()
    )
    embed.set_thumbnail(url=enemy.image_url)
    embed.set_image(url=ctx.author.avatar.url)
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


def embed_death_msg(ctx, msg: str):
    '''
    Sends an embed when victorious in combat

    :param ctx: Discord CTX
    :param msg: Victory message
    '''
    embed = discord.Embed(
        title=f'{emojis.SKULL_EMOJI} Death {emojis.SKULL_EMOJI}',
        description='You have died.',
        color=discord.Colour.red()
    )
    embed.set_image(url=ctx.author.avatar.url)
    return embed


def embed_player_profile(ctx, player_name: str, msgs: str) -> discord.Embed:
    """
    Embed for whenever the player checks their profile.

    :param ctx: Discord's CTX
    :return: Embed
    """
    embed = discord.Embed(
        title=f'Profile - {player_name}',
        description=msgs,
        color=discord.Colour.red()
    )
    embed.set_image(url=ctx.author.avatar.url)
    return embed
