import discord
from discord import app_commands
from discord.ext import commands

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="info", description="Shows the server information, including member counts.")
    async def info(self, interaction: discord.Interaction):
        guild = interaction.guild
        total_members = guild.member_count
        humans = len([member for member in guild.members if not member.bot])
        bots = total_members - humans

        embed = discord.Embed(
            title=f"Server Info: {guild.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Total Members", value=total_members, inline=False)
        embed.add_field(name="Humans", value=humans, inline=True)
        embed.add_field(name="Bots", value=bots, inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
