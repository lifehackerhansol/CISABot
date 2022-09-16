#
# CISA 2022 Discord server bot
# Copyright (C) 2021-2022 lifehackerhansol
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#

from discord.ext import commands


class General(commands.Cog):
    """
    General commands
    """

    def __init__(self, bot):
        self.bot = bot

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
