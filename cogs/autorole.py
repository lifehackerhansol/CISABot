#
# Copyright (C) 2021-present lifehackerhansol
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

import discord
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
            if message.guild.id == self.bot.settings['GUILD'] and message.channel.id == self.bot.settings['WELCOME']:
                if message.content == "g":
                    return await message.author.add_roles(message.guild.get_role(self.bot.settings['SETG_ROLE']))
                elif message.content == "h":
                    return await message.author.add_roles(message.guild.get_role(self.bot.settings['SETH_ROLE']))
                elif message.content == "j":
                    return await message.author.add_roles(message.guild.get_role(self.bot.settings['SETJ_ROLE']))
                else:
                    return await message.channel.send("Invalid class. Try again.")


async def setup(bot):
    await bot.add_cog(Autorole(bot))
