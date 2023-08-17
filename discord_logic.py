import constants
import random
import discord
import discord_embeds
import discord_ui
import emojis
import info_msgs
import interface
import data_management
import messager
import battle

from error_msgs import *


async def create_character(ctx) -> None:
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


async def begin_fight(ctx, action_menu_ui: discord.ui.View) -> None:
    """
    Begins a fight for the player.

    :param ctx: Discord CTX
    :param action_menu_ui: UI View for the action menu
    :return: None
    """

    # Find treasure
    if constants.TREASURE_CHANCE_WHEN_FIGHTING >= random.randint(0, 100):
        no_error, msgs = interface.receive_treasure(ctx.author.name, constants.NUMBER_OF_ITEMS_IN_TREASURE)
        if no_error:
            await ctx.send(f'While searching the area, {ctx.author.mention} found a treasure!')
            await ctx.send(embed=discord_embeds.embed_treasure_found(ctx, msgs))
        else:
            await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')
    # Begin fight
    else:
        no_error, msgs = interface.begin_battle(ctx.author.name, False)
        if no_error:
            battle_inst = data_management.search_cache_battle_by_player(ctx.author.name)
            await ctx.send(embed=discord_embeds.embed_fight_msg(ctx, battle_inst.player, battle_inst.enemy),
                           view=action_menu_ui)
        else:
            await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


# TODO
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

async def begin_boss_fight(ctx, action_menu_ui) -> None:
    """
    Begins a boss fight for the player.

    :param ctx: Discord CTX
    :param action_menu_ui: UI View for the action menu
    :return: None
    """

    no_error, msgs = interface.begin_battle(ctx.author.name, True)
    if no_error:
        battle_inst = data_management.search_cache_battle_by_player(ctx.author.name)
        await ctx.send(embed=discord_embeds.embed_fight_msg(ctx, battle_inst.player, battle_inst.enemy),
                       view=action_menu_ui)
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def attack(ctx) -> None:
    """
    Attacks the enemy.

    :param ctx: Discord CTX
    :return: None.
    """

    no_error, msgs = interface.normal_attack(ctx.author.name)
    await continue_battle(ctx, no_error, msgs, discord_ui.ActionMenu(ctx))


async def rest(ctx) -> None:
    """
    Rests the player (Fully recovers).

    :param ctx: Discord CTX
    :return: None
    """

    no_error, msgs = interface.player_rest(ctx.author.name)
    if no_error:
        msg_str = msgs_to_msg_str(msgs)
        await ctx.send(msg_str)
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def inventory(ctx) -> None:
    """
    Shows the player's inventory.

    :param ctx: Discord CTX
    :return: None
    """

    no_error, msgs = interface.show_player_inventory(ctx.author.name)
    if no_error:
        await ctx.send(msgs_to_msg_str(msgs))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def shop(ctx) -> None:
    """
    Shows the area's shop.

    :param ctx: Discord CTX
    :return: None
    """

    no_error, msgs = interface.show_shop_inventory(ctx.author.name)
    if no_error:
        item_list = data_management.search_cache_shop_by_area(
            data_management.search_cache_player(ctx.author.name).current_area).item_list
        await ctx.send(
            f"Please select an item to buy, {ctx.author.mention}. You currently have **{data_management.search_cache_player(ctx.author.name).money}** {emojis.ESC_GOLD_ICON}",
            view=discord_ui.ItemBuySelectView(ctx, item_list))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def equipment(ctx) -> None:
    """
    Shows the player's equipment.

    :param ctx: Discord CTX
    :return: None
    """

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


async def essence(ctx) -> None:
    """
    Shows the essence menu.

    :param ctx: Discord CTX
    :return: None
    """

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


async def area(ctx) -> None:
    """
    Shows the area menu.

    :param ctx: Discord CTX
    :return: None
    """

    no_error, msgs = interface.show_area(ctx.author.name)
    if no_error:
        player_inst = data_management.search_cache_player(ctx.author.name)
        await ctx.send(msgs_to_msg_str(msgs), view=discord_ui.AreaSelectView(ctx, player_inst))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def profile(ctx, player_menu_ui: discord.ui.View) -> None:
    """
    Shows the player's profile.

    :param ctx: Discord CTX
    :param player_menu_ui: Player menu UI
    :return: None
    """

    no_error, msgs = interface.show_player_profile(ctx.author.name)
    if no_error:
        player_inst = data_management.search_cache_player(ctx.author.name)
        job_inst = data_management.search_cache_job_by_name(player_inst.current_job)
        await ctx.send(embed=discord_embeds.embed_player_profile(ctx, ctx.author.name, player_inst, job_inst), view=player_menu_ui)
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def job(ctx) -> None:
    """
    Shows the player's job info.

    :param ctx: Discord CTX
    :return: None
    """

    no_error, msgs = interface.show_player_job(ctx.author.name)
    if no_error:
        player_inst = data_management.search_cache_player(ctx.author.name)
        await ctx.send(embed=discord_embeds.embed_current_job(ctx, player_inst.current_job, msgs_to_msg_str(msgs)),
                       view=discord_ui.JobSelectView(ctx,
                                                     data_management.search_available_jobs_by_player(player_inst.name), player_inst))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def show_skills(ctx) -> None:
    """
    Shows the player's skills and its information.

    :param ctx: Discord CTX
    :return: None
    """

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


async def dungeon(ctx) -> None:
    """
    Shows the dungeon menu.

    :param ctx: Discord CTX
    :return: None
    """

    no_error, msgs = interface.show_dungeons(ctx.author.name)
    if no_error:
        dungeon_list = [data_management.search_cache_dungeon_by_name(d) for d in msgs]
        await ctx.send(f"Please select a dungeon, {ctx.author.mention}",
                       view=discord_ui.DungeonSelectView(ctx, dungeon_list))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


# WIP
async def duel(ctx, enemy_name: str) -> None:
    """
    Shows the duel menu.

    :param ctx: Discord CTX
    :param enemy_name: Enemy name
    :return: None
    """

    no_error, msgs = interface.duel_check(ctx.author.name, enemy_name)
    if no_error:
        await ctx.send(embed=discord_embeds.embed_duel_msg(ctx, enemy_name), view=discord_ui.DuelSelectView(ctx, battle))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def continue_battle(ctx, no_error: bool, msgs: list, action_menu_ui: discord.ui.View) -> None:
    """
    Handles the logic of the battle after finishing a turn.

    :param ctx: Discord CTX
    :param no_error: Whether there was an error or not
    :param msgs: Info msgs of the battle
    :param action_menu_ui: Action menu UI discord object
    :return: None
    """

    if no_error:
        # Search battle
        battle_inst = data_management.search_cache_battle_by_player(ctx.author.name)
        msg_str = msgs_to_msg_str(msgs)

        # Battle is over
        if battle_inst.is_over:
            msg_str = msgs_to_msg_str(msgs)
            await ctx.send(msg_str)
            # Player wins
            if battle_inst.player.alive:
                loot = battle_inst.win_battle()
                await ctx.send('', embed=discord_embeds.embed_victory_msg(ctx, msgs_to_msg_str(
                    messager.empty_queue(ctx.author.name))))
                if loot != '':
                    await ctx.send(embed=discord_embeds.embed_treasure_found(ctx, [loot]))
                if battle_inst.player.in_dungeon:
                    await traverse_dungeon(battle_inst, ctx)
                else:
                    await profile(ctx, discord_ui.PlayerMenu(ctx))
            # Player loses
            else:
                battle_inst.lose_battle()
                await ctx.send('', embed=discord_embeds.embed_death_msg(ctx))
                await profile(ctx, discord_ui.PlayerMenu(ctx))
        # Continue battle
        else:
            await ctx.send(msg_str, embed=discord_embeds.embed_fight_msg(ctx, battle_inst.player, battle_inst.enemy),
                                    view=action_menu_ui)
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs}')

async def manage_battle(ctx, no_error: bool, msgs: list, action_menu_ui: discord.ui.View) -> None:
    """
    Manages a battle after starting it.

    :param ctx: Discord CTX
    :param no_error: Whether there was an error or not
    :param msgs: List of info messages.
    :param action_menu_ui: Action menu UI discord object
    :return: None.
    """

    if no_error:
        battle_inst = data_management.search_cache_battle_by_player(ctx.author.name)
        await ctx.send(
            embed=discord_embeds.embed_fight_msg(ctx, battle_inst.player, battle_inst.enemy),
            view=action_menu_ui)
    else:
        await ctx.send(
            f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')


async def traverse_dungeon(ctx, battle_inst: battle.Battle) -> None:
    """
    Traverses a dungeon after defeating an enemy of that same dungeon.

    :param battle_inst: Battle instance.
    :param ctx: Discord CTX
    :return: None
    """

    dungeon_inst = data_management.search_cache_dungeon_inst_by_player(battle_inst.player.name)
    # if it was the boss, receive rewards from the dungeon
    if dungeon_inst.boss_defeated:
        # Receive rewards
        no_error, msgs = interface.receive_treasure(ctx.author.name, random.randint(2, 3))
        # Remove dungeon
        battle_inst.player.in_dungeon = False
        if no_error:
            await ctx.send(embed=discord_embeds.embed_treasure_found(ctx, msgs))
            await profile(ctx, discord_ui.PlayerMenu(ctx))
        else:
            await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs_to_msg_str(msgs)}')
        data_management.delete_cache_dungeon_inst(battle_inst.player.name)
        data_management.update_player_info(battle_inst.player.name)
    # Check if next enemy should be a boss or not
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


def return_jobs_curr_lvl_dict(job_dictionary, job_name) -> int:
    """
    Returns the current level of a job from a dictionary.
    This is not clean, but whatever.

    :param job_dictionary: Dictionary containing the jobs.
    :param job_name: Name of the job.
    :return: Integer with current level of the job.
    """

    try:
        return job_dictionary[job_name]
    except KeyError:
        return 1