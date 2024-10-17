import discord
from discord.ext import commands
from discord import app_commands

class ClearMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Clear messages in the chat")
    @app_commands.describe(amount="Number of messages to delete")
    async def clear(self, interaction: discord.Interaction, amount: int):
        if amount < 1 or amount > 100:
            await interaction.response.send_message("Please enter a number between 1 and 100.", ephemeral=True)
            return

        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("You do not have permission to manage messages.", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)
        deleted = await interaction.channel.purge(limit=amount + 1)

        embed = discord.Embed(
            title="Messages Deleted",
            description=f"Deleted messages: {len(deleted) - 1}",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Deleted by: {interaction.user.name}", icon_url=interaction.user.avatar.url)

        response_message = await interaction.channel.send(embed=embed)
        await response_message.delete(delay=10)

async def setup(bot):
    await bot.add_cog(ClearMessages(bot))
