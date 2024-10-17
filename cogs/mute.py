import discord
from discord import app_commands
from discord.ext import commands
import re
import asyncio

class MuteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mute", description="Mute a member for a specified time")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: str = "No reason provided"):
        await interaction.response.defer()

        if not interaction.user.guild_permissions.manage_roles:
            embed = discord.Embed(
                title="Error",
                description="You don't have permission to manage roles.",
                color=discord.Color.red()
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)

        if not interaction.guild.me.guild_permissions.manage_roles:
            embed = discord.Embed(
                title="Error",
                description="I don't have permission to manage roles.",
                color=discord.Color.red()
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)

        mute_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await interaction.guild.create_role(name="Muted")

            for channel in interaction.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False, add_reactions=False, speak=False)
        else:
            for channel in interaction.guild.channels:
                overwrite = channel.overwrites_for(mute_role)
                overwrite.send_messages = False
                overwrite.add_reactions = False
                overwrite.speak = False
                await channel.set_permissions(mute_role, overwrite=overwrite)

        if mute_role in member.roles:
            embed = discord.Embed(
                title="Error",
                description=f"{member.mention} is already muted.",
                color=discord.Color.red()
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)

        await member.add_roles(mute_role, reason=reason)

        time_seconds = self.parse_duration(duration)
        if time_seconds:
            embed = discord.Embed(
                title=f"User Muted: {member.display_name}",
                description=f"**Reason:** {reason}\n**Duration:** {duration}",
                color=discord.Color.orange()
            )
            embed.set_footer(text=f"Muted by: {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)

            await asyncio.sleep(time_seconds)
            await member.remove_roles(mute_role)

            unmute_embed = discord.Embed(
                title="User Unmuted",
                description=f"{member.mention} has been unmuted after {duration}.",
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=unmute_embed)

    @app_commands.command(name="unmute", description="Unmute a member")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()

        if not interaction.user.guild_permissions.manage_roles:
            embed = discord.Embed(
                title="Error",
                description="You don't have permission to manage roles.",
                color=discord.Color.red()
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)

        if not interaction.guild.me.guild_permissions.manage_roles:
            embed = discord.Embed(
                title="Error",
                description="I don't have permission to manage roles.",
                color=discord.Color.red()
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)

        mute_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not mute_role or mute_role not in member.roles:
            embed = discord.Embed(
                title="Error",
                description=f"{member.mention} is not muted.",
                color=discord.Color.red()
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)

        await member.remove_roles(mute_role)

        embed = discord.Embed(
            title=f"User Unmuted: {member.display_name}",
            description=f"**Reason:** Unmuted by {interaction.user.display_name}",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Unmuted by: {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
        await interaction.followup.send(embed=embed)

    def parse_duration(self, duration: str):
        match = re.match(r'(\d+)([smh])', duration)
        if not match:
            return None

        amount, unit = match.groups()
        amount = int(amount)

        if unit == 's':
            return amount
        elif unit == 'm':
            return amount * 60
        elif unit == 'h':
            return amount * 3600

        return None

    @mute.error
    @unmute.error
    async def command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(
                title="Error",
                description="You don't have permission to use this command.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="Error",
                description="An error occurred while executing the command.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(MuteCog(bot))
