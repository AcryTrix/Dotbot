import discord
from discord.ext import commands
from discord import app_commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help', description='Shows a list of available commands.')
    async def help_command(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            with open('./cogs/files/help.txt', 'r', encoding='utf-8') as file:
                help_text = file.read()

            embed = discord.Embed(title="Bot Commands", description=help_text, color=discord.Color.blue())
            await interaction.followup.send(embed=embed)

        except FileNotFoundError:
            await interaction.followup.send("The file with command information was not found.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
