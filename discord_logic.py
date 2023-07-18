import constants
import random

import discord_embeds
import discord_ui
import emojis
import info_msgs
import interface
import data_management
import messager
from error_msgs import *


async def create_character(ctx):
    """
    Creates a new character for the player.
    :param ctx: Discord CTX
    :return: None
    """
    no_error, msgs = interface.create_player(ctx.author.name)
    if no_error:
        await ctx.send(
            f'Welcome, {ctx.author.mention}, to the world of Escordia.\nWe recommend you see the `!tutorial`.')
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def begin_fight(ctx, action_menu_ui):
    """
    Begins a fight for the player.
    :param ctx: Discord CTX
    :param action_menu_ui: UI View for the action menu
    :return: None
    """
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
            await ctx.send(embed=discord_embeds.embed_fight_msg(ctx, battle.player, battle.enemy),
                           view=action_menu_ui)
        else:
            await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def begin_pvp_fight(ctx, action_menu_ui, duel_starter_player, dueled_player, coin_choice):
    """
    Begins a PvP fight between two players.

    :param ctx: Discord CTX
    :param action_menu_ui: UI View for the action menu
    :param duel_starter_player: Player who started the duel
    :param dueled_player: Player who was dueled
    :param coin_choice: Coin choice of the player who was dueled
    :return:
    """
    result = random.choice(["HEADS", "TAILS"])
    if result == coin_choice:
        pass
    else:
        pass

async def begin_boss_fight(ctx, action_menu_ui):
    """
    Begins a boss fight for the player.
    :param ctx: Discord CTX
    :param action_menu_ui: UI View for the action menu
    :return: None
    """
    no_error, msgs = interface.begin_battle(ctx.author.name, True)
    if no_error:
        battle = data_management.search_cache_battle_by_player(ctx.author.name)
        await ctx.send(embed=discord_embeds.embed_fight_msg(ctx, battle.player, battle.enemy),
                       view=action_menu_ui)
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def attack(ctx):
    no_error, msgs = interface.normal_attack(ctx.author.name)
    await continue_battle(no_error, msgs, ctx, discord_ui.ActionMenu(ctx))


async def rest(ctx):
    no_error, msgs = interface.player_rest(ctx.author.name)
    if no_error:
        msg_str = msgs_to_msg_str(msgs)
        await ctx.send(msg_str)
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def inventory(ctx):
    no_error, msgs = interface.show_player_inventory(ctx.author.name)
    if no_error:
        await ctx.send(msgs_to_msg_str(msgs))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def shop(ctx):
    no_error, msgs = interface.show_shop_inventory(ctx.author.name)
    if no_error:
        item_list = data_management.search_cache_shop_by_area(
            data_management.search_cache_player(ctx.author.name).current_area).item_list
        await ctx.send(
            f"Please select an item to buy, {ctx.author.mention}. You currently have **{data_management.search_cache_player(ctx.author.name).money}** {emojis.ESC_GOLD_ICON}",
            view=discord_ui.ItemBuySelectView(ctx, item_list))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def equipment(ctx):
    player_inst = data_management.search_cache_player(ctx.author.name)
    if player_inst is None:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {ERROR_CHARACTER_DOES_NOT_EXIST}')
        return

    if data_management.search_cache_battle_by_player(ctx.author.name) is not None:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {ERROR_CANNOT_DO_WHILE_IN_FIGHT}')
        return

    await ctx.send(f"{emojis.MAGE_EMOJI} This is your current equipment, {ctx.author.mention}:")
    for e_type in constants.EQUIPMENT_TYPES:
        item_list = player_inst.inventory.get_equipment_from_type(e_type)
        if len(item_list) == 0 and player_inst.equipment[e_type] is None:
            await ctx.send(f"**{e_type}**\nYou don't have any.")
        else:
            await ctx.send(f"**{e_type}**",
                           view=discord_ui.EquipmentSelectView(ctx, item_list, player_inst.equipment[e_type]))


async def essence(ctx):
    no_error, msgs = interface.essence_crafting(ctx.author.name)
    if no_error:
        player_inst = data_management.search_cache_player(ctx.author.name)
        if len(player_inst.inventory.items) == 0:
            await ctx.send(f"{ctx.author.mention} {info_msgs.ESSENCE_MSG}\nYou currently have no items to destroy.")
        else:
            await ctx.send(
            f"{ctx.author.mention} {info_msgs.ESSENCE_MSG}",
            view=discord_ui.ItemDestroySelectView(ctx, player_inst.inventory.items))
        await ctx.send(f"{ctx.author.mention} You currently have **{player_inst.essence}** {emojis.ESC_ESSENCE_ICON}.", view=discord_ui.BlessingBuySelectView(ctx, player_inst.blessings))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def area(ctx):
    no_error, msgs = interface.show_area(ctx.author.name)
    if no_error:
        player_inst = data_management.search_cache_player(ctx.author.name)
        await ctx.send(msgs_to_msg_str(msgs), view=discord_ui.AreaSelectView(ctx, player_inst))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def profile(ctx, player_menu_ui):
    no_error, msgs = interface.show_player_profile(ctx.author.name)
    if no_error:
        player_inst = data_management.search_cache_player(ctx.author.name)
        job_inst = data_management.search_cache_job_by_name(player_inst.current_job)
        await ctx.send(embed=discord_embeds.embed_player_profile(ctx, ctx.author.name, player_inst, job_inst), view=player_menu_ui)
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def job(ctx):
    no_error, msgs = interface.show_player_job(ctx.author.name)
    if no_error:
        player_inst = data_management.search_cache_player(ctx.author.name)
        await ctx.send(embed=discord_embeds.embed_current_job(ctx, player_inst.current_job, msgs_to_msg_str(msgs)),
                       view=discord_ui.JobSelectView(ctx,
                                                     data_management.search_available_jobs_by_player(player_inst.name), player_inst))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def show_skills(ctx):
    player_inst = data_management.search_cache_player(ctx.author.name)
    if player_inst is None:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {ERROR_CHARACTER_DOES_NOT_EXIST}')
        return

    skill_str = ""
    for s in player_inst.skills:
        skill_inst = data_management.search_cache_skill_by_name(s)
        if skill_inst is not None:
            skill_str += f"**{s}** - {emojis.skill_emoji(skill_inst, player_inst.current_job)}\n_{skill_inst.description}_\nPower: {skill_inst.power} | MP Cost: {skill_inst.mp_cost}{'%' if skill_inst.percentage_cost else ''} | Cooldown: {skill_inst.cooldown}\n\n"

    await ctx.send(embed=discord_embeds.embed_skills_info(ctx, player_inst.name, skill_str))


async def dungeon(ctx):
    no_error, msgs = interface.show_dungeons(ctx.author.name)
    if no_error:
        dungeon_list = [data_management.search_cache_dungeon_by_name(d) for d in msgs]
        await ctx.send(f"Please select a dungeon, {ctx.author.mention}",
                       view=discord_ui.DungeonSelectView(ctx, dungeon_list))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def duel(ctx, enemy_name: str):
    no_error, msgs = interface.duel_check(ctx.author.name, enemy_name)
    if no_error:
        await ctx.send(embed=discord_embeds.embed_duel_msg(ctx, enemy_name), view=discord_ui.DuelSelectView(ctx, battle))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def continue_battle(no_error: bool, msgs: list, ctx, action_menu_ui) -> None:
    if no_error:
        battle = data_management.search_cache_battle_by_player(ctx.author.name)
        msg_str = msgs_to_msg_str(msgs)
        if battle.is_over:
            msg_str = msgs_to_msg_str(msgs)
            await ctx.send(msg_str)
            if battle.player.alive:
                loot = battle.win_battle()
                await ctx.send('', embed=discord_embeds.embed_victory_msg(ctx, msgs_to_msg_str(
                    messager.empty_queue(ctx.author.name))))
                if loot != '':
                    await ctx.send(embed=discord_embeds.embed_treasure_found(ctx, [loot]))
                if battle.player.in_dungeon:
                    await traverse_dungeon(battle, ctx)
                else:
                    await profile(ctx, discord_ui.PlayerMenu(ctx))
            else:
                battle.lose_battle()
                await ctx.send('', embed=discord_embeds.embed_death_msg(ctx))
                await profile(ctx, discord_ui.PlayerMenu(ctx))
        else:
            await ctx.send(msg_str, embed=discord_embeds.embed_fight_msg(ctx, battle.player, battle.enemy),
                                    view=action_menu_ui)
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs}')

async def manage_battle(no_error: bool, ctx, msgs: list, action_menu_ui):
    """
    Manages a battle after starting it.
    :param no_error: Whether there was an error or not
    :param ctx: Discord CTX
    :param msgs: List of info messages.
    :return: None.
    """
    if no_error:
        battle = data_management.search_cache_battle_by_player(ctx.author.name)
        await ctx.send(
            embed=discord_embeds.embed_fight_msg(ctx, battle.player, battle.enemy),
            view=action_menu_ui)
    else:
        await ctx.send(
            f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def traverse_dungeon(battle, ctx):
    dungeon_inst = data_management.search_cache_dungeon_inst_by_player(battle.player.name)
    if dungeon_inst.boss_defeated:
        # Receive rewards
        no_error, msgs = interface.receive_treasure(ctx.author.name, random.randint(2, 3))
        battle.player.in_dungeon = False
        if no_error:
            await ctx.send(embed=discord_embeds.embed_treasure_found(ctx, msgs))
            await profile(ctx, discord_ui.PlayerMenu(ctx))
        else:
            await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')
        data_management.delete_cache_dungeon_inst(battle.player.name)
        data_management.update_player_info(battle.player.name)
    else:
        if dungeon_inst.current_enemies_defeated != dungeon_inst.enemy_count:
            no_error, msgs = interface.begin_battle(ctx.author.name, False,
                                                    enemy=random.choice(dungeon_inst.enemy_list))
            await manage_battle(no_error, ctx, msgs, discord_ui.ActionMenu(ctx))
        else:
            no_error, msgs = interface.begin_battle(ctx.author.name, False,
                                                    enemy=dungeon_inst.boss)
            await manage_battle(no_error, ctx, msgs, discord_ui.ActionMenu(ctx))


def msgs_to_msg_str(msgs: list) -> str:
    """
    Converts a list of messages to a string

    :param msgs: List of messages
    :return: String containing all messages.
    """
    return "\n".join(msgs)


def return_jobs_curr_lvl_dict(job_dictionary, job_name):
    """
    Returns the current level of a job from a dictionary.
    This is not clean, but whatever.

    :param job_dictionary:
    :param job_name:
    :return:
    """
    try:
        return job_dictionary[job_name]
    except KeyError:
        return 1