import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice


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
        await interaction.response.send_message(f"Added the {role} role to {member}", ephemeral=True)

    @app_commands.command(name="removerole", description="Remove a role from a user")  # remove role
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(role="The role you wish to remove",
                           member="The user you wish to remove the role from")
    async def removerole(self, interaction: discord.Interaction, role: discord.Role, member: discord.Member):
        await member.remove_roles(role)
        await interaction.response.send_message(f"Removed the {role} role from {member}", ephemeral=True)

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
        embed.add_field(name="Server Join Date:", value=joined_date, inline=True)
        embed.add_field(name="> Account Creation Date:", value=f"> {create_date}", inline=True)
        if len(mention) > 0:
            embed.add_field(name=f"Roles: ({len(mention)})", value=' '.join(f"{role}" for role in mention),
                            inline=False)
        if len(perms) > 0:
            embed.add_field(name="Key Permissions:", value=', '.join(f"{perm}" for perm in perms), inline=False)
        embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text=f"ID: {member.id}", )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(moderation(bot))
