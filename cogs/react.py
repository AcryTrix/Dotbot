import discord
from discord import app_commands
from discord.ext import commands

class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reaction", description="Adds a reaction to a message and grants a role upon reaction.")
    async def reaction(
        self, 
        interaction: discord.Interaction, 
        message_id: str, 
        emoji: str, 
        role: discord.Role, 
        permanent: bool = False
    ):
        if not interaction.user.guild_permissions.manage_roles:
            embed = discord.Embed(
                title="Error",
                description="You don't have permission to manage roles.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            channel = interaction.channel
            message = await channel.fetch_message(int(message_id))
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Could not find the message with ID: {message_id}. Error: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            await message.add_reaction(emoji)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Failed to add reaction: {emoji}. Error: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        def check(reaction, user):
            return reaction.message.id == message.id and str(reaction.emoji) == emoji and user != self.bot.user

        embed = discord.Embed(
            title="Success",
            description=f"Reaction {emoji} added to the message! Role {role.mention} will be granted upon reaction.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        while True:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            if role not in user.roles:
                try:
                    await user.add_roles(role)
                except Exception as e:
                    error_embed = discord.Embed(
                        title="Error",
                        description=f"Failed to grant role {role.name} to user {user.name}. Error: {e}",
                        color=discord.Color.red()
                    )
                    await interaction.channel.send(embed=error_embed)

            def check_reaction_remove(reaction, user):
                return reaction.message.id == message.id and user != self.bot.user

            reaction_remove, user_remove = await self.bot.wait_for('reaction_remove', check=check_reaction_remove)
            if not permanent:
                if role in user_remove.roles:
                    await user_remove.remove_roles(role)

async def setup(bot):
    await bot.add_cog(ReactionRole(bot))
