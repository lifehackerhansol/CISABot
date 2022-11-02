#
# CISA 2022 Discord server bot
# Copyright (C) 2021-2022 lifehackerhansol
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#

from datetime import datetime, timedelta

from discord.ext import commands
from discord.utils import format_dt


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

    @commands.command(aliases=['remind', 'reminder'])
    async def remindme(self, ctx, remind_in: str, *, reminder: str):
        """Sends a reminder after a set time, just for you. Max reminder size is 800 characters.\n\nTime format: #d#h#m#s."""
        time = datetime.now()
        if (seconds := utils.parse_time(remind_in)) == -1:
            return await ctx.send("💢 I don't understand your time format.")
        if seconds < 30 or seconds > 3.154e+7:
            return await ctx.send("You can't set a reminder for less than 30 seconds or for more than a year.")
        if len(reminder) > 800:
            return await ctx.send("The reminder is too big! (Longer than 800 characters)")
        timestamp = datetime.utcnow()
        delta = timedelta(seconds=seconds)
        reminder_time = timestamp + delta
        await self.bot.db.add_reminder(ctx.author, ctx.channel, reminder_time, reminder)
        await ctx.send(f"I will send you a reminder on {format_dt(reminder_time, style='F')}.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(General(bot))
