import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

        @client.command(aliases=["delete", "del", "remove"])  # clear command
        @has_permissions(manage_messages=True)
        async def clear(ctx, amount=1):
                await ctx.channel.purge(limit=int(amount)+1)

        @client.command()  # kick command
        @has_permissions(administrator=True)
        async def kick(ctx, member: discord.Member, *, reason):
            await member.kick(reason=reason)
            await ctx.send("Get outta here")

        @client.command()  # ban command
        @has_permissions(administrator=True)
        async def ban(ctx, member: discord.Member, *, reason):
            await member.ban(reason=reason)
            await ctx.send("Be gone!")

        @client.command()  # unban command
        @has_permissions(administrator=True)
        async def unban(ctx, *, member):
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f"Unbanned {user.mention}")
                    return

        @client.command(aliases=["silence"])  # mute command
        @has_permissions(administrator=True)
        async def mute(ctx, member: discord.Member, *, reason):
            guild = ctx.guild
            role = discord.utils.get(ctx.guild.roles, name="Muted")

            if not role:
                role = await guild.create_role(name="Muted")

                for channel in guild.channels:
                    await channel.set_permissions(role, speak=False, send_messages=False)

            await member.add_roles(role, reason=reason)
            embed = discord.Embed(
                color=discord.Color.orange()
            )
            embed.add_field(name=f"Muted {member}",
                            value=f"Reason: {reason}",
                            inline=False)

            await ctx.send(embed=embed)

        @client.command()  # unmute command
        @has_permissions(administrator=True)
        async def unmute(ctx, member: discord.Member):
            role = discord.utils.get(ctx.guild.roles, name="Muted")

            await member.remove_roles(role)
            embed = discord.Embed(
                color=discord.Color.orange()
            )
            embed.add_field(name=f"Unmuted {member}",
                            value="Try not to cause trouble again",
                            inline=False)

            await ctx.send(embed=embed)

        @client.command(aliases=["ar", "giverole", "gr"])  # add role
        @has_permissions(administrator=True)
        async def addrole(ctx, role: discord.Role = None, member: discord.Member = None):
            if role is None:
                return await ctx.send("Please mention a role!")
            elif member is None:
                await ctx.send("Please mention someone!")
                return
            await member.add_roles(role)
            await ctx.send(f"*Added the {role} role to {member}*")

        @client.command(aliases=["rr", "tr", "takerole"])  # remove role
        @has_permissions(administrator=True)
        async def removerole(ctx, role: discord.Role = None, member: discord.Member = None):
            if role is None:
                return await ctx.send("Please mention a role!")
            elif member is None:
                await ctx.send("Please mention someone!")
                return
            await member.remove_roles(role)
            await ctx.send(f"*Removed the {role} role from {member}*")


async def setup(bot):
    await bot.add_cog(moderation(bot))
