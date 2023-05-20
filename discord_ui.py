import discord

import emojis
import interface
import data_management
import discord_embeds
import messager

import time


class ActionMenu(discord.ui.View):
    """
    Class that handles the menu while in combat.
    """
    def __init__(self, ctx):
        super().__init__()
        self.value = None
        self.ctx = ctx

    @discord.ui.button(label="Attack", style=discord.ButtonStyle.red)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            start_time = time.time()
            no_error, msgs = interface.normal_attack(self.ctx.author.name)
            await continue_battle(no_error, msgs, self.ctx)
            await interaction.response.defer()
            print(f"Attack took {time.time() - start_time} seconds")

    @discord.ui.button(label="Skill", style=discord.ButtonStyle.primary)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            battle = data_management.search_cache_battle_by_player(self.ctx.author.name)
            cooldown_str = ""
            if len(battle.skills_in_cooldown) != 0:
                skills_in_cooldown_str_list = [f"**{s}**: {battle.skills_in_cooldown[s] + 1}" for s in battle.skills_in_cooldown]
                cooldown_str = f"\nSkills in cooldown - {','.join(skills_in_cooldown_str_list)}"
            skill_list = battle.player.skills.copy()
            for skill in battle.skills_in_cooldown:
                skill_list.remove(skill)
            if len(skill_list) == 0:
                await self.ctx.send(f"**Escordia Error** - {self.ctx.author.mention}: You have no skills to use!")
            else:
                await interaction.response.send_message(f"Please select a skill to perform, {self.ctx.author.mention}"
                                                        f"{cooldown_str}",
                                                        view=SkillSelectView(self.ctx, skill_list, battle.player.current_job))

    @discord.ui.button(label="Item", style=discord.ButtonStyle.green)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            print("Item!")


class ItemBuySelect(discord.ui.Select):
    def __init__(self, ctx, item_list):
        items_in_options = [data_management.search_cache_item_by_name(i) for i in item_list]
        options = [discord.SelectOption(label=i.name,
                                        description=f"{i.description if i.object_type != 'EQUIPMENT' else ''}"
                                                    f"{' ' + str(i.stat_change_list).replace('{', '').replace('}', '') if i.object_type == 'EQUIPMENT' else ''}"
                                                    f" - {i.individual_value}G",
                                        emoji=emojis.obj_emoji(i)) for i in items_in_options]
        super().__init__(placeholder="Select an item to buy", max_values=1, min_values=1, options=options)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        if await check_button_pressed(self.ctx, interaction):
            item = data_management.search_cache_item_by_name(self.values[0])
            no_error, msgs = interface.buy_item(self.ctx.author.name, item.name)
            if no_error:
                await interaction.response.send_message(msgs_to_msg_str(msgs))
            else:
                await self.ctx.send(f'**Escordia Error** - {self.ctx.author.mention}: {msgs}')


class ItemBuySelectView(discord.ui.View):
    def __init__(self, ctx, item_list):
        super().__init__()
        self.add_item(ItemBuySelect(ctx, item_list))


class EquipmentSelect(discord.ui.Select):
    def __init__(self, ctx, item_list, player_equipment):
        default_option = None
        if player_equipment is not None:
            player_equipment = data_management.search_cache_item_by_name(player_equipment)
            default_option = discord.SelectOption(label=player_equipment.name,
                                                    description=f"{player_equipment.description}"
                                                        f"{' ' + str(player_equipment.stat_change_list)}",
                                                    emoji=emojis.obj_emoji(player_equipment),
                                                    default=True)

        items_in_options = [data_management.search_cache_item_by_name(i.name) for i in item_list]
        options = [discord.SelectOption(label=i.name,
                                        description=f"{i.description}"
                                                    f"{' ' + str(i.stat_change_list)}",
                                        emoji=emojis.obj_emoji(i)) for i in items_in_options]

        if default_option is not None:
            options.append(default_option)

        super().__init__(placeholder="Select an item to equip", max_values=1, min_values=1, options=options)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        if await check_button_pressed(self.ctx, interaction):
            item = data_management.search_cache_item_by_name(self.values[0])
            no_error, msgs = interface.equip_item(self.ctx.author.name, item.name)
            if no_error:
                await interaction.response.send_message(msgs_to_msg_str(msgs))
            else:
                await self.ctx.send(f'**Escordia Error** - {self.ctx.author.mention}: {msgs}')


class EquipmentSelectView(discord.ui.View):
    def __init__(self, ctx, item_list, player_equipment):
        super().__init__()
        self.add_item(EquipmentSelect(ctx, item_list, player_equipment))


class SkillSelect(discord.ui.Select):
    def __init__(self, ctx, skill_list, curr_job):
        skills_in_options = [data_management.search_cache_skill_by_name(i) for i in skill_list]
        options = [discord.SelectOption(label=s.name,
                                        description=f"Power: {s.power} | Cooldown: {s.cooldown}",
                                        emoji=emojis.skill_emoji(s, curr_job)) for s in skills_in_options]
        super().__init__(placeholder=f"Select a skill to perform", max_values=1, min_values=1, options=options)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        if await check_button_pressed(self.ctx, interaction):
            start_time = time.time()
            skill = data_management.search_cache_skill_by_name(self.values[0])
            no_error, msgs = interface.skill_attack(self.ctx.author.name, skill.name)
            await continue_battle(no_error, msgs, self.ctx)
            await interaction.response.defer()
            print(f"Skill took {time.time() - start_time} seconds")


class SkillSelectView(discord.ui.View):
    def __init__(self, ctx, skill_list, curr_job):
        super().__init__()
        self.add_item(SkillSelect(ctx, skill_list, curr_job))


# TODO - Current job as default
class JobSelect(discord.ui.Select):
    def __init__(self, ctx, job_list):
        jobs_in_options = [data_management.search_cache_job_by_name(i) for i in job_list]
        options = [discord.SelectOption(label=j.name,
                                        description=f"{j.description}",
                                        emoji=emojis.job_to_emoji[j.name]) for j in jobs_in_options]
        super().__init__(placeholder=f"Select a job to change to", max_values=1, min_values=1, options=options)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        if await check_button_pressed(self.ctx, interaction):
            job = data_management.search_cache_job_by_name(self.values[0])
            no_error, msgs = interface.change_player_job(self.ctx.author.name, job.name)
            if no_error:
                await interaction.response.send_message(msgs_to_msg_str(msgs))
            else:
                await self.ctx.send(f'**Escordia Error** - {self.ctx.author.mention}: {msgs}')


class JobSelectView(discord.ui.View):
    def __init__(self, ctx, job_list):
        super().__init__()
        self.add_item(JobSelect(ctx, job_list))


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


async def check_button_pressed(ctx, interaction) -> bool:
    """
    Checks if button has been pressed by same user that initiated the interaction.

    :param ctx: Discord's CTX
    :param interaction: Discord's interaction
    :return: True if button pressed by correspondent user, False if not. Also spits a message.
    """
    if interaction.user.name == ctx.author.name:
        return True
    else:
        await interaction.response.send_message(f"That button is not for you, {interaction.user.mention}!")
        return False


async def continue_battle(no_error: bool, msgs: list, ctx) -> None:
    if no_error:
        battle = data_management.search_cache_battle_by_player(ctx.author.name)
        msg_str = msgs_to_msg_str(msgs)
        if battle.is_over:
            msg_str = msgs_to_msg_str(msgs)
            await ctx.send(msg_str)
            if battle.player.alive:
                battle.win_battle()
                await ctx.send('', embed=discord_embeds.embed_victory_msg(ctx, msgs_to_msg_str(
                    messager.empty_queue(ctx.author.name))))
            else:
                battle.lose_battle()
                await ctx.send('', embed=discord_embeds.embed_death_msg(ctx, msgs_to_msg_str(
                    messager.empty_queue(ctx.author.name))))
        else:
            await ctx.send(msg_str,
                                embed=discord_embeds.embed_fight_msg(ctx, battle.player, battle.enemy),
                                view=ActionMenu(ctx))
    else:
        await ctx.send(f'**Escordia Error** - {ctx.author.mention}: {msgs}')
