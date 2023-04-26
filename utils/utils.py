#
# CISA 2022 Discord server bot
# Portions Copyright (C) 2020 Nintendo Homebrew
# Copyright (C) 2021-2023 lifehackerhansol
#
# SPDX-License-Identifier: Apache-2.0
#

import traceback

import discord
from discord.ext import commands


async def send_dm_message(member: discord.Member, message: str, ctx: commands.Context = None, **kwargs) -> bool:
    """A helper function for sending a message to a member's DMs.

    Returns a boolean indicating success of the DM
    and notifies of the failure if ctx is supplied."""
    try:
        await member.send(message, **kwargs)
        return True
    except (discord.HTTPException, discord.Forbidden, discord.NotFound, AttributeError):
        if ctx:
            await ctx.send(f"Failed to send DM message to {member.mention}")
        return False


def command_signature(command, *, prefix=".") -> str:
    """Helper function for a command signature

    Parameters
    -----------
    command: :class:`discord.ext.commands.Command`
        The command to generate a signature for
    prefix: str
        The prefix to include in the signature"""
    signature = f"{discord.utils.escape_markdown(prefix)}{command.qualified_name} {command.signature}"
    return signature


def create_error_embed(ctx, exc) -> discord.Embed:
    embed = discord.Embed(title=f"Unexpected exception in command {ctx.command}", color=0xe50730)
    trace = "".join(traceback.format_exception(type(exc), value=exc, tb=exc.__traceback__))
    embed.description = f'```py\n{trace}```'
    embed.add_field(name="Exception Type", value=exc.__class__.__name__)
    embed.add_field(name="Information", value=f"channel: {ctx.channel.mention if isinstance(ctx.channel, discord.TextChannel) else 'Direct Message'}\ncommand: {ctx.command}\nmessage: {ctx.message.content}\nauthor: {ctx.author.mention}", inline=False)
    return embed


def is_guild_owner():
    async def predicate(ctx):
        if ctx.author == ctx.guild.owner:
            return True
        return False
    return commands.check(predicate)


def is_staff():
    def predicate(ctx):
        if not ctx.guild:
            return False
        return any((role.id in ctx.bot.settings['staff_roles'] or role.name in ctx.bot.settings['staff_roles']) for role in ctx.message.author.roles) if not ctx.author == ctx.guild.owner else True
    return commands.check(predicate)
