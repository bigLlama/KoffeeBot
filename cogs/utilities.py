import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import has_permissions
import random


class utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

        @client.tree.command(name="greet", description="KoffeeBot will greet you accordingly :)")  # Hello command
        async def greet(interaction: discord.Interaction):
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

        @client.tree.command(name="poll", description="Make a poll")
        @app_commands.describe(topic="The topic of the poll")
        async def poll(interaction: discord.Interaction, topic: str, option1: str, option2: str,
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

            embed = discord.Embed(title=topic, description=desc, color=discord.Color.orange())
            await interaction.response.send_message(f"**{interaction.user.mention} started a poll:**")
            message = await interaction.channel.send(embed=embed)

            for x in range(i):
                await message.add_reaction(num[x])


        @client.tree.command(name="avatar", description="View someone's discord profile picture")  # avatar command
        @app_commands.describe(user="The person who you wish to view/ava")
        async def avatar(interaction, user: discord.Member = None):
            if user is None:
                user = interaction.user
            em = discord.Embed(title=f"{user.name}",color=discord.Color.orange())
            em.set_image(url=user.avatar)
            await interaction.response.send_message(embed=em)


        @client.tree.command(name="support", description="Join the KoffeeBot Support discord server")  # support discord server
        async def support(interaction: discord.Interaction):
            embed = discord.Embed(color=discord.Color.orange())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
            embed.add_field(name='KoffeeBot Support', value="Have any problems with KoffeeBot? Tell us here!\n[Support "
                                                            "Server](https://discord.gg/fa3j7fpbA6/ "
                                                            "'Takes you to the official KoffeeBot discord')")
            await interaction.response.send_message(embed=embed)

        @client.tree.command(name="invite", description="Invite KoffeeBot to your discord server")  # Invite bot link
        async def invite(interaction):
            embed = discord.Embed(color=discord.Color.orange())
            embed.add_field(name="Add me to other servers :D",
                            value="https://top.gg/bot/901223515242508309?s=0210af7e1c4e5",
                            inline=False)
            await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(utilities(bot))
