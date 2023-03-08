#!/usr/bin/env python3

#
# CISA 2022 Discord server bot
# Copyright (C) 2021-2023 lifehackerhansol
#
# SPDX-License-Identifier: Apache-2.0
#

import asyncio
import os
from typing import Any, Dict

import aiohttp
import discord
from discord.ext import commands

import config
from utils.utils import create_error_embed


class CISABot(commands.Bot):
    def __init__(self, settings: Dict[str, Any]):
        intents = discord.Intents(guilds=True, members=True, bans=True, messages=True, message_content=True)
        self.settings = settings
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False)
        super().__init__(
            command_prefix=[x for x in settings['PREFIX']],
            intents=intents,
            allowed_mentions=allowed_mentions,
            status=discord.Status.online,
            case_insensitive=True
        )

    async def load_cogs(self):
        cog = ""
        for filename in os.listdir("./cogs"):
            try:
                if filename.endswith(".py"):
                    cog = f"cogs.{filename[:-3]}"
                    await self.load_extension(cog)
                    print(f"Loaded cog cogs.{filename[:-3]}")
            except Exception as e:
                exc = "{}: {}".format(type(e).__name__, e)
                print(f"Failed to load cog {cog}\n{exc}")
        try:
            await self.load_extension("jishaku")
            print("Loaded cog jishaku")
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print(f"Failed to load cog jishaku\n{exc}")

    async def on_ready(self):
        await self.load_cogs()
        print("CISABot ready.")

    async def on_command_error(self, ctx: commands.Context, exc: commands.CommandInvokeError):
        author: discord.Member = ctx.author
        command: commands.Command = ctx.command or '<unknown cmd>'
        exc = getattr(exc, 'original', exc)
        channel = ctx.channel

        if isinstance(exc, commands.CommandNotFound):
            return

        elif isinstance(exc, commands.ArgumentParsingError):
            await ctx.send_help(ctx.command)

        elif isinstance(exc, commands.NoPrivateMessage):
            await ctx.send(f'`{command}` cannot be used in direct messages.')

        elif isinstance(exc, commands.MissingPermissions):
            await ctx.send(f"{author.mention} You don't have permission to use `{command}`.")

        elif isinstance(exc, commands.CheckFailure):
            await ctx.send(f'{author.mention} You cannot use `{command}`.')

        elif isinstance(exc, commands.BadArgument):
            await ctx.send(f'{author.mention} A bad argument was given: `{exc}`\n')
            await ctx.send_help(ctx.command)

        elif isinstance(exc, commands.BadUnionArgument):
            await ctx.send(f'{author.mention} A bad argument was given: `{exc}`\n')

        elif isinstance(exc, commands.BadLiteralArgument):
            await ctx.send(f'{author.mention} A bad argument was given, expected one of {", ".join(exc.literals)}')

        elif isinstance(exc, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention} You are missing required argument {exc.param.name}.\n')
            await ctx.send_help(ctx.command)

        elif isinstance(exc, discord.NotFound):
            await ctx.send("ID not found.")

        elif isinstance(exc, discord.Forbidden):
            await ctx.send(f"💢 I can't help you if you don't let me!\n`{exc.text}`.")

        elif isinstance(exc, commands.CommandInvokeError):
            await ctx.send(f'{author.mention} `{command}` raised an exception during usage')
            embed = create_error_embed(ctx, exc)
            await channel.send(embed=embed)
        else:
            await ctx.send(f'{author.mention} Unexpected exception occurred while using the command `{command}`')
            embed = create_error_embed(ctx, exc)
            await channel.send(embed=embed)


async def mainprocess():
    settings = config.loadSettings()
    bot = CISABot(settings)
    bot.help_command = commands.DefaultHelpCommand()
    bot.session = aiohttp.ClientSession()
    print('Starting bot...')
    await bot.start(settings['TOKEN'])


if __name__ == '__main__':
    asyncio.run(mainprocess())
