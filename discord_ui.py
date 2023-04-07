import discord
import interface
import data_management
import discord_embeds

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
            no_error, msgs = interface.normal_attack(self.ctx.author.name)
            if no_error:
                battle = data_management.search_cache_battle_by_player(self.ctx.author.name)
                msg_str = msgs_to_msg_str(msgs)
                # Player won the fight
                if battle is None:
                    # This is not the best way to do this
                    loot_msg = msgs.pop()
                    win_msg = msgs.pop()
                    msg_str = msgs_to_msg_str(msgs)
                    await self.ctx.send(msg_str, embed=discord_embeds.embed_victory_msg(self.ctx, f"{win_msg}\n{loot_msg}"))
                else:
                    await self.ctx.send(msg_str, embed=discord_embeds.embed_fight_msg(self.ctx, battle.player, battle.enemy), view=ActionMenu(self.ctx))
            else:
                await self.ctx.send(f'**Escordia Error** - {self.ctx.author.mention}: {msgs}')
            await interaction.response.defer()

    @discord.ui.button(label="Skill", style=discord.ButtonStyle.primary)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            print("Skill!")

    @discord.ui.button(label="Item", style=discord.ButtonStyle.green)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            print("Item!")

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