import discord
from discord import app_commands
from discord.ext import commands

class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="vote", description="Create a poll")
    @app_commands.describe(question="Question for the poll")
    async def vote(self, interaction: discord.Interaction, question: str):
        has_permissions = (
            interaction.user.guild_permissions.manage_messages or
            interaction.user.guild_permissions.create_public_threads
        )
        if not has_permissions:
            await interaction.response.send_message(
                "You don't have permission to create a poll. Required permissions: 'Manage Messages' or 'Create Public Threads'.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="Poll",
            description=question,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Created by: {interaction.user.display_name}")

        message = await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()

        await message.add_reaction("✅")
        await message.add_reaction("❌")

async def setup(bot: commands.Bot):
    await bot.add_cog(Vote(bot))
