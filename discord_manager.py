import data_management
import os
import discord
import discord_embeds
import discord_logic
import discord_ui
import info_msgs

from discord.ext import commands

# Discord token from VENV
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

# Bot initialization
intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.watching, name="!help")
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)
bot.remove_command('help')

# Discord Commands
@bot.command()
async def start(ctx):
    '''
    !start command
    Creates a new character
    '''
    await discord_logic.create_character(ctx)


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
    await discord_logic.begin_fight(ctx, discord_ui.ActionMenu(ctx))


@bot.command()
async def boss(ctx):
    '''
    !boss command
    Makes the player fight the boss of current area
    '''
    await discord_logic.begin_boss_fight(ctx, discord_ui.ActionMenu(ctx))


@bot.command()
async def attack(ctx):
    '''
    !attack command
    Attack enemy fighting the player
    '''
    await discord_logic.attack(ctx)


@bot.command()
async def rest(ctx):
    """
    !rest command
    Fully recovers the player
    """
    await discord_logic.rest(ctx)


@bot.command()
async def inventory(ctx):
    """
    !inventory command
    Shows player's inventory
    """
    await discord_logic.inventory(ctx)


@bot.command()
async def profile(ctx):
    """
    !profile command
    Shows player's profile
    """
    await discord_logic.profile(ctx, None)


@bot.command()
async def menu(ctx):
    """
    !menu command
    Shows main menu, with player's profile and buttons for interacting (in order to minimize inputting commands)
    """
    await discord_logic.profile(ctx, discord_ui.PlayerMenu(ctx))


@bot.command()
async def shop(ctx):
    """
    !shop command
    Shows the shop of the current area
    """
    await discord_logic.shop(ctx)


@bot.command()
async def equipment(ctx):
    """
    !equipment command
    Shows player's equipment
    """
    await discord_logic.equipment(ctx)


@bot.command()
async def job(ctx):
    """
    !job command
    Shows player's job, also allows to change it
    """
    await discord_logic.job(ctx)


@bot.command()
async def skills(ctx):
    """
    !skills command
    Shows player's skills info
    """
    await discord_logic.show_skills(ctx)


@bot.command()
async def dungeon(ctx):
    """
    !dungeon command
    Shows all dungeons in current area
    """
    await discord_logic.dungeon(ctx)


@bot.command()
async def duel(ctx, enemy_name: str):
    """
    !duel command
    Makes the player fight another player
    """
    await discord_logic.duel(ctx, enemy_name.lower())


def msgs_to_msg_str(msgs: list) -> str:
    """
    Converts a list of messages to a string

    :param msgs: List of messages
    :return: String containing all messages.
    """
    return "\n".join(msgs)

# Main program
if __name__ == "__main__":
    data_management.load_everything()
    bot.run(DISCORD_TOKEN)
