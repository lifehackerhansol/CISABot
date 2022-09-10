#
# CISA 2022 Discord server bot
# Copyright (C) 2021-2022 lifehackerhansol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from inspect import cleandoc

import discord
from discord.ext import commands


class General(commands.Cog):
    """
    General commands
    """

    def __init__(self, bot):
        self.bot = bot

    async def simple_embed(self, ctx, text, *, title="", color=discord.Color.default()):
        embed = discord.Embed(title=title, color=color)
        embed.description = cleandoc(text)
        await ctx.send(embed=embed)

    @commands.command()
    async def about(self, ctx):
        await ctx.send("https://github.com/lifehackerhansol/CISABot")

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def outline(self, ctx):
        """List of class outlines"""
        await ctx.send_help(ctx.command)

    def outlineurl(self, number: int):
        return f"https://www.bcit.ca/outlines/{number}"

    @outline.command(name="programming")
    async def outline_programming(self, ctx):
        await ctx.send(self.outlineurl(20223045218))

    @outline.command(name="database")
    async def outline_database(self, ctx):
        await ctx.send(self.outlineurl(20223045217))

    @outline.command(name="linux")
    async def outline_linux(self, ctx):
        await ctx.send(self.outlineurl(20223045216))

    @outline.command(name="windows")
    async def outline_windows(self, ctx):
        await ctx.send(self.outlineurl(20223045215))

    @outline.command(name="desktop")
    async def outline_desktop(self, ctx):
        await ctx.send(self.outlineurl(20223045214))

    @outline.command(name="networking")
    async def outline_networking(self, ctx):
        await ctx.send(self.outlineurl(20223045213))


async def setup(bot):
    await bot.add_cog(General(bot))
