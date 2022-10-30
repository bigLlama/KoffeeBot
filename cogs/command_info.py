import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands


class commandsInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="help", description="View a list of KoffeeBot's categories and commands")  # commands/help
    @app_commands.describe(category="Browse KoffeeBot's help categories")
    @app_commands.choices(category=[
        Choice(name="Economy", value="economy"),
        Choice(name="Games", value="Games"),
        Choice(name="Images", value="Images"),
        Choice(name="Mafia", value="Mafia"),
        Choice(name="Fun", value="Fun"),
        Choice(name="Miscellaneous", value="Misc"),
        Choice(name="Moderation", value="Moderation")])
    async def help(self, interaction: discord.Interaction, category: str = None):
        if category is None:
            embed = discord.Embed(
                title="A list of all my current commands/features",
                description="Descriptions are provided below each command\n" 
                            "[Support Server](https://discord.gg/fa3j7fpbA6/ 'Takes you to the official KoffeeBot "
                            "discord')",
                color=discord.Color.orange()
            )
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
            embed.add_field(name=":tada: help fun", value="Displays all fun related commands",inline=True)
            embed.add_field(name=":moneybag: help economy", value="Displays all economy commands", inline=True)
            embed.add_field(name=":game_die: help games", value="Displays all game related commands",inline=True)
            embed.add_field(name=":shield: help moderation", value="Displays all moderation commands",inline=True)
            embed.add_field(name=":jigsaw: help images", value="Displays all image manipulation commands",inline=True)
            embed.add_field(name=":pushpin: help misc", value="Displays all miscellaneous commands ", inline=True)
            embed.add_field(name="<:hat:984285090190360657> help mafia", value="Displays all mafia commands ", inline=True)

            await interaction.response.send_message(embed=embed)
            return

        if category.lower() == "moderation":
            embed = discord.Embed(
                title="Moderation",
                description="Descriptions are provided below each command\n"
                            "[Support Server](https://discord.gg/fa3j7fpbA6/ 'Takes you to the official KoffeeBot "
                            "discord')",
                color=discord.Color.orange())
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
            embed.add_field(name=":wastebasket: clear [Amount]", value="Deletes a specified amount of text messages", inline=True)
            embed.add_field(name=":foot: kick [user] [Reason]", value="Kicks someone from the server", inline=True)
            embed.add_field(name=":hammer: ban [user] [Reason]", value="Bans someone from the server",
                            inline=True)
            embed.add_field(name=":tools: unban [user]", value="Unbans someone\n", inline=True)
            embed.add_field(name=":tickets: giverole [role] [user]", value="Give someone a role from your server",
                            inline=True)
            embed.add_field(name=":carpentry_saw: removerole [role] [user]", value="Remove a role from someone",
                            inline=True)
            await interaction.response.send_message(embed=embed)

        elif category.lower() == "misc":
            embed = discord.Embed(
                title="Miscellaneous",
                description="Descriptions are provided below each command\n"
                            "[Support Server](https://discord.gg/fa3j7fpbA6/ 'Takes you to the official KoffeeBot "
                            "discord')",
                color=discord.Color.orange()
            )
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
            embed.add_field(name=":wave: greet", value="KoffeeBot introduces\n itself", inline=True)
            embed.add_field(name=":thumbsup: poll [message]", value="Creates a poll", inline=True)
            embed.add_field(name=":performing_arts: avatar", value="View a user's profile picture", inline=True)
            embed.add_field(name=":bellhop: invite", value="Add KoffeeBot to other servers", inline=True)
            embed.add_field(name=':hourglass: support', value="Have any problems with KoffeeBot?")
            embed.add_field(name=':chart_with_upwards_trend: servers', value="Check how many servers are using KoffeeBot")
            await interaction.response.send_message(embed=embed)

        elif category.lower() == "fun":
            embed = discord.Embed(
                title="Fun",
                description="Descriptions are provided below each command\n"
                            "[Support Server](https://discord.gg/fa3j7fpbA6/ 'Takes you to the official KoffeeBot "
                            "discord')",
                color=discord.Color.orange()
            )
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
            embed.add_field(name=":8ball: 8ball [Question]", value="Ask the magical 8ball any question you like",
                            inline=True)
            embed.add_field(name=":rofl: roast", value="Roasts someone", inline=True)
            embed.add_field(name=":eyes: simp", value="Are you a simp?\n", inline=True)
            embed.add_field(name=":brain: dumb", value="Checks how stupid someone is", inline=True)
            embed.add_field(name=":rainbow_flag: gay", value="How gay are you really?\n", inline=True)
            embed.add_field(name=":smile: laugh", value="KoffeeBot will awkwardly laugh", inline=True)
            embed.add_field(name=":roll_of_paper: meme", value="Enjoy some quality memes!", inline=True)
            embed.add_field(name="⭕ o [message]", value="Replace all vowels with the letter 'o'", inline=True)
            embed.add_field(name="✨ insult", value="Curse someone with the mildest of inconveniences", inline=True)
            embed.add_field(name="💭 topic", value="Not sure what to talk about? Try this :D", inline=True)
            await interaction.response.send_message(embed=embed)

        elif category.lower() == "games":
            embed = discord.Embed(
                title="Games",
                description="Descriptions are provided below each command\n"
                            "[Support Server](https://discord.gg/fa3j7fpbA6/ 'Takes you to the official KoffeeBot "
                            "discord')",
                color=discord.Color.orange()
            )
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
            embed.add_field(name=":scissors: rps [choice]", value="Play a game of Rock, Paper, Scissors", inline=True)
            embed.add_field(name=":bowling: bowl", value="Enjoy some bowling\n", inline=True)
            embed.add_field(name="⭕ coinflip [choice]", value="Heads or Tails!!!",inline=True)
            embed.add_field(name="❓ guess", value="Guess the number game!", inline=True)
            embed.add_field(name="🥊 fight [user]", value="Fight to the death!", inline=True)
            await interaction.response.send_message(embed=embed)

        elif category.lower() == "economy":  # economy
            embed = discord.Embed(
                title="Economy",
                description="Descriptions are provided below each command\n"
                            "[Support Server](https://discord.gg/fa3j7fpbA6/ 'Takes you to the official KoffeeBot "
                            "discord')",
                color=discord.Color.orange()
            )
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
            embed.add_field(name="💳 bal", value="Check your balance/ open an account")
            embed.add_field(name='💼 inv', value="Displays your inventory")
            embed.add_field(name=':calendar: daily', value="Receive your daily amount of <:KoffeeKoin:939562780363726868>")
            embed.add_field(name=':screwdriver: work', value="Start working for some <:KoffeeKoin:939562780363726868>")
            embed.add_field(name='⏰ jobs', value="You might need a job to earn <:KoffeeKoin:939562780363726868>")
            embed.add_field(name='🗄️ resign', value="Quit your current job")
            embed.add_field(name='🙏 beg', value="Beg for people to give you <:KoffeeKoin:939562780363726868>")
            embed.add_field(name='🍀 lucky', value="Do you think you're lucky?")
            embed.add_field(name=":diamonds: scam", value="So now you're taking people's money?")
            embed.add_field(name='💼 withdraw [amount]', value="Withdraw money from the bank")
            embed.add_field(name='💸 give [user] [amount] [item]', value="Give the poor people their money")
            embed.add_field(name='🏛️ dep [amount]', value="Deposit <:KoffeeKoin:939562780363726868> into your bank account.")
            embed.add_field(name='🛒 shop', value="Opens up the KoffeeBot shop")
            embed.add_field(name='🛍️ buy [item] [amount]', value="Buy an item from the shop")
            embed.add_field(name='💰 sell [item] [amount]', value="Sell an item from your inventory")
            embed.add_field(name=':smiling_imp: steal [user]', value="Attemp to steal <:KoffeeKoin:939562780363726868> from someone")
            embed.add_field(name='🍽️ recipes', value="Shows all craftable items")
            embed.add_field(name='⛏ craft [item] [amount]', value="Craft an item")
            embed.add_field(name=':slot_machine: slots [amount]', value="Risk it all with the slot machine!")
            embed.add_field(name='💎 rich', value="View the richest KoffeeBot users in your discord")

            await interaction.response.send_message(embed=embed)

        elif category.lower() == "images":  # Images
            embed = discord.Embed(
                title="Image Manipulation",
                description="Descriptions are provided below each command\n"
                            "[Support Server](https://discord.gg/fa3j7fpbA6/ 'Takes you to the official KoffeeBot "
                            "discord')",
                color=discord.Color.orange()
            )
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
            embed.add_field(name=":detective: wanted", value="Shows your wanted picture", inline=True)
            embed.add_field(name=":coffin: rip", value="You died?", inline=True)
            embed.add_field(name=":punch: hit [user]", value="Punch someone!\n", inline=True)
            embed.add_field(name=":dancer: dance", value="Enjoy some cool dance moves!", inline=True)
            embed.add_field(name=":clap: slap [user]", value="Slap someone!", inline=True)
            embed.add_field(name=":hugging: hug [user]", value="Hug someone", inline=True)
            embed.add_field(name=":broken_heart: ship [user]", value="See you chances of shipping with someone",
                            inline=True)
            embed.add_field(name=":japanese_ogre: evil", value="Are you really that evil?", inline=True)
            embed.add_field(name=":gun: shoot [user]", value="Shoot someone", inline=True)
            embed.add_field(name=":rage: angry", value="Let all that rage out", inline=True)
            embed.add_field(name=":eyes: threaten [user]", value="Make sure this person stays quiet",
                            inline=True)
            await interaction.response.send_message(embed=embed)

        elif category.lower() == "mafia":
            embed = discord.Embed(
                title="Mafia",
                description="Descriptions are provided below each command\n"
                            "[Support Server](https://discord.gg/fa3j7fpbA6/ 'Takes you to the official KoffeeBot "
                            "discord')",
                color=discord.Color.orange()
            )
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
            embed.add_field(name="<:hat:984285090190360657> mafia", value="Displays your mafia profile", inline=True)
            embed.add_field(name="🚬 mafia create [name]", value="Create a mafia", inline=True)
            embed.add_field(name="✉ mafia invite [user]", value="Invite someone into your mafia", inline=True)
            embed.add_field(name="👌 promote [user]", value="Promote someone in your mafia", inline=True)
            embed.add_field(name="🦴 demote [user]", value="Demote someone in your mafia", inline=True)
            embed.add_field(name="👞 mafia kick [target]", value="Kick someone from your mafia", inline=True)
            embed.add_field(name="💼 mafia leave", value="Leave your current mafia", inline=True)
            embed.add_field(name="🧨 mafia delete", value="Delete a mafia you have created", inline=True)
            embed.add_field(name="🧱 heist [target]", value="Attemp to rob someone's bank account", inline=True)
            embed.add_field(name="🔑 vault withdraw [amount]", value="Withdraw <:KoffeeKoin:939562780363726868> from your vault", inline=True)
            embed.add_field(name="🗝️ vault deposit [amount]", value="Deposit <:KoffeeKoin:939562780363726868> into your vault", inline=True)
            await interaction.response.send_message(embed=embed)

        else:
            await interaction.response.send_message("Please enter a valid category")


async def setup(bot):
    await bot.add_cog(commandsInfo(bot))
