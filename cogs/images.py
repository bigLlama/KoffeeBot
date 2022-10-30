import discord
from discord.ext import commands
import random
from discord import app_commands
from discord.app_commands import Choice
from PIL import Image
from io import BytesIO


class images(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="ship", description="Check your compatibility status with another user")  # Ship probability
    @app_commands.describe(target="The user you wish to be shipped with")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ship(self, interaction: discord.Interaction, target: discord.Member):
        random_number = str(random.randrange(1, 100))

        ships = Image.open("media/ship.png")
        asset1 = interaction.user.avatar
        data1 = BytesIO(await asset1.read())
        pfp1 = Image.open(data1)
        pfp1 = pfp1.resize((318, 318))
        ships.paste(pfp1, (12, 14))

        asset2 = target.avatar
        data2 = BytesIO(await asset2.read())
        pfp2 = Image.open(data2)
        pfp2 = pfp2.resize((318, 318))
        ships.paste(pfp2, (636, 14))
        ships.save("media/ships.png")
        await interaction.response.send_message(file=discord.File("media/ships.png"))

        await interaction.followup.send(
            f"The probability of you shipping with {target} is **{random_number}%**")

    @commands.command()  # wanted command
    @commands.cooldown(1, 5, commands.BucketType.user)
    @app_commands.describe(member="The user you wish to be wanted")
    async def wanted(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        want = Image.open("media/wanted.jpg")
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((255, 256))
        want.paste(pfp, (97, 200))
        want.save("media/want.jpg")

        await ctx.send(file=discord.File("media/want.jpg"))

    @commands.command(aliases=["death", "die"])  # rip command
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rip(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        ded = Image.open("media/rip.png")
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((125, 125))
        ded.paste(pfp, (88, 150))
        ded.save("media/ded.png")

        await ctx.send(file=discord.File("media/ded.png"))

    @commands.command(aliases=["hit"])  # punch command
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def punch(self, ctx, target: discord.Member):

        hit = Image.open("media/punch.jpg")
        asset1 = ctx.author.avatar_url_as(size=128)
        data = BytesIO(await asset1.read())
        pfp1 = Image.open(data)
        pfp1 = pfp1.resize((80, 80))
        hit.paste(pfp1, (40, 220))

        asset2 = target.avatar_url_as(size=128)
        data = BytesIO(await asset2.read())
        pfp2 = Image.open(data)
        pfp2 = pfp2.resize((80, 80))
        hit.paste(pfp2, (160, 50))

        asset3 = target.avatar_url_as(size=128)
        data = BytesIO(await asset3.read())
        pfp3 = Image.open(data)
        pfp3 = pfp3.resize((80, 80))
        hit.paste(pfp3, (430, 340))
        hit.save("media/hit.jpg")

        await ctx.send(file=discord.File("media/hit.jpg"))

    @commands.command()  # slap command
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slap(self, ctx, target: discord.Member):

        slaps = Image.open("media/slap.jpg")
        asset1 = ctx.author.avatar_url_as(size=128)
        data = BytesIO(await asset1.read())
        pfp1 = Image.open(data)
        pfp1 = pfp1.resize((80, 80))
        slaps.paste(pfp1, (219, 87))

        asset2 = target.avatar_url_as(size=128)
        data = BytesIO(await asset2.read())
        pfp2 = Image.open(data)
        pfp2 = pfp2.resize((80, 80))
        slaps.paste(pfp2, (495, 120))
        slaps.save("media/slapped.jpg")

        await ctx.send(file=discord.File("media/slapped.jpg"))

    @commands.command()  # hug command
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, target: discord.Member):

        hugs = Image.open("media/hug.jpg")
        asset1 = ctx.author.avatar_url_as(size=128)
        data = BytesIO(await asset1.read())
        pfp1 = Image.open(data)
        pfp1 = pfp1.resize((70, 70))
        hugs.paste(pfp1, (60, 75))

        asset2 = target.avatar_url_as(size=128)
        data = BytesIO(await asset2.read())
        pfp2 = Image.open(data)
        pfp2 = pfp2.resize((70, 70))
        hugs.paste(pfp2, (150, 65))
        hugs.save("media/hugged.jpg")

        await ctx.send(file=discord.File("media/hugged.jpg"))

    @commands.command(aliases=['mad'])  # angry command
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def angry(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        hugs = Image.open("media/angry.jpg")
        asset1 = member.avatar_url_as(size=128)
        data = BytesIO(await asset1.read())
        pfp1 = Image.open(data)
        pfp1 = pfp1.resize((540, 540))
        hugs.paste(pfp1, (820, 20))

        asset2 = member.avatar_url_as(size=128)
        data = BytesIO(await asset2.read())
        pfp2 = Image.open(data)
        pfp2 = pfp2.resize((450, 450))
        hugs.paste(pfp2, (840, 965))
        hugs.save("media/mad.jpg")

        await ctx.send(file=discord.File("media/mad.jpg"))

    @commands.command(aliases=["devil"])  # evil command
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def evil(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        want = Image.open("media/evil.jpg")
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((120, 120))
        want.paste(pfp, (163, 72))
        want.save("media/devil.jpg")

        await ctx.send(file=discord.File("media/devil.jpg"))

    @commands.command()  # shoot command
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shoot(self, ctx, target: discord.Member):

        slaps = Image.open("media/shoot.png")
        asset1 = ctx.author.avatar_url_as(size=128)
        data = BytesIO(await asset1.read())
        pfp1 = Image.open(data)
        pfp1 = pfp1.resize((60, 60))
        slaps.paste(pfp1, (315, 23))

        asset2 = target.avatar_url_as(size=128)
        data = BytesIO(await asset2.read())
        pfp2 = Image.open(data)
        pfp2 = pfp2.resize((40, 40))
        slaps.paste(pfp2, (80, 101))
        slaps.save("media/shot.png")

        await ctx.send(file=discord.File("media/shot.png"))

    @commands.command(aliases=["threat", "blackmail"])  # threat command
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def threaten(self, ctx, target: discord.Member):

        slaps = Image.open("media/threat.png")
        asset1 = ctx.author.avatar_url_as(size=128)
        data = BytesIO(await asset1.read())
        pfp1 = Image.open(data)
        pfp1 = pfp1.resize((150, 150))
        slaps.paste(pfp1, (505, 150))

        asset2 = target.avatar_url_as(size=128)
        data = BytesIO(await asset2.read())
        pfp2 = Image.open(data)
        pfp2 = pfp2.resize((160, 160))
        slaps.paste(pfp2, (110, 135))
        slaps.save("media/threatened.png")

        await ctx.send(file=discord.File("media/threatened.png"))

    @commands.command(aliases=['party'])  # dance command
    async def dance(self, ctx):
        gifs = ['https://c.tenor.com/KsE4YxgXzqcAAAAd/hungarian-top-gamers2019hungary.gif',
                'https://cdn.discordapp.com/attachments/744639508880031775/948311371441926234/happy-pants.gif',
                'https://cdn.discordapp.com/attachments/744639508880031775/948311928567128094/funny-dance.gif']

        await ctx.send(random.choice(gifs))


async def setup(client):
    await client.add_cog(images(client))
