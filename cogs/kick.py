import discord
from discord import app_commands
from discord.ext import commands

class KickCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='kick', description='Kick a member from the server.')
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        embed = discord.Embed(
            title=f'{member.name} has been kicked',
            description=f'Reason: {reason}',
            color=discord.Color.red()
        )
        embed.set_footer(
            text=f'Kicked by {interaction.user.name}',
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None
        )

        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have enough permissions to kick this member.", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("Failed to kick the member due to an error.", ephemeral=True)

    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permission to kick members.", ephemeral=True)
        else:
            await interaction.response.send_message("An error occurred while trying to kick the member.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(KickCommand(bot))
