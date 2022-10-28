import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ext.commands import MissingPermissions, MissingRequiredArgument
import time
import os
import asyncio
from itertools import cycle
from discord.utils import find

TOKEN = "MTAzNTE0MTA4MTQ4Mzk3MjY4OQ.GsXWLD.RLn9Ar2KkF_CjAB8ghwk_cdMAnud8ulPh-KPcU"
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=['!'], intents=intents, case_insensitive=True)
client.remove_command('help')
status = cycle(["kof help",
                "with your feelings",
                "Phasmophobia 4",
                "Fantasy Tower",
                "Dead by nightlight",
                "Rainbow Seven Siege",
                "Fortnite 2",
                "War Lightning",
                "Genshin Impact 2.0",
                "Destiny 3",
                "Tower of Fantasy 2",
                "Little Foot",
                "League of Legends 2",
                "The Sims 5",
                "Far Cry 9",
                "Brawlhalla 2",
                "Overwatch 3",
                "Among You",
                "Minecraft 2",
                "Rocket League 2",
                "Rust 4",
                "Borderlands 5",
                "The Witcher 6",
                "GTA VII",
                "Elden Ring 3",
                "Cyberpunk 420",
                "COD BO 5"])  # Bot status games


@client.event  # Bot is ready
async def on_ready():
    change_status.start()
    print('Online as {0.user}'.format(client))
    print(f"Currently in {len(client.guilds)} servers")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
        print()
    except Exception as e:
        print(e)


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with client:
        await load_extensions()
        await client.start(TOKEN)




@client.event  # on guild join
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send("Hi, I'm KofeeBot. Use **kof help** to get started!")


@client.event  # error events
async def on_command_error(interaction: discord.Interaction, error):
    if isinstance(error, MissingPermissions): # missing permissions
        embed = discord.Embed(color=discord.Color.orange())
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
        embed.add_field(name="Missing Permissions", value="You don't have the required\npermissions to do that!")
        msg = await interaction.response.send_message(embed=embed)
        time.sleep(5)
        await msg.delete()

    elif isinstance(error, MissingRequiredArgument): # missing an argument in command
        embed = discord.Embed(color=discord.Color.orange())
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
        embed.add_field(name="Missing an Argument", value="Not all the requirements have been met.\nMake sure you are "
                                                          "using the command correctly\n Use **kof help** to help "
                                                          "with using a command")
        msg = await interaction.response.send_message(embed=embed)
        time.sleep(5)
        await msg.delete()
        # client.get_command(ctx.invoked_with).reset_cooldown(ctx)

    elif isinstance(error, commands.CommandOnCooldown): # cooldown handling

        timer = error.retry_after

        if timer >= 3600:
            timer_format = "hours"
            timer = error.retry_after/3600
        elif timer >= 60:
            timer_format = "min"
            timer = error.retry_after/60
        else:
            timer_format = "seconds"

        embed = discord.Embed(color=discord.Color.orange())
        embed.set_thumbnail(
            url=interaction.user.avatar)
        embed.add_field(name="Cooldown", value=f"You are on cooldown!\nTry again in `{round(timer)} {timer_format}`")
        msg = await interaction.response.send_message(embed=embed)
        time.sleep(5)
        await msg.delete()


@tasks.loop(minutes=120)  # loops different status
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.tree.command(name="servers", description="Show KoffeeBot server count")
async def servers(interaction: discord.Interaction):
    embed = discord.Embed(title="KoffeeBot Server count", color=discord.Color.orange())
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
    embed.add_field(name=f"Currently in {len(client.guilds)} servers", value="Add me to more :D\n"
                         "https://top.gg/bot/901223515242508309?s=0210af7e1c4e5")
    await interaction.response.send_message(embed=embed)

asyncio.run(main())
