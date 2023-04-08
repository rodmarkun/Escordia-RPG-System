import data_management
import os
import discord
import discord_embeds
from discord.ext import commands

import discord_ui
import interface

# Discord token from VENV

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

# Bot initialization
intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.watching, name="!help")
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)
bot.remove_command('help')


@bot.command()
async def start(ctx):
    '''
    !start command
    Creates a new character
    '''
    no_error, msgs = interface.create_player(ctx.author.name)
    if no_error:
        await ctx.send(f'Welcome, {ctx.author.mention}, to the world of Escordia.')
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs}')


@bot.command()
async def fight(ctx):
    '''
    !fight command
    Makes the player fight a random enemy from current area
    '''
    no_error, msgs = interface.begin_battle(ctx.author.name)
    if no_error:
        battle = data_management.search_cache_battle_by_player(ctx.author.name)
        await ctx.send(embed=discord_embeds.embed_fight_msg(ctx, battle.player, battle.enemy), view=discord_ui.ActionMenu(ctx))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs}')


@bot.command()
async def attack(ctx):
    '''
    !attack command
    Attack enemy fighting the player
    '''
    no_error, msgs = interface.normal_attack(ctx.author.name)
    if no_error:
        battle = data_management.search_cache_battle_by_player(ctx.author.name)
        msg_str = msgs_to_msg_str(msgs)
        # Player won the fight
        if battle is None:
            # This is just for it to be prettier
            loot_msg = msgs.pop()
            win_msg = msgs.pop()
            msg_str = msgs_to_msg_str(msgs)
            await ctx.send(msg_str, embed=discord_embeds.embed_victory_msg(ctx, f"{win_msg}\n{loot_msg}"))
        else:
            await ctx.send(msg_str, embed=discord_embeds.embed_fight_msg(ctx, battle.player, battle.enemy), view=discord_ui.ActionMenu(ctx))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs}')


@bot.command()
async def rest(ctx):
    """
    !rest command
    Fully recovers the player
    """
    no_error, msgs = interface.player_rest(ctx.author.name)
    if no_error:
        msg_str = msgs_to_msg_str(msgs)
        await ctx.send(msg_str)
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs}')


@bot.command()
async def inventory(ctx):
    """
    !inventory command
    Shows player's inventory
    """
    no_error, msgs = interface.show_player_inventory(ctx.author.name)
    if no_error:
        await ctx.send(msgs_to_msg_str(msgs))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs}')


@bot.command()
async def profile(ctx):
    """
    !profile command
    Shows player's profile
    """
    no_error, msgs = interface.show_player_profile(ctx.author.name)
    if no_error:
        await ctx.send(embed=discord_embeds.embed_player_profile(ctx, ctx.author.name, msgs_to_msg_str(msgs)))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs}')


@bot.command()
async def shop(ctx):
    """
    !shop command
    Shows the shop of the current area
    """
    no_error, msgs = interface.show_shop_inventory(ctx.author.name)
    if no_error:
        item_list = data_management.search_cache_shop_by_area(data_management.search_cache_player(ctx.author.name).current_area).item_list
        await ctx.send(msgs_to_msg_str(msgs), view=discord_ui.ItemSelectView(ctx, item_list))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs}')


def msgs_to_msg_str(msgs: list) -> str:
    """
    Converts a list of messages to a string

    :param msgs: List of messages
    :return: String containing all messages.
    """
    msg_str = ""
    for msg in msgs:
        msg_str += msg + '\n'
    return msg_str


data_management.load_everything()
bot.run(DISCORD_TOKEN)