import discord
import sqlite3
from datetime import datetime
from discord.ext import commands
from discord import app_commands, Spotify
from discord.app_commands import Choice


def store_notes(user: discord.Member, user_note: str, server_id: int):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM notes WHERE id = {user.id} AND server_id = {server_id}")
    result = cursor.fetchone()

    current_date = datetime.today().strftime('%d %b %Y at %H:%M %p')

    if result:
        return None
    else:
        sql = "INSERT INTO notes(id, note, date, server_id) VALUES(?,?,?,?)"
        val = (user.id, user_note, current_date, server_id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

    return f"Created note for {user.name}"


def get_notes(user: discord.Member, server_id):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM notes WHERE id = {user.id} AND server_id = {server_id}")
    result = cursor.fetchone()

    return result


class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="clear", description="Clear away messy chat")  # clear command
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(amount="The amount of messages you wish to clear")
    async def clear(self, interaction: discord.Interaction, amount: int = 1):
        await interaction.response.defer()
        await interaction.channel.purge(limit=int(amount))


    @app_commands.command(name="addrole", description="Assign a role to a user")  # add role
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(role="The role you wish to add",
                           member="The user you wish to give the role to")
    async def addrole(self, interaction: discord.Interaction, role: discord.Role, member: discord.Member):
        await member.add_roles(role)

        embed = discord.Embed(title="Roles", description=f"Added the {role} role to {member}")
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="removerole", description="Remove a role from a user")  # remove role
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(role="The role you wish to remove",
                           member="The user you wish to remove the role from")
    async def removerole(self, interaction: discord.Interaction, role: discord.Role, member: discord.Member):
        await member.remove_roles(role)

        embed = discord.Embed(title="Roles", description=f"Removed the {role} role from {member}")
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="inspect", description="Show information about a user")  # inspect a user
    @app_commands.describe(member="The user you wish to inspect (Also works with user's id)")
    async def inspect(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        elif member == member.id:
            member = member

        key_perms = ["Administrator", "Manage_Server", "Manage_Roles", "Manage_Channels",
                     "Manage_Messages", "Manage_Webhooks", "Manage_Nicknames", "Manage_Emojis",
                     "Kick_Members", "Ban_Members", "Mention_Everyone", "View_Audit_Log", "Moderate_Members"]

        create_date = member.created_at
        create_date = create_date.strftime('%d %b %Y at %H:%M %p')
        joined_date = member.joined_at
        joined_date = joined_date.strftime('%d %b %Y at %H:%M %p')

        mention = []
        for role in member.roles:
            if "@everyone" == role.name:
                continue
            mention.append(role.mention)

        perms = []
        for perm in member.guild_permissions:
            if perm[1] is True:
                if perm[0].title() in key_perms:
                    perms.append(perm[0].title())

        embed = discord.Embed(description=member.mention, color=discord.Color.blue())
        embed.set_author(name=f"{member}", icon_url=member.avatar)
        embed.add_field(name="Server Join Date:", value=f"`{joined_date}`", inline=True)
        embed.add_field(name="> Account Creation Date:", value=f"> `{create_date}`", inline=True)
        if len(mention) > 0:
            embed.add_field(name=f"Roles: ({len(mention)})", value=' '.join(f"{role}" for role in mention),
                            inline=False)
        if len(perms) > 0:
            embed.add_field(name="Key Permissions:", value=', '.join(f"{perm}" for perm in perms), inline=False)
        embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text=f"ID: {member.id}")

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="addnote", description="Add notes for a server member")
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.describe(user="The member you wish to create a note for",
                           note="The note you wish to add to this member")
    async def addnote(self, interaction: discord.Interaction, user: discord.Member, note: str):
        guild_id = interaction.guild.id
        msg = store_notes(user, note, guild_id)

        if not msg:
            embed = discord.Embed(description=f"This user already has a saved note\n"
                                    f"To edit their existing note use /editnote",
                                  color=discord.Color.blue())
            return await interaction.response.send_message(embed=embed)

        await interaction.response.send_message(msg)

    @app_commands.command(name="notes", description="View notes for a server member")
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.describe(user="The user who's notes you wish to view")
    async def notes(self, interaction: discord.Interaction, user: discord.Member):
        guild_id = interaction.guild.id
        note = get_notes(user, guild_id)

        if not note:
            embed = discord.Embed(description="There are no notes for this user", color=discord.Color.blue())
            return await interaction.response.send_message(embed=embed)

        embed = discord.Embed(description=user.mention, color=discord.Color.blue())
        embed.set_author(name=user, icon_url=user.avatar)
        embed.add_field(name="Note added:", value=f"`{note[2]}`", inline=False)
        embed.add_field(name="Notes:", value=f"{note[1]}", inline=False)
        embed.set_thumbnail(url=user.avatar)
        embed.set_footer(text=f"ID: {user.id}")

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="editnote", description="Edit an existing member's notes")
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.describe(user="The member who's note you wish to edit",
                           note="The new note you wish to add")
    async def editnote(self, interaction: discord.Interaction, user: discord.Member, note: str):
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM notes WHERE id = {user.id}")
        old_note = cursor.fetchone()

        current_date = datetime.today().strftime('%d %b %Y at %H:%M %p')
        cursor.execute(f"UPDATE notes SET note = '{note}', date = '{current_date}' WHERE id = {user.id}")
        db.commit()

        embed = discord.Embed(description=f"Updated notes for {user.mention}\n\n"
                                          f"**From:**\n{old_note[1]}\n\n**To:**\n{note}",
                              color=discord.Color.blue())
        embed.set_author(name=user, icon_url=user.avatar)
        embed.set_thumbnail(url=user.avatar)

        await interaction.response.send_message(embed=embed)

        cursor.close()
        db.close()

    @app_commands.command(name="serverstats", description="View your servser statistics!")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def serverstats(self, interaction: discord.Interaction):
        guild = interaction.guild
        created = guild.created_at.strftime("%d/%m/%Y %H:%M:%S")
        total_members = guild.member_count
        total_channels = len(guild.channels)

        online_members = len([m for m in guild.members if m.status != discord.Status.offline])
        offline_members = guild.member_count - online_members


        embed = discord.Embed(title=f"Stats for {guild}",
                              color=discord.Color.blue())
        embed.add_field(name="Server Creation Date", value=f"`{created}`", inline=False)
        embed.add_field(name="Server Members", value=f"Online members: `{online_members}`\n"
                                          f"Offline members: `{offline_members}`\n"
                                          f"Total members: `{total_members}`\n\n"
                                          f"Channels: `{total_channels}`", inline=False)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"Guild ID: {guild.id}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="playing", description="Who is playing which game?")
    async def playing(self, interaction: discord.Interaction):
        members = interaction.guild.members
        playing_members = [member for member in members if
                           member.activity is not None and member.activity.type == discord.ActivityType.playing]
        print(playing_members)
        embed = discord.Embed(title='Currently Playing', description='\n'.join(
            f'**{member.name}** `{member.activity.name}`' for member in playing_members), color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)\


    @app_commands.command(name="listening", description="Who is listening to what?")
    async def listening(self, interaction: discord.Interaction):
        members = interaction.guild.members
        playing_members = [member for member in members if
                           member.activity is not None and member.activity.type == discord.ActivityType.listening]

        embed = discord.Embed(title='Currently Playing', description='\n'.join(
            f'**{member.name}** `{member.activity.title} | {member.activity.artist}`'
            for member in playing_members if isinstance(member.activity, discord.Spotify)), color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(moderation(bot))
