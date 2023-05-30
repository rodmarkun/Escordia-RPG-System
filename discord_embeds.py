import discord
import emojis
import formulas

from StringProgressBar import progressBar


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
        title=f'Fight - {ctx.author}',
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
    embed = discord.Embed(
        title=f'Enemy - {enemy.name}',
        description=f'Enemy description goes in here\n\n{enemy.show_enemy_info()}\n**Weaknesses**\n{" ".join([emojis.element_to_emoji[e] for e in enemy.weaknesses])}\n**Resistances**\n{" ".join([emojis.element_to_emoji[e] for e in enemy.resistances])}',
        color=discord.Colour.red()
    )
    embed.set_image(url=enemy.image_url)
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
