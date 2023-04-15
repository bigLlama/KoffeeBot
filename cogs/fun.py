import discord
from discord import app_commands
from discord.ext import commands
import random
import praw
import re


class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="meme", description="Enjoy some quality memes!")
    async def meme(self, interaction: discord.Interaction):
        reddit = praw.Reddit(client_id='WPQU7NjhT4M9zTKCVxoRzQ',
                             client_secret='jSKwzWRALcXyWtZ_e6ZiNGfO-Kvg5A',
                             user_agent='pythonprawmeme')

        meme_submissions = reddit.subreddit('memes').hot()
        post_to_pick = random.randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in meme_submissions if not x.stickied)
        await interaction.response.send_message(submission.url)

    @app_commands.command(name="roast", description="Roast someone")  # Roast (Add more roasts in future)
    @app_commands.describe(person="The person you wish to roast")
    async def roast(self, interaction: discord.Interaction, person: discord.Member = None):
        if person is None:
            person = interaction.user

        roasts = ["You are so ugly you made a happy meal cry",
                  "I'll never forget the first time I met you, but i will keep on trying",
                  "Don't be ashamed of who you are. That's your parents' job",
                  "You are like a cloud. Once you disappear, it's a lovely day",
                  "You were born on the highway, next to all the other accidents",
                  "You have your whole life to be a jerk, why not take a day off?",
                  "It's funny to think that out of all the choices you could have made, "
                  "you decided to wake up for another day",
                  "If I throw a stick, will you leave?",
                  "I thought of you today. It reminded me to take out the trash",
                  "You are the reason why shampoo bottles have instructions",
                  "Mirrors can't talk back. Luckily they can't laugh either",
                  "You are mentally handicapped",
                  "You seem like the type of person who would know what each type of crayon tastes like",
                  "Even skunks run when they smell you",
                  "When I look at you, I wish I could meet you again for the first time… and walk past.",
                  "You have such a beautiful face… But let’s put a bag over that personality.",
                  "There is someone out there for everyone. For you, it’s a therapist.",
                  "Whoever told you to be yourself, gave you a bad advice.",
                  "Everyone is allowed to act stupid once, but you… you are abusing that privilege.",
                  "Where is your off button?",
                  "Earth is full. Go home.",]

        embed = discord.Embed(
            title="Roast-inator",
            color=discord.Color.blue())
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')

        embed.add_field(name=f"{person}", value=random.choice(roasts) + " :joy:", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="insult", description="Curse someone with the slightest of inconviences")
    @app_commands.describe(user="The person you wish to insult")
    async def insult(self, interaction: discord.Interaction, user: discord.Member = None):
        if user is None:
            user = interaction.user

        troubles = ["I hope there's hole in your sock perfectly fitting for your big toe to slide through",
                    "I hope your phone charger only works at a specific angle",
                    "I hope someone eats your food that you've stored in the fridge",
                    "I hope you can't find your keys when you're in a rush",
                    "I hope you get stung by a bee",
                    "I hope you step on a lego",
                    "I hope you can't find the light switch at night",
                    "I hope your pillow case keeps sliding off",
                    "I hope your favourite snack is always out of stock at the store",
                    "I hope you're never able to close the door on the first try",
                    "I hope your earphones are always tangled when you are about to use them",
                    "I hope the next time someone leaves your room they leave the door open",
                    "I hope you get 3 ads on Youtube before getting to watch your video",
                    "I hope the next time you watch a video it keeps buffering every 5 seconds",
                    "I hope the next time you wake up your phone didn't charge overnight",
                    "I hope that you insert a USB wrong at least twice before getting it right"]

        embed = discord.Embed(
            title="Mild inconveniences", color=discord.Color.blue())
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
        embed.add_field(name=f"{user.name}", value=random.choice(troubles) + " :sparkles:", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="8ball", description="Ask a question and have it answered by the magical 8ball")  # 8ball
    @app_commands.describe(question="Your question")
    async def _8ball(self, interaction: discord.Interaction, question: str):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes definitely.",
                     "You may rely on it.",
                     " As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]

        embed = discord.Embed(
            title="Magic 8-ball",
            color=discord.Color.blue())
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')

        embed.add_field(name=f":8ball: Question: {question}", value=f":8ball: Answer: {random.choice(responses)}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="simp", description="Check how much of a SIMP you are")  # simp probability
    @app_commands.describe(person="The person you wish to target")
    async def simp(self, interaction: discord.Interaction, person: discord.Member = None):
        if person is None:
            person = interaction.user

        embed = discord.Embed(title="Simp machine", color=discord.Color.blue())
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
        embed.add_field(name=f"{person}", value="You are " + str(random.choices(range(1, 101))) + "% simp!")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="stupid", description="Check how smart you really are")  # Stupid probability
    @app_commands.describe(person="The person you wish to target")
    async def dumb(self, interaction: discord.Interaction, person: discord.Member = None):
        if person is None:
            person = interaction.user

        embed = discord.Embed(title="Dumb calculator", color=discord.Color.blue())
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
        embed.add_field(name=f"{person}", value="You are " + str(random.choices(range(1, 101))) + "% stupid!")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="laugh", description="KoffeeBot will respond accordingly")  # laugh command
    async def laugh(self, interaction: discord.Interaction):
        laughs = ['haha',
                  'lol',
                  'haha lol',
                  "Why? I don't see anything funny",
                  'lmao',
                  'no',
                  "Nothing's funny except your face..."]
        await interaction.response.send_message(random.choice(laughs))

    @app_commands.command(name="o", description="Replace every vowel with the letter 'o'")
    @app_commands.describe(msg="Your message that will be transformed!")
    async def o(self, interaction: discord.Interaction, msg: str):
        msg = msg.lower()
        x = ''
        vowels = ['a', 'e', 'i', 'u']

        for i in range(len(vowels)):
            x = re.sub(vowels[i], 'o', msg)
            msg = x

        embed = discord.Embed(title=x, color=discord.Color.blue())
        embed.set_footer(text="inspired by Chorry")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="topic", description="Can't think of a conversation starter. Let us help!")
    async def topic(self, interaction: discord.Interaction):
        f = open("topics.txt", encoding="utf8").read().splitlines()
        rand_topic = random.choice(f)
        embed = discord.Embed(title="Topic generator", description=f"{rand_topic}", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(fun(bot))
