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


        # @client.tree.command(name="poll")  # make a poll
        # @app_commands.describe(question="Type your poll question here")
        # async def poll(interaction: discord.Interaction, question: str, options: str):
        #     if len(options) <= 1:
        #         await interaction.response.send_message('You need more than one option to make a poll!')
        #         return
        #     if len(options) > 10:
        #         await interaction.response.send_message('You cannot make a poll for more than 10 things!')
        #         return
        #
        #     if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
        #         reactions = ['✅', '❌']
        #     else:
        #         reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
        #
        #     description = []
        #     for x, option in enumerate(options):
        #         description += '\n {} {}'.format(reactions[x], option)
        #     embed = discord.Embed(title=question, description=''.join(description), color=discord.Color.orange())
        #     embed.set_thumbnail(
        #         url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
        #     embed.set_footer(text=f"Poll created by {interaction.user}", icon_url=interaction.user.avatar)
        #     react_message = await interaction.response.send_message(embed=embed)
        #     for reaction in reactions[:len(options)]:
        #         await react_message.add_reaction(reaction)
        #     await react_message.edit_message(embed=embed)



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
