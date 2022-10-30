import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice



class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

        @client.tree.command(name="clear", description="Clear away messy chat")  # clear command
        @app_commands.checks.has_permissions(manage_messages=True)
        @app_commands.describe(amount="The amount of messages you wish to clear")
        async def clear(interaction: discord.Interaction, amount: int = 1):
            await interaction.channel.purge(limit=int(amount))

        @client.tree.command(name="kick", description="Kick a user from your server")  # kick command
        @app_commands.checks.has_permissions(kick_members=True)
        @app_commands.describe(member="The user you wish to kick",
                               reason="If you wish to provide a reason for kicking this user")
        async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
            await member.kick(reason=reason)
            await interaction.response.send_message(f"Kicked {member}")

        @client.tree.command(name="ban", description="Ban a user from your server")  # ban command
        @app_commands.checks.has_permissions(ban_members=True, administrator=True)
        @app_commands.describe(member="The user you wish to ban",
                               reason="If you wish to provide a reason for banning this user")
        async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
            await member.ban(reason=reason)
            await interaction.response.send_message(f"Banned {member}")

        @client.tree.command(name="unban", description="Unban a user from your server")  # unban command
        @app_commands.checks.has_permissions(ban_members=True, administrator=True)
        async def unban(interaction: discord.Interaction, member: discord.Member):
            banned_users = interaction.guild.bans()
            member_name, member_discriminator = member.split('#')

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await interaction.guild.unban(user)
                    await interaction.response.send_message(f"Unbanned {user.mention}")
                    return


        @client.tree.command(name="addrole", description="Assign a role to a user")  # add role
        @app_commands.checks.has_permissions(manage_roles=True)
        @app_commands.describe(role="The role you wish to add",
                               member="The user you wish to give the role to")
        async def addrole(interaction: discord.Interaction, role: discord.Role, member: discord.Member):
            await member.add_roles(role)
            await interaction.response.send_message(f"Added the {role} role to {member}", ephemeral=True)

        @client.tree.command(name="removerole", description="Remove a role from a user")  # remove role
        @app_commands.checks.has_permissions(manage_roles=True)
        @app_commands.describe(role="The role you wish to remove",
                               member="The user you wish to remove the role from")
        async def removerole(interaction: discord.Interaction, role: discord.Role, member: discord.Member):
            await member.remove_roles(role)
            await interaction.response.send_message(f"Removed the {role} role from {member}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(moderation(bot))
