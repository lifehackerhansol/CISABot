#
# CISA 2022 Discord server bot
# Copyright (C) 2021-2023 lifehackerhansol
#
# SPDX-License-Identifier: Apache-2.0
#

import discord
from asyncio.exceptions import TimeoutError as AsyncTimeoutError
from discord.ext import commands
from mcstatus import JavaServer


class Minecraft(commands.Cog):
    """
    Checking Minecraft server status
    Only really supports one server
    """

    def __init__(self, bot):
        self.bot = bot
        self.mcserver = None
        if self.bot.settings["MCSERVER"]:
            self.mcserver = JavaServer.lookup(address=self.bot.settings["MCSERVER"], timeout=10)

    async def cog_check(self, ctx):
        if self.mcserver is None:
            raise commands.CheckFailure()
        return True

    @commands.command()
    async def mcping(self, ctx):
        async with ctx.typing():
            ping = await self.mcserver.async_ping()
            await ctx.send(f"Pong! The server responded in {ping:.3f} ms.")

    @commands.command()
    async def mcstatus(self, ctx):
        async with ctx.typing():
            try:
                status = await self.mcserver.async_status()
            except AsyncTimeoutError:
                return await ctx.send("Server timed out. Please try again later.")
            embed = discord.Embed(title=status.description)
            embed.add_field(name="Server Version", value=status.version.name, inline=False)
            embed.add_field(name="Players online", value=status.players.online, inline=False)
            embed.add_field(name="Latency", value=status.latency, inline=False)
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Minecraft(bot))
