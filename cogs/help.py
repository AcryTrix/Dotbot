import discord
from discord.ext import commands
from discord import app_commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help', description='Показывает список доступных команд.')
    async def help_command(self, interaction: discord.Interaction):
        try:
            with open('./cogs/files/help.txt', 'r', encoding='utf-8') as file:
                help_text = file.read()
            
            embed = discord.Embed(title="Команды бота", description=help_text, color=discord.Color.blue())
            await interaction.response.send_message(embed=embed)
        
        except FileNotFoundError:
            await interaction.response.send_message("Файл с информацией о командах не найден.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
