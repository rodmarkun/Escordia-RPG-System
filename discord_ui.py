import random
import discord
import discord_logic
import emojis
import interface
import data_management
import discord_embeds
import time


class ActionMenu(discord.ui.View):
    """
    Class that handles the menu while in combat.
    """

    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.value = None
        self.ctx = ctx

    # Normal Attack
    @discord.ui.button(label="Attack", style=discord.ButtonStyle.red)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            await discord_logic.attack(self.ctx)
            await interaction.response.defer()

    # Skill
    @discord.ui.button(label="Skill", style=discord.ButtonStyle.primary)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            battle = data_management.search_cache_battle_by_player(self.ctx.author.name)

            # All of this is to get all player skills that are not in cooldown
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
                await interaction.response.send_message(f"Please select a skill to perform, {self.ctx.author.mention}.\n"
                                                        f"Remember you can see information about your skills in `!skills`\n"
                                                        f"{cooldown_str}",
                                                        view=SkillSelectView(self.ctx, skill_list, battle.player.current_job))

    # Item
    @discord.ui.button(label="Inspect enemy", style=discord.ButtonStyle.green)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            await interaction.response.send_message(embed=discord_embeds.embed_enemy_info(self.ctx, data_management.search_cache_battle_by_player(self.ctx.author.name).enemy))


class PlayerMenu(discord.ui.View):
    """
    Class that handles general menu.
    """

    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.value = None
        self.ctx = ctx

    # Fight
    @discord.ui.button(label=emojis.CROSSED_SWORDS_EMOJI + " Fight", style=discord.ButtonStyle.red)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            await discord_logic.begin_fight(self.ctx, ActionMenu(self.ctx))
            await interaction.response.defer()

    # Dungeon
    @discord.ui.button(label=emojis.CASTLE_EMOJI + " Dungeon", style=discord.ButtonStyle.red)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            await discord_logic.dungeon(self.ctx)
            await interaction.response.defer()

    # Boss
    @discord.ui.button(label=emojis.SKULL_EMOJI + " Boss", style=discord.ButtonStyle.red)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            await discord_logic.begin_boss_fight(self.ctx, ActionMenu(self.ctx))
            await interaction.response.defer()


    # Map
    @discord.ui.button(label=emojis.MAP_EMOJI + " Map", style=discord.ButtonStyle.primary)
    async def menu4(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            await discord_logic.area(self.ctx)
            await interaction.response.defer()


    # Equipment
    @discord.ui.button(label=emojis.MAGE_EMOJI + " Equipment", style=discord.ButtonStyle.primary)
    async def menu5(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            await discord_logic.equipment(self.ctx)
            await interaction.response.defer()


    # Skill Info
    @discord.ui.button(label=emojis.SPARKLER_EMOJI + " Skills", style=discord.ButtonStyle.primary)
    async def menu6(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            await discord_logic.show_skills(self.ctx)
            await interaction.response.defer()


    # Job
    @discord.ui.button(label=emojis.CRYSTAL_BALL_EMOJI + " Job", style=discord.ButtonStyle.primary)
    async def menu7(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            await discord_logic.job(self.ctx)
            await interaction.response.defer()


    # Rest
    #@discord.ui.button(label=emojis.BED_EMOJI + " Rest", style=discord.ButtonStyle.green)
    #async def menu8(self, interaction: discord.Interaction, button: discord.ui.Button):
    #    if await check_button_pressed(self.ctx, interaction):
    #        await discord_logic.rest(self.ctx)
    #        await interaction.response.defer()


    # Shop
    @discord.ui.button(label=emojis.SHOP_EMOJI + " Shop", style=discord.ButtonStyle.green)
    async def menu9(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            await discord_logic.shop(self.ctx)
            await interaction.response.defer()


    # Extract Essence
    @discord.ui.button(label=emojis.EXTRACT_ESSENCE_EMOJI + " Essence", style=discord.ButtonStyle.green)
    async def menu10(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            await discord_logic.essence(self.ctx)
            await interaction.response.defer()

    # PVP
    #@discord.ui.button(label=emojis.DAGGER_EMOJI + " PVP", style=discord.ButtonStyle.green)
    #async def menu11(self, interaction: discord.Interaction, button: discord.ui.Button):
    #    if await check_button_pressed(self.ctx, interaction):
    #        await interaction.response.send_message(info_msgs.PVP_MSG)


# TODO
class ToinCossMenu(discord.ui.View):
    """
    Class that handles general menu.
    """

    def __init__(self, ctx, dueled_player: str):
        super().__init__(timeout=None)
        self.dueled_player = dueled_player
        self.option_chosen = None
        self.ctx = ctx

    # Fight
    @discord.ui.button(label="Heads", style=discord.ButtonStyle.red)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed_by_certain_name(self.ctx, interaction, self.dueled_player):
            await discord_logic.begin_pvp_fight(self.ctx, ActionMenu(self.ctx), self.ctx.author, self.dueled_player, "HEADS")
            await interaction.response.defer()

    # Fight
    @discord.ui.button(label="Tails", style=discord.ButtonStyle.red)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed_by_certain_name(self.ctx, interaction, self.dueled_player):
            await discord_logic.begin_pvp_fight(self.ctx, ActionMenu(self.ctx), self.ctx.author, self.dueled_player, "TAILS")
            await interaction.response.defer()


class ItemBuySelect(discord.ui.Select):
    """
    Class that handles the item selection for the shop.
    """

    def __init__(self, ctx, item_list):
        items_in_options = [data_management.search_cache_item_by_name(i) for i in item_list]
        stat_str_remove = "'"
        options = [discord.SelectOption(label=i.name,
                                        description=f"{i.description if i.object_type != 'EQUIPMENT' else ''}"
                                                    f"{i.stat_list_formatted()}"
                                                    f"  - {i.individual_value}G",
                                        emoji=emojis.obj_emoji(i)) for i in items_in_options]
        super().__init__(placeholder="Select an item to buy", max_values=1, min_values=1, options=options)
        self.ctx = ctx

    # Buys an item
    async def callback(self, interaction: discord.Interaction) -> None:
        """
        Callback function for the item selection.

        :param interaction: Discord interaction
        :return: None
        """

        if await check_button_pressed(self.ctx, interaction):
            item = data_management.search_cache_item_by_name(self.values[0])
            # Buys the item
            no_error, msgs = interface.buy_item(self.ctx.author.name, item.name)
            if no_error:
                await interaction.response.send_message(discord_logic.msgs_to_msg_str(msgs))
            else:
                await self.ctx.send(f'**Escordia Error** - {self.ctx.author.mention}: {msgs}')


class ItemBuySelectView(discord.ui.View):
    def __init__(self, ctx, item_list):
        super().__init__(timeout=None)
        self.add_item(ItemBuySelect(ctx, item_list))


class ItemDestroySelect(discord.ui.Select):
    """
    Class that handles the item destruction for essence.
    """

    def __init__(self, ctx, item_list):
        items_in_options = [data_management.search_cache_item_by_name(i) for i in item_list]
        options = [discord.SelectOption(label=i.name,
                                        description=f"{i.description if i.object_type != 'EQUIPMENT' else ''}"
                                                    f"{i.stat_list_formatted()}",
                                        emoji=emojis.obj_emoji(i)) for i in items_in_options]
        super().__init__(placeholder="Select an item to destroy", max_values=1, min_values=1, options=options)
        self.ctx = ctx

    # Destroys an item
    async def callback(self, interaction: discord.Interaction) -> None:
        """
        Callback function for the item selection.

        :param interaction: Discord interaction
        :return: None
        """
        if await check_button_pressed(self.ctx, interaction):
            item = data_management.search_cache_item_by_name(self.values[0])
            # Destroys the item
            no_error, msgs = interface.destroy_item_for_essence(self.ctx.author.name, item.name)
            if no_error:
                await interaction.response.send_message(discord_logic.msgs_to_msg_str(msgs))
            else:
                await self.ctx.send(f'**Escordia Error** - {self.ctx.author.mention}: {msgs}')

class ItemDestroySelectView(discord.ui.View):
    def __init__(self, ctx, item_list):
        super().__init__(timeout=None)
        self.add_item(ItemDestroySelect(ctx, item_list))
        self.ctx = ctx

    # Destroy all items button
    @discord.ui.button(label="Destroy all items", style=discord.ButtonStyle.red)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            no_error, msgs = interface.destroy_all_items_for_essence(self.ctx.author.name)
            if no_error:
                await interaction.response.send_message(discord_logic.msgs_to_msg_str(msgs))
            else:
                await self.ctx.send(f'**Escordia Error** - {self.ctx.author.mention}: {msgs}')


class BlessingBuySelect(discord.ui.Select):
    """
    Class that handles the blessing selection.
    """

    def __init__(self, ctx, player_blessing_list):
        items_in_options = []
        for b in data_management.BLESSINGS_CACHE:
            if b not in player_blessing_list:
                items_in_options.append(data_management.search_cache_blessing(b))
        options = [discord.SelectOption(label=b.name,
                                        description=f"{' '.join(b.stat_change_list)}" \
                                                    f"  - COST: {b.essence_cost} Essence",
                                        emoji=emojis.ESC_ESSENCE_ICON) for b in items_in_options]
        super().__init__(placeholder="Select a blessing to buy", max_values=1, min_values=1, options=options)
        self.ctx = ctx

    # Purchases a blessing
    async def callback(self, interaction: discord.Interaction) -> None:
        """
        Callback function for the blessing selection.

        :param interaction: Discord interaction
        :return: None
        """

        if await check_button_pressed(self.ctx, interaction):
            # Purchases the blessing
            no_error, msgs = interface.purchase_blessing(self.ctx.author.name, self.values[0])
            if no_error:
                await interaction.response.send_message(discord_logic.msgs_to_msg_str(msgs))
            else:
                await self.ctx.send(f'**Escordia Error** - {self.ctx.author.mention}: {msgs}')


class BlessingBuySelectView(discord.ui.View):
    def __init__(self, ctx, player_blessing_list):
        super().__init__(timeout=None)
        self.add_item(BlessingBuySelect(ctx, player_blessing_list))


class EquipmentSelect(discord.ui.Select):
    """
    Class that handles the equipment selection.
    """
    def __init__(self, ctx, item_list, player_equipment):
        default_option = None
        if player_equipment is not None:
            player_equipment = data_management.search_cache_item_by_name(player_equipment)
            default_option = discord.SelectOption(label=player_equipment.name,
                                                  description=f"{player_equipment.stat_list_formatted()}",
                                                  emoji=emojis.obj_emoji(player_equipment),
                                                  default=True)

        items_in_options = [data_management.search_cache_item_by_name(i.name) for i in item_list]

        if player_equipment in items_in_options:
            items_in_options.remove(player_equipment)

        options = [discord.SelectOption(label=i.name,
                                        description=f"{i.stat_list_formatted()}",
                                        emoji=emojis.obj_emoji(i)) for i in items_in_options]

        if default_option is not None:
            options.append(default_option)

        super().__init__(placeholder="Select an item to equip", max_values=1, min_values=1, options=options)
        self.ctx = ctx

    # Equips an item
    async def callback(self, interaction: discord.Interaction) -> None:
        """
        Callback function for the item selection.

        :param interaction: Discord Interaction
        :return: None
        """

        if await check_button_pressed(self.ctx, interaction):
            item = data_management.search_cache_item_by_name(self.values[0])
            no_error, msgs = interface.equip_item(self.ctx.author.name, item.name)
            if no_error:
                await interaction.response.send_message(discord_logic.msgs_to_msg_str(msgs))
            else:
                await self.ctx.send(f'**Escordia Error** - {self.ctx.author.mention}: {msgs}')


class EquipmentSelectView(discord.ui.View):
    def __init__(self, ctx, item_list, player_equipment):
        super().__init__(timeout=None)
        self.add_item(EquipmentSelect(ctx, item_list, player_equipment))


class AreaSelect(discord.ui.Select):
    """
    Class that handles the equipment selection.
    """

    def __init__(self, ctx, player_inst):
        current_area = data_management.search_cache_area_by_number(player_inst.current_area)
        default_option = discord.SelectOption(label=current_area.name,
                                                description=f"Area {current_area.number}",
                                              emoji=emojis.MAP_EMOJI,
                                              default=True)

        areas_in_options = [data_management.search_cache_area_by_number(a) for a in data_management.AREAS_CACHE if int(a) <= len(player_inst.defeated_bosses) + 1]

        if current_area in areas_in_options:
            areas_in_options.remove(current_area)

        options = [discord.SelectOption(label=a.name,
                                        description=f"Area {a.number}",
                                        emoji=emojis.MAP_EMOJI) for a in areas_in_options]

        if default_option is not None:
            options.append(default_option)

        super().__init__(placeholder="Select an area to travel to", max_values=1, min_values=1, options=options)
        self.ctx = ctx

    # Travels to another area
    async def callback(self, interaction: discord.Interaction) -> None:
        """
        Callback function for the area selection.

        :param interaction: Discord Interaction
        :return: None
        """

        if await check_button_pressed(self.ctx, interaction):
            area = data_management.search_cache_area_by_name(self.values[0])
            # Travel
            no_error, msgs = interface.travel_to_area(self.ctx.author.name, area.number)
            if no_error:
                await interaction.response.send_message(discord_logic.msgs_to_msg_str(msgs))
            else:
                await self.ctx.send(f'**Escordia Error** - {self.ctx.author.mention}: {msgs}')


class AreaSelectView(discord.ui.View):
    def __init__(self, ctx, player_inst):
        super().__init__(timeout=None)
        self.add_item(AreaSelect(ctx, player_inst))


class DungeonSelect(discord.ui.Select):
    """
    Class that handles the dungeon selection.
    """
    def __init__(self, ctx, dungeon_list):
        options = [discord.SelectOption(label=i.dungeon_name,
                                        description=f"Rec. Lvl: {i.recommended_lvl} | Enemies: {i.enemy_count + 1}",
                                        emoji=emojis.ESC_DUNGEON_ICON) for i in dungeon_list]
        super().__init__(placeholder="Select a dungeon to explore", max_values=1, min_values=1, options=options)
        self.ctx = ctx

    # Starts a dungeon
    async def callback(self, interaction: discord.Interaction) -> None:
        """
        Callback function for the dungeon selection.

        :param interaction: Discord interaction
        :return: None
        """

        if await check_button_pressed(self.ctx, interaction):
            dungeon = data_management.search_cache_dungeon_by_name(self.values[0])
            no_error, msgs = interface.start_dungeon(self.ctx.author.name, dungeon.dungeon_name)
            # Battles
            if no_error:
                if data_management.search_cache_player(self.ctx.author.name).in_dungeon:
                    no_error, msgs = interface.begin_battle(self.ctx.author.name, False, enemy=random.choice(dungeon.enemy_list))
                    await discord_logic.manage_battle(no_error, self.ctx, msgs, ActionMenu(self.ctx))
                    await interaction.response.defer()
            else:
                await self.ctx.send(f'**Escordia Error** - {self.ctx.author.mention}: {msgs}')


class DungeonSelectView(discord.ui.View):
    def __init__(self, ctx, dungeon_list):
        super().__init__(timeout=None)
        self.add_item(DungeonSelect(ctx, dungeon_list))


class SkillSelect(discord.ui.Select):
    """
    Class that handles the skill selection.
    """

    def __init__(self, ctx, skill_list, curr_job):
        skills_in_options = [data_management.search_cache_skill_by_name(i) for i in skill_list]
        options = [discord.SelectOption(label=s.name,
                                        description=f"Power: {s.power} | MP Cost: {s.mp_cost}{'%' if s.percentage_cost else ''} | Cooldown: {s.cooldown}",
                                        emoji=emojis.skill_emoji(s, curr_job)) for s in skills_in_options if s is not None]
        super().__init__(placeholder=f"Select a skill to perform", max_values=1, min_values=1, options=options)
        self.ctx = ctx

    # Uses a skill
    async def callback(self, interaction: discord.Interaction) -> None:
        """
        Callback function for the skill selection.

        :param interaction: Discord Interaction
        :return: None
        """

        if await check_button_pressed(self.ctx, interaction):
            skill_inst = data_management.search_cache_skill_by_name(self.values[0])
            no_error, msgs = interface.skill_attack(self.ctx.author.name, skill_inst.name)
            await discord_logic.continue_battle(self.ctx, no_error, msgs, ActionMenu(self.ctx))
            await interaction.response.defer()


class SkillSelectView(discord.ui.View):
    def __init__(self, ctx, skill_list, curr_job):
        super().__init__(timeout=None)
        self.add_item(SkillSelect(ctx, skill_list, curr_job))


# TODO - Current job as default
class JobSelect(discord.ui.Select):
    """
    Class that handles the job selection.
    """

    def __init__(self, ctx, job_list, player_inst):
        jobs_in_options = [data_management.search_cache_job_by_name(i) for i in job_list]

        jobs_curr_lvl_dict = {}
        for job_dict in player_inst.job_dict_list:
            jobs_curr_lvl_dict[job_dict["Name"]] = job_dict["lvl"]
        jobs_curr_lvl_dict[player_inst.current_job_dict["Name"]] = player_inst.current_job_dict["lvl"]

        options = [discord.SelectOption(label=j.name,
                                        description=f"Current level: {discord_logic.return_jobs_curr_lvl_dict(jobs_curr_lvl_dict, j.name)}",
                                        emoji=emojis.job_to_emoji[j.name]) for j in jobs_in_options]
        super().__init__(placeholder=f"Select a job to change to", max_values=1, min_values=1, options=options)
        self.ctx = ctx

    # Changes a player's job
    async def callback(self, interaction: discord.Interaction) -> None:
        """
        Callback function for the job selection.

        :param interaction: Discord interaction
        :return: None
        """

        if await check_button_pressed(self.ctx, interaction):
            job = data_management.search_cache_job_by_name(self.values[0])
            # Changes job
            no_error, msgs = interface.change_player_job(self.ctx.author.name, job.name)
            if no_error:
                await interaction.response.send_message(discord_logic.msgs_to_msg_str(msgs))
            else:
                await self.ctx.send(f'**Escordia Error** - {self.ctx.author.mention}: {msgs}')


class JobSelectView(discord.ui.View):
    def __init__(self, ctx, job_list, player_inst):
        super().__init__(timeout=None)
        self.add_item(JobSelect(ctx, job_list, player_inst))


async def check_button_pressed(ctx, interaction: discord.Interaction) -> bool:
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


async def check_button_pressed_by_certain_name(ctx, interaction: discord.Interaction, certain_name: str) -> bool:
    """
    Checks if button has been pressed by a certain user.

    :param ctx: Discord's CTX
    :param interaction: Discord's interaction
    :param certain_name: Name of the user that should press the button
    :return: True if button pressed by correspondent user, False if not. Also spits a message.
    """

    if interaction.user.name == certain_name:
        return True
    else:
        await interaction.response.send_message(f"That button is not for you, {interaction.user.mention}!")
        return False
