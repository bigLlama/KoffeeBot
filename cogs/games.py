import discord
from discord.ext import commands
import random
import time
from discord import app_commands
from discord.app_commands import Choice
import asyncio


class games(commands.Cog):
    def __init__(self, client):
        self.client = client

        @client.tree.command(name="rps", description="Play rock/paper/scissors against the mighty KoffeeBot!")  # Rock Paper Scissors
        @app_commands.choices(choice=[
            Choice(name="Rock", value="rock"),
            Choice(name="Paper", value="paper"),
            Choice(name="Scissors", value="scissors")])
        @app_commands.checks.cooldown(1, 3.0, key=lambda i: (i.guild_id, i.user.id))
        async def rps(interaction: discord.Interaction, choice: str):
            weapons = ["rock", "paper", "scissors"]
            decision = random.choice(weapons)
            choice = choice.lower()

            if choice == decision:
                return await interaction.response.send_message(f"I choose {decision}. It's a Tie!")

            def win(player, cpu):
                if (player == 'rock' and cpu == 'scissors') or (player == 'scissors' and cpu == 'paper') or (player == 'paper' and cpu == 'rock'):
                    return True

            if win(choice, decision):
                return await interaction.response.send_message(f"I choose {decision}. You Win!")
            return await interaction.response.send_message(f"I choose {decision}. You Lose!")

        @client.tree.command(name="bowling", description="Do you have the skill to get a strike?")  # bowling
        @app_commands.checks.cooldown(1, 3.0, key=lambda i: (i.guild_id, i.user.id))
        async def bowl(interaction: discord.Interaction):
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
            embed = discord.Embed(description=f"{random.choice(outcomes)}", color=discord.Color.orange())
            await interaction.response.send_message(embed=embed)

        @client.tree.command(name="coinflip", description="Heads or Tails?")
        @app_commands.checks.cooldown(1, 3.0, key=lambda i: (i.guild_id, i.user.id))
        @app_commands.choices(guess=[
            Choice(name="Heads", value="heads"),
            Choice(name="Tails", value="tails")])
        async def coinflip(interaction: discord.Interaction, guess: str):
            coin = ["heads", "tails"]
            outcome = random.choice(coin)

            while guess in coin:
                embed = discord.Embed(title='Heads or Tails', color=discord.Color.orange())
                embed.set_thumbnail(url=interaction.user.avatar)
                if str(guess) == str(outcome):
                    embed.add_field(name=f"The outcome is {outcome}",
                                    value=f"You have guessed correctly!", inline=False)
                else:
                    embed.add_field(name=f"The outcome is {outcome}",
                                    value="Better luck next time!", inline=False)
                return await interaction.response.send_message(embed=embed)
            await interaction.response.send_message("That is not a valid option")

        @client.tree.command(name="guess_the_number", description="Guess a number between 1 and 10")
        @app_commands.checks.cooldown(1, 3.0, key=lambda i: (i.guild_id, i.user.id))
        async def guess(interaction: discord.Interaction):
            cpu = random.randint(1, 10)
            chances = 3

            embed = discord.Embed(description='Im thinking of a number between 1 and 10. You have 3 guesses:',
                                color=discord.Color.orange())
            await interaction.response.send_message(embed=embed)

            def check(m):
                return m.author == interaction.user

            while chances != 0:
                try:
                    guess = await client.wait_for(event='message', check=check, timeout=7.0)
                except asyncio.TimeoutError:
                    # client.get_command("guess").reset_cooldown(ctx)
                    return await interaction.response.send_message("You did not respond in time. Be quicker next time!")
                else:
                    if guess.content == str(cpu):
                        embed = discord.Embed(description="Congratulations! You've guessed correctly",
                                              color=discord.Color.orange())
                        return await interaction.response.send_message(embed=embed)
                    else:
                        chances -= 1
                        await interaction.response.send_message(f"Incorrect! You have {chances} chances left")

            embed = discord.Embed(description=f"The number was {cpu}. Better luck next time",
                                  color=discord.Color.orange())
            await interaction.response.send_message(embed=embed)

        @client.tree.command(name='fight', description="Challenge another user to a 1v1 duel!")
        @app_commands.describe(member="The user you wish to fight!")
        @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
        async def fight(interaction: discord.Interaction, member: discord.Member):

            p1 = 100
            p2 = 100
            done = False

            if member == interaction.user:
                # client.get_command("fight").reset_cooldown(ctx)
                return await interaction.response.send_message("You can not fight yourself!")


            embed = discord.Embed(title='Duel!',
                                  description=f'{member.mention}, {interaction.user.name} has challenged you to a fight to the death\n'
                                              f'Respond by typing either `accept` or `retreat`',
                                  color=discord.Color.orange())
            await interaction.response.send_message(embed=embed)

            def check(m):
                return m.author == member

            try:
                answer = await client.wait_for(event='message', check=check, timeout=10.0)
            except asyncio.TimeoutError:
                # client.get_command("fight").reset_cooldown(ctx)
                return await interaction.response.send_message("You did not respond in time. Be quicker next time!")
            else:
                if answer.content.lower() == 'retreat':
                    embed = discord.Embed(description=f'{interaction.user.mention}! {member.name} has declined your challenge', color=discord.Color.orange())
                    return await interaction.response.send_message(embed=embed)
                elif answer.content.lower() == 'accept':
                    embed = discord.Embed(
                        description=f'Duel: {interaction.user.name} & {member.name} are fighting to the death',
                        color=discord.Color.orange())
                    embed.add_field(name=interaction.user.name, value=f"Health: {p1}", inline=True)
                    embed.add_field(name=member.name, value=f"Health: {p2}", inline=True)
                    msg = await interaction.response.send_message(embed=embed)

                    while done is False:
                        e = discord.Embed(
                            description=f'Duel: {interaction.user.name} & {member.name} are fighting to the death',
                            color=discord.Color.orange())
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
                        await msg.edit(embed=e)

                        if p1 == 0:
                            f = discord.Embed(
                                description=f'{member.mention} has defeated {interaction.user.mention} and won the fight!',
                                color=discord.Color.orange())
                            f.add_field(name=interaction.user.name, value=f"Health: 0", inline=True)
                            f.add_field(name=member.name, value=f"Health: {p2}", inline=True)
                            return await msg.edit(embed=f)
                        elif p2 == 0:
                            f = discord.Embed(
                                description=f'{interaction.user.mention} has defeated {member.mention} and won the fight!',
                                color=discord.Color.orange())
                            f.add_field(name=interaction.user.name, value=f"Health: {p1}", inline=True)
                            f.add_field(name=member.name, value=f"Health: 0", inline=True)
                            return await msg.edit(embed=f)


async def setup(bot):
    await bot.add_cog(games(bot))
