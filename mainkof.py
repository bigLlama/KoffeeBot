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


@client.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
    if isinstance(error, app_commands.errors.CommandOnCooldown):
        timer = error.retry_after

        if timer >= 3600:
            timer_format = "hours"
            timer = error.retry_after/3600
        elif timer >= 60:
            timer_format = "min"
            timer = error.retry_after/60
        else:
            timer_format = "seconds"

        embed = discord.Embed(color=discord.Color.blue())
        embed.set_thumbnail(
            url=interaction.user.avatar)
        embed.add_field(name="Cooldown", value=f"You are on cooldown!\nTry again in `{round(timer)} {timer_format}`")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    elif isinstance(error, app_commands.errors.MissingPermissions):
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
        embed.add_field(name="Missing Permissions", value="You don't have the required\npermissions to do that!")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    elif isinstance(error, app_commands.errors.BotMissingPermissions):
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
        embed.add_field(name="Bot Missing Permissions", value="KoffeeBot does not have the required permissions to do this command. Make sure you have enabled permissions for me to do so")
        await interaction.response.send_message(embed=embed)


@tasks.loop(minutes=120)  # loops different status
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.tree.command(name="servers", description="Show KoffeeBot server count")
async def servers(interaction: discord.Interaction):
    embed = discord.Embed(title="KoffeeBot Server count", color=discord.Color.blue())
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
    embed.add_field(name=f"Currently in {len(client.guilds)} servers", value="Add me to more :D\n"
                         "https://top.gg/bot/901223515242508309?s=0210af7e1c4e5")
    await interaction.response.send_message(embed=embed)

asyncio.run(main())
