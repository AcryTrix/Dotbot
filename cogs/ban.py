import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import re

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banned_users = {}

    @app_commands.command(name='ban', description='Bans a user (temporarily or permanently).')
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None, duration: str = None):
        if duration:
            duration_timedelta = self.parse_duration(duration)
            if duration_timedelta is None:
                await interaction.response.send_message("Invalid time format. Use, for example, 5m, 1h, 1d.")
                return

            end_time = datetime.now() + duration_timedelta
            self.banned_users[member.id] = end_time
            await member.ban(reason=reason)
            await interaction.response.send_message(embed=self.create_ban_embed(member, reason, duration_timedelta, interaction.user))
            await self.schedule_unban(member, end_time)
        else:
            await member.ban(reason=reason)
            await interaction.response.send_message(embed=self.create_ban_embed(member, reason, None, interaction.user))

    @app_commands.command(name='unban', description='Unbans a user.')
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, member: str):
        user_id = int(member.split("#")[1])
        try:
            user = await self.bot.fetch_user(user_id)
            await interaction.guild.unban(user)
            if user_id in self.banned_users:
                del self.banned_users[user_id]
            await interaction.response.send_message(f'{user.name} has been successfully unbanned.')
        except discord.NotFound:
            await interaction.response.send_message("User not found.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}")

    def create_ban_embed(self, member, reason, duration, author):
        embed = discord.Embed(
            title=f'User Banned: {member.name}',
            description=f'**Reason:** {reason}\n' +
                        (f'**Ban Duration:** {duration}\n' if duration else ''),
            color=discord.Color.red(),
        )
        embed.set_footer(text=f'Banned by: {author.name}', icon_url=author.avatar.url)
        return embed

    async def schedule_unban(self, member, end_time):
        await discord.utils.sleep_until(end_time)
        await member.unban(reason="Temporary ban expired.")
        if member.id in self.banned_users:
            del self.banned_users[member.id]

    def parse_duration(self, duration_str):
        duration_regex = r'(\d+)([smhd])'
        matches = re.findall(duration_regex, duration_str)

        total_duration = timedelta()
        for value, unit in matches:
            value = int(value)
            if unit == 's':
                total_duration += timedelta(seconds=value)
            elif unit == 'm':
                total_duration += timedelta(minutes=value)
            elif unit == 'h':
                total_duration += timedelta(hours=value)
            elif unit == 'd':
                total_duration += timedelta(days=value)

        return total_duration if total_duration else None

async def setup(bot):
    await bot.add_cog(BanCog(bot))
