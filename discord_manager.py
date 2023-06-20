import random

import constants
import data_management
import os
import discord
import discord_embeds
import discord_ui
import emojis
import info_msgs
import interface

from error_msgs import *
from discord.ext import commands

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
        await ctx.send(f'Welcome, {ctx.author.mention}, to the world of Escordia.\nWe recommend you see the `!tutorial`.')
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


@bot.command()
async def help(ctx):
    '''
    !help command
    Shows all commands
    '''
    await ctx.send(embed=discord_embeds.embed_help_msg(ctx))


@bot.command()
async def tutorial(ctx):
    '''
    !help command
    Shows all commands
    '''
    await ctx.send(f"{ctx.author.mention} - {info_msgs.TUTORIAL_MSG}")


@bot.command()
async def fight(ctx):
    '''
    !fight command
    Makes the player fight a random enemy from current area
    '''
    if constants.TREASURE_CHANCE_WHEN_FIGHTING >= random.randint(0, 100):
        no_error, msgs = interface.receive_treasure(ctx.author.name, constants.NUMBER_OF_ITEMS_IN_TREASURE)
        if no_error:
            await ctx.send(f'While searching the area, {ctx.author.mention} found a treasure!')
            await ctx.send(embed=discord_embeds.embed_treasure_found(ctx, msgs))
        else:
            await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')
    else:
        no_error, msgs = interface.begin_battle(ctx.author.name, False)
        if no_error:
            battle = data_management.search_cache_battle_by_player(ctx.author.name)
            await ctx.send(embed=discord_embeds.embed_fight_msg(ctx, battle.player, battle.enemy), view=discord_ui.ActionMenu(ctx))
        else:
            await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


@bot.command()
async def boss(ctx):
    '''
    !boss command
    Makes the player fight the boss of current area
    '''
    no_error, msgs = interface.begin_battle(ctx.author.name, True)
    if no_error:
        battle = data_management.search_cache_battle_by_player(ctx.author.name)
        await ctx.send(embed=discord_embeds.embed_fight_msg(ctx, battle.player, battle.enemy),
                       view=discord_ui.ActionMenu(ctx))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


@bot.command()
async def attack(ctx):
    '''
    !attack command
    Attack enemy fighting the player
    '''
    no_error, msgs = interface.normal_attack(ctx.author.name)
    await discord_ui.continue_battle(no_error, msgs, ctx)


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
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


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
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


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
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


@bot.command()
async def shop(ctx):
    """
    !shop command
    Shows the shop of the current area
    """
    no_error, msgs = interface.show_shop_inventory(ctx.author.name)
    if no_error:
        item_list = data_management.search_cache_shop_by_area(data_management.search_cache_player(ctx.author.name).current_area).item_list
        await ctx.send(f"Please select an item to buy, {ctx.author.mention}. You currently have **{data_management.search_cache_player(ctx.author.name).money}G**", view=discord_ui.ItemBuySelectView(ctx, item_list))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


@bot.command()
async def equipment(ctx):
    """
    !equipment command
    Shows player's equipment
    """

    player_inst = data_management.search_cache_player(ctx.author.name)
    if player_inst is None:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {ERROR_CHARACTER_DOES_NOT_EXIST}')
        return

    if data_management.search_cache_battle_by_player(ctx.author.name) is not None:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {ERROR_CANNOT_DO_WHILE_IN_FIGHT}')
        return

    await ctx.send(f"This is your current equipment, {ctx.author.mention}:")
    for e_type in constants.EQUIPMENT_TYPES:
        item_list = player_inst.inventory.get_equipment_from_type(e_type)
        if len(item_list) == 0 and player_inst.equipment[e_type] is None:
            await ctx.send(f"**{e_type}**\nYou don't have any.")
        else:
            await ctx.send(f"**{e_type}**", view=discord_ui.EquipmentSelectView(ctx, item_list, player_inst.equipment[e_type]))


@bot.command()
async def job(ctx):
    """
    !job command
    Shows player's job, also allows to change it
    """
    no_error, msgs = interface.show_player_job(ctx.author.name)
    if no_error:
        player_inst = data_management.search_cache_player(ctx.author.name)
        await ctx.send(embed=discord_embeds.embed_current_job(ctx, player_inst.current_job, msgs_to_msg_str(msgs)), view=discord_ui.JobSelectView(ctx, data_management.search_available_jobs_by_player(player_inst.name)))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


@bot.command()
async def skills(ctx):
    """
    !skills command
    Shows player's skills info
    """
    player_inst = data_management.search_cache_player(ctx.author.name)
    if player_inst is None:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {ERROR_CHARACTER_DOES_NOT_EXIST}')
        return

    skill_str = ""
    for s in player_inst.skills:
        skill_inst = data_management.search_cache_skill_by_name(s)
        skill_str += f"**{s}** - {emojis.skill_emoji(skill_inst, player_inst.current_job)}\n_{skill_inst.description}_\nPower: {skill_inst.power} | MP Cost: {skill_inst.mp_cost} | Cooldown: {skill_inst.cooldown}\n\n"

    await ctx.send(f"These are your current skills, {ctx.author.mention}:\n\n{skill_str}")


@bot.command()
async def dungeon(ctx):
    """
    !dungeon command
    Shows all dungeons in current area
    """
    no_error, msgs = interface.show_dungeons(ctx.author.name)
    if no_error:
        dungeon_list = [data_management.search_cache_dungeon_by_name(d) for d in msgs]
        await ctx.send(f"Please select a dungeon, {ctx.author.mention}", view=discord_ui.DungeonSelectView(ctx, dungeon_list))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


def msgs_to_msg_str(msgs: list) -> str:
    """
    Converts a list of messages to a string

    :param msgs: List of messages
    :return: String containing all messages.
    """
    return "\n".join(msgs)


data_management.load_everything()
bot.run(DISCORD_TOKEN)
