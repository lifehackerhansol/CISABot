#
# CISA 2022 Discord server bot
# Copyright (C) 2021-2023 lifehackerhansol
#
# SPDX-License-Identifier: Apache-2.0
#

from discord.ext import commands


class Autorole(commands.Cog):
    """
    Automatic roles!
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # avoid a stupid race condition, apparently the bot checks its own messages. What?
        if message.author.id != self.bot.user.id:
            if message.guild is not None:
                if message.guild.id == self.bot.settings['GUILD'] and message.channel.id == self.bot.settings['WELCOME']:
                    await message.delete()
                    if message.content.lower() == "g":
                        return await message.author.add_roles(message.guild.get_role(self.bot.settings['SETG_ROLE']))
                    elif message.content.lower() == "h":
                        return await message.author.add_roles(message.guild.get_role(self.bot.settings['SETH_ROLE']))
                    elif message.content.lower() == "j":
                        return await message.author.add_roles(message.guild.get_role(self.bot.settings['SETJ_ROLE']))
                    elif message.content.lower() == "f":
                        return await message.author.add_roles(message.guild.get_role(self.bot.settings['DEFAULT_ROLE']))
                    else:
                        return await message.channel.send(content="Invalid class. Try again.", delete_after=10)


async def setup(bot):
    await bot.add_cog(Autorole(bot))
