import discord
from discord.ext import commands
import asyncio

class ClearCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='clear', description='Clear the specified number of messages')
    async def clear(self, ctx: commands.Context, amount: int):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("You do not have permission to manage messages.", ephemeral=True)
            return

        if amount < 1 or amount > 100:
            await ctx.send("Please specify an amount between 1 and 100.", ephemeral=True)
            return

        deleted = await ctx.channel.purge(limit=amount+1)

        embed = discord.Embed(title='Messages Cleared', color=0xFFFF00)
        if len(deleted) == 0:
            embed.description = 'No messages were deleted.'
        else:
            if len(deleted) == 1:
                embed.description = '1 message was deleted.'
            else:
                embed.description = f'{len(deleted) - 1} messages were deleted.'

        embed.set_thumbnail(url=ctx.author.avatar.url)
        message = await ctx.send(embed=embed)

        await asyncio.sleep(7)
        await message.delete()

async def setup(bot: commands.Bot):
    await bot.add_cog(ClearCog(bot))
