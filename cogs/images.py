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
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
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

    @app_commands.command(name="wanted", description="Shows your wanted picture")  # wanted command
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(member="The user you wish to be wanted")
    async def wanted(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        want = Image.open("media/wanted.jpg")
        asset = member.avatar
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((255, 256))
        want.paste(pfp, (97, 200))
        want.save("media/want.jpg")

        await interaction.response.send_message(file=discord.File("media/want.jpg"))

    @app_commands.command(name="rip", description="Show your tombstone")  # rip command
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(member="The user you wish to see dead")
    async def rip(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        ded = Image.open("media/rip.png")
        asset = member.avatar
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((125, 125))
        ded.paste(pfp, (88, 150))
        ded.save("media/ded.png")

        await interaction.response.send_message(file=discord.File("media/ded.png"))

    @app_commands.command(name="punch", description="Sometimes we all want to punch someone in the face")  # punch command
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(target="The user you wish to punch")
    async def punch(self, interaction: discord.Interaction, target: discord.Member):

        hit = Image.open("media/punch.jpg")
        asset1 = interaction.user.avatar
        data = BytesIO(await asset1.read())
        pfp1 = Image.open(data)
        pfp1 = pfp1.resize((80, 80))
        hit.paste(pfp1, (40, 220))

        asset2 = target.avatar
        data = BytesIO(await asset2.read())
        pfp2 = Image.open(data)
        pfp2 = pfp2.resize((80, 80))
        hit.paste(pfp2, (160, 50))

        asset3 = target.avatar
        data = BytesIO(await asset3.read())
        pfp3 = Image.open(data)
        pfp3 = pfp3.resize((80, 80))
        hit.paste(pfp3, (430, 340))
        hit.save("media/hit.jpg")

        await interaction.response.send_message(file=discord.File("media/hit.jpg"))

    @app_commands.command(name="slap", description="Slap someone who you think deserves it!")  # slap command
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(target="The user you wish to slap")
    async def slap(self, interaction: discord.Interaction, target: discord.Member):

        slaps = Image.open("media/slap.jpg")
        asset1 = interaction.user.avatar
        data = BytesIO(await asset1.read())
        pfp1 = Image.open(data)
        pfp1 = pfp1.resize((80, 80))
        slaps.paste(pfp1, (219, 87))

        asset2 = target.avatar
        data = BytesIO(await asset2.read())
        pfp2 = Image.open(data)
        pfp2 = pfp2.resize((80, 80))
        slaps.paste(pfp2, (495, 120))
        slaps.save("media/slapped.jpg")

        await interaction.response.send_message(file=discord.File("media/slapped.jpg"))

    @app_commands.command(name="hug", description="hug someone who needs it <3")  # hug command
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(target="The user you wish to hug")
    async def hug(self, interaction: discord.Interaction, target: discord.Member):

        hugs = Image.open("media/hug.jpg")
        asset1 = interaction.user.avatar
        data = BytesIO(await asset1.read())
        pfp1 = Image.open(data)
        pfp1 = pfp1.resize((70, 70))
        hugs.paste(pfp1, (60, 75))

        asset2 = target.avatar
        data = BytesIO(await asset2.read())
        pfp2 = Image.open(data)
        pfp2 = pfp2.resize((70, 70))
        hugs.paste(pfp2, (150, 65))
        hugs.save("media/hugged.jpg")

        await interaction.response.send_message(file=discord.File("media/hugged.jpg"))

    @app_commands.command(name="angry", description="Don't we all rage at some point?")  # angry command
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(member="The user you wish to see angry")
    async def angry(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        hugs = Image.open("media/angry.jpg")
        asset1 = member.avatar
        data = BytesIO(await asset1.read())
        pfp1 = Image.open(data)
        pfp1 = pfp1.resize((540, 540))
        hugs.paste(pfp1, (820, 20))

        asset2 = member.avatar
        data = BytesIO(await asset2.read())
        pfp2 = Image.open(data)
        pfp2 = pfp2.resize((450, 450))
        hugs.paste(pfp2, (840, 965))
        hugs.save("media/mad.jpg")

        await interaction.response.send_message(file=discord.File("media/mad.jpg"))

    @app_commands.command(name="evil", description="Wonder what it's like to be evil?")  # evil command
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(member="The user you wish to see evil")
    async def evil(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        want = Image.open("media/evil.jpg")
        asset = member.avatar
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((120, 120))
        want.paste(pfp, (163, 72))
        want.save("media/devil.jpg")

        await interaction.response.send_message(file=discord.File("media/devil.jpg"))

    @app_commands.command(name="shoot", description="No! don't shoot!")  # shoot command
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(target="The user you wish to shoot")
    async def shoot(self, interaction: discord.Interaction, target: discord.Member):

        slaps = Image.open("media/shoot.png")
        asset1 = interaction.user.avatar
        data = BytesIO(await asset1.read())
        pfp1 = Image.open(data)
        pfp1 = pfp1.resize((60, 60))
        slaps.paste(pfp1, (315, 23))

        asset2 = target.avatar
        data = BytesIO(await asset2.read())
        pfp2 = Image.open(data)
        pfp2 = pfp2.resize((40, 40))
        slaps.paste(pfp2, (80, 101))
        slaps.save("media/shot.png")

        await interaction.response.send_message(file=discord.File("media/shot.png"))

    @app_commands.command(name="blackmail", description="We can do this the easy way, or the hard way...")  # threat command
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(target="The user you wish to threaten")
    async def blackmail(self, interaction: discord.Interaction, target: discord.Member):

        slaps = Image.open("media/threat.png")
        asset1 = interaction.user.avatar
        data = BytesIO(await asset1.read())
        pfp1 = Image.open(data)
        pfp1 = pfp1.resize((150, 150))
        slaps.paste(pfp1, (505, 150))

        asset2 = target.avatar
        data = BytesIO(await asset2.read())
        pfp2 = Image.open(data)
        pfp2 = pfp2.resize((160, 160))
        slaps.paste(pfp2, (110, 135))
        slaps.save("media/threatened.png")

        await interaction.response.send_message(file=discord.File("media/threatened.png"))

    @app_commands.command(name="dance", description="Dance party!!!")  # dance command
    async def dance(self, interaction):
        gifs = ['https://c.tenor.com/KsE4YxgXzqcAAAAd/hungarian-top-gamers2019hungary.gif',
                'https://cdn.discordapp.com/attachments/744639508880031775/948311371441926234/happy-pants.gif',
                'https://cdn.discordapp.com/attachments/744639508880031775/948311928567128094/funny-dance.gif']

        await interaction.response.send_message(random.choice(gifs))


async def setup(client):
    await client.add_cog(images(client))
