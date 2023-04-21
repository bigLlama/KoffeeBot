import discord
from discord.ext import commands
import random
import time
from discord import app_commands
from discord.app_commands import Choice
import asyncio


fight_cd = app_commands.Cooldown(1, 10)


class games(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    def fight_cooldown(interaction: discord.Interaction):
        return fight_cd

    @app_commands.command(name="rps", description="Play rock/paper/scissors against the mighty KoffeeBot!")  # Rock Paper Scissors
    @app_commands.choices(choice=[
        Choice(name="Rock", value="rock"),
        Choice(name="Paper", value="paper"),
        Choice(name="Scissors", value="scissors")])
    @app_commands.checks.cooldown(1, 3.0, key=lambda i: (i.guild_id, i.user.id))
    async def rps(self, interaction: discord.Interaction, choice: str):
        weapons = ["rock", "paper", "scissors"]
        decision = random.choice(weapons)

        def win(player, cpu):
            if (player == 'rock' and cpu == 'scissors') or (player == 'scissors' and cpu == 'paper') or (player == 'paper' and cpu == 'rock'):
                return True

        if win(choice, decision):
            result = f"You chose `{choice}`\nI chose `{decision}`\n**You Win!**"
        else:
            result = f"You chose `{choice}`\nI chose `{decision}`\n**You Lose!**"

        if choice == decision:
            result = f"You chose `{choice}`\nI chose `{decision}`\n**It's a Tie!**"

        embed = discord.Embed(title="Rock Paper Scissors", description=result, color=discord.Color.blue())
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="bowling", description="Do you have the skill to get a strike?")  # bowling
    @app_commands.checks.cooldown(1, 3.0, key=lambda i: (i.guild_id, i.user.id))
    async def bowl(self, interaction: discord.Interaction):
        outcomes = ["You've YEETED the ball out of existence!!!",
                    "Strike!!",
                    "Oohh, seems you've missed all the pins",
                    "Do you even know how to aim that thing?",
                    "Don't throw it at the children!!!",
                    "You have demolished the bowling alley, are you proud?",
                    "Strike!!",
                    "What a strike!",
                    "Close one! Only 2 pins left",
                    "I take it you don't go bowling often?",
                    "Nice Strike, You're really good at this",
                    "Only 1 pin left!",
                    "You hit 3 pins xD",
                    "Sir! The alley is this way",
                    "Nice Spare!",
                    "Strike!!",
                    "Epic fail xD",
                    "Strike! You might be the best bowler I've ever seen",
                    "You broke a finger trying to throw the ball"
                    ]
        embed = discord.Embed(description=f"{random.choice(outcomes)}", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="coinflip", description="Heads or Tails?")
    @app_commands.checks.cooldown(1, 3.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.choices(guess=[
        Choice(name="Heads", value="heads"),
        Choice(name="Tails", value="tails")])
    async def coinflip(self, interaction: discord.Interaction, guess: str):
        coin = ["heads", "tails"]
        outcome = random.choice(coin)

        while guess in coin:
            embed = discord.Embed(title='Heads or Tails', color=discord.Color.blue())
            embed.set_thumbnail(url=interaction.user.avatar)
            if str(guess) == str(outcome):
                embed.add_field(name=f"The outcome is {outcome}",
                                value=f"You have guessed correctly!", inline=False)
            else:
                embed.add_field(name=f"The outcome is {outcome}",
                                value="Better luck next time!", inline=False)
            return await interaction.response.send_message(embed=embed)

    @app_commands.command(name='duel', description="Challenge another user to a 1v1 duel!")
    @app_commands.describe(member="The user you wish to duel!")
    @app_commands.checks.dynamic_cooldown(fight_cooldown)
    async def duel(self, interaction: discord.Interaction, member: discord.Member):

        p1 = 100
        p2 = 100

        if member == interaction.user:
            app_commands.Cooldown.reset(fight_cd)
            embed = discord.Embed(title='🥊 Duel 🥊',
                                  description="You can not duel against yourself!",
                                  color=discord.Color.blue())
            return await interaction.response.send_message(embed=embed)

        embed = discord.Embed(
            title='🥊 Duel 🥊',
            description=f'{interaction.user.name} & {member.name} are now dueling!',
            color=discord.Color.blue())
        embed.add_field(name=interaction.user.name, value=f"Health: {p1}", inline=True)
        embed.add_field(name=member.name, value=f"Health: {p2}", inline=True)
        await interaction.response.send_message(embed=embed)

        while True:
            e = discord.Embed(
                title='🥊 Duel 🥊',
                description=f'{interaction.user.name} & {member.name} are now dueling!',
                color=discord.Color.blue())
            e.add_field(name=interaction.user.name, value=f"Health: {p1}", inline=True)
            e.add_field(name=member.name, value=f"Health: {p2}", inline=True)

            damage = random.randint(4, 17)
            turn = random.randint(1, 2)

            if turn == 1:
                if p1 < 25:
                    damage = random.randint(1,3)
                p1 = p1 - damage
                if p1 - damage <= 0:
                    p1 = 0
            elif turn == 2:
                if p2 < 25:
                    damage = random.randint(1,3)
                p2 = p2 - damage
                if p2 - damage <= 0:
                    p2 = 0

            time.sleep(1)
            await interaction.edit_original_response(embed=e)

            if p1 == 0:
                f = discord.Embed(
                    title='🥊 Duel 🥊',
                    description=f'{member.mention} has defeated {interaction.user.mention} and won the duel!',
                    color=discord.Color.blue())
                f.add_field(name=interaction.user.name, value=f"Health: 0", inline=True)
                f.add_field(name=member.name, value=f"Health: {p2}", inline=True)
                await interaction.edit_original_response(embed=f)
                break
            elif p2 == 0:
                f = discord.Embed(
                    title='🥊 Duel 🥊',
                    description=f'{interaction.user.mention} has defeated {member.mention} and won the duel!',
                    color=discord.Color.blue())
                f.add_field(name=interaction.user.name, value=f"Health: {p1}", inline=True)
                f.add_field(name=member.name, value=f"Health: 0", inline=True)
                await interaction.edit_original_response(embed=f)
                break


async def setup(bot):
    await bot.add_cog(games(bot))
