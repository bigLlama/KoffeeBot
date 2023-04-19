import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from discord.ext.commands import has_permissions
import random
import asyncio
import datetime


class utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="greet", description="KoffeeBot will greet you accordingly :)")  # Hello command
    async def greet(self, interaction: discord.Interaction):
        hey = ["Hello there!",
               "Helloo",
               "Hey!",
               "Yo!",
               "Wazzup",
               f"Greetings {interaction.user.name}!",
               "Sup",
               f"Hi {interaction.user.name}"]
        if interaction.user.id == 465839240777826324:  # Me
            await interaction.response.send_message('Good to see you master')
            return
        elif interaction.user.id == 660749269921169410:  # sheepy
            await interaction.response.send_message('Hello Sheep')
            return
        elif interaction.user.id == 324570286068334592:  # janlu
            await interaction.response.send_message('My lord!')
            return
        elif interaction.user.id == 190877518029520896:  # vir juan van janlu
            await interaction.response.send_message('jys kak in leugue of legends #getgoodfam')
            return
        await interaction.response.send_message(random.choice(hey))

    @app_commands.command(name="poll", description="Make a poll")
    @app_commands.describe(topic="The topic of the poll")
    async def poll(self, interaction: discord.Interaction, topic: str, option1: str, option2: str,
                   option3: str = None, option4: str = None, option5: str = None, option6: str = None,
                   option7: str = None, option8: str = None, option9: str = None, option10: str = None):

        option_list = [option1, option2, option3, option4, option5, option6, option7, option8, option9, option10]
        num = ['\u0031\u20E3', '\u0032\u20E3', '\u0033\u20E3', '\u0034\u20E3', '\u0035\u20E3',
                '\u0036\u20E3', '\u0037\u20E3', '\u0038\u20E3', '\u0039\u20E3', '\u0030\u20E3']

        # see which options are populated
        i = 0
        items = []
        for item in option_list:
            if item is not None:
                items.append(item)
                i += 1

        # add populated items to the poll list (embed description)
        desc = ""
        for y, item in enumerate(items):
            desc += f"{num[y]} {item}\n"

        embed = discord.Embed(title=topic, description=desc, color=discord.Color.blue())
        await interaction.response.send_message(f"**{interaction.user.mention} started a poll:**")
        message = await interaction.channel.send(embed=embed)

        for x in range(i):
            await message.add_reaction(num[x])


    @app_commands.command(name="avatar", description="View someone's discord profile picture")  # avatar command
    @app_commands.describe(user="The person who you wish to view/ava")
    async def avatar(self, interaction, user: discord.Member = None):
        if user is None:
            user = interaction.user
        em = discord.Embed(title=f"{user.name}",color=discord.Color.blue())
        em.set_image(url=user.avatar)
        await interaction.response.send_message(embed=em)


    @app_commands.command(name="support", description="Join the KoffeeBot Support discord server")  # support discord server
    async def support(self, interaction: discord.Interaction):
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
        embed.add_field(name='KoffeeBot Support', value="Have any problems with KoffeeBot? Tell us here!\n[Support "
                                                        "Server](https://discord.gg/fa3j7fpbA6/ "
                                                        "'Takes you to the official KoffeeBot discord')")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="invite", description="Invite KoffeeBot to your discord server")  # Invite bot link
    async def invite(self, interaction):
        embed = discord.Embed(color=discord.Color.blue())
        embed.add_field(name="Add me to other servers :D",
                        value="https://top.gg/bot/901223515242508309?s=0210af7e1c4e5",
                        inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="giveaway", description="Start a giveaway in your server")
    @app_commands.describe(channel="The channel you wish to host the giveaway in", prize="The prize you wish to give away",
                           duration="Choose a duration format", amount="The amount of time")
    @app_commands.choices(duration=[
        Choice(name="Seconds", value="seconds"),
        Choice(name="Minutes", value="minutes"),
        Choice(name="Hours", value="hours"),
        Choice(name="Days", value="days")])
    async def giveaway(self, interaction: discord.Interaction, channel: discord.TextChannel, prize: str,
                       duration: str, amount: int):

        if amount <= 0:
            await interaction.response.send_message("Invalid duration. Please enter a positive number.")
            return

        duration_dict = {
            "seconds": datetime.timedelta(seconds=amount),
            "minutes": datetime.timedelta(minutes=amount),
            "hours": datetime.timedelta(hours=amount),
            "days": datetime.timedelta(days=amount)
        }

        embed = discord.Embed(title="Giveaway",
                              description=f"You have started a giveaway in {channel.mention}",
                              color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

        embed = discord.Embed(title="🎉 GIVEAWAY 🎉",
                              description=f"**Prize:** `{prize}`\n**Time Left:** `{amount} {duration}`",
                              color=discord.Color.blue())
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
        embed.set_footer(text="React below to enter the giveaway!")
        message = await channel.send(embed=embed)
        await message.add_reaction("🎉")

        end_time = datetime.datetime.utcnow() + duration_dict[duration]

        while datetime.datetime.utcnow() < end_time:
            time_left = end_time - datetime.datetime.utcnow()
            duration_str = str(time_left).split(".")[0]
            embed = discord.Embed(title="🎉 GIVEAWAY 🎉",
                                  description=f"**Prize:** `{prize}`\n**Time Left:** `{duration_str}`",
                                  color=discord.Color.blue())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
            embed.set_footer(text="React below to enter the giveaway!")
            await message.edit(embed=embed)
            await asyncio.sleep(1)

        # Get all users who reacted to the message
        users = []
        message = await channel.fetch_message(message.id)
        for reaction in message.reactions:
            async for user in reaction.users():
                if user not in users and not user.bot:
                    users.append(user)

        # Pick a random winner from the list of users who reacted to the message
        winner = random.choice(users)

        embed = discord.Embed(title="🎉 GIVEAWAY WINNER 🎉",
                              description=f"**Prize:** `{prize}`\n**Time Left:** `{duration_str}`\n\n"
                                          f"Congratulations {winner.mention}\nYou have won the giveaway for `{prize}`",
                              color=discord.Color.blue())
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
        embed.set_footer(text="This giveaway has ended.")
        await message.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(utilities(bot))
