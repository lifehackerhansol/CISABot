#
# CISA 2022 Discord server bot
# Copyright (C) 2021-2022 lifehackerhansol
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#

import discord
import tweepy.asynchronous
from discord.ext import commands

from utils.utils import is_staff


class UpdateStream(tweepy.asynchronous.AsyncStreamingClient):
    def __init__(self, bearer_key, channel_target):
        self.channel = channel_target
        super().__init__(bearer_key)

    async def on_tweet(self, tweet):
        embed = discord.Embed(timestamp=tweet.created_at)
        embed.author = f"{tweet.fields.user.name} (@{tweet.fields.user.username})"
        embed.description = tweet.text
        await self.channel.send(embed=embed)


class Twitter(commands.Cog):
    """
    Twitter polling
    """

    def __init__(self, bot):
        self.bot = bot
        if all([
            bot.settings['TWITTER_BEARER'],
            bot.settings['BUSUPDATES'],
            bot.settings['GUILD']
        ]):
            self.updatestream = UpdateStream(
                bot.settings['TWITTER_BEARER'],
                bot.get_guild(bot.settings['GUILD']).get_channel(bot.settings['BUSUPDATES'])
            )
        if all([
            bot.settings['TWITTER_APIKEY'],
            bot.settings['TWITTER_APISECRET'],
            bot.settings['TWITTER_TOKEN'],
            bot.settings['TWITTER_TOKENSECRET']
        ]):
            print(bot.settings['TWITTER_APIKEY'])
            print(bot.settings['TWITTER_APISECRET'])
            print(bot.settings['TWITTER_TOKEN'])
            print(bot.settings['TWITTER_TOKENSECRET'])
            self.twitter = tweepy.asynchronous.Client(
                consumer_key=bot.settings['TWITTER_APIKEY'],
                consumer_secret=bot.settings['TWITTER_APISECRET'],
                access_token=bot.settings['TWITTER_TOKEN'],
                access_token_secret=bot.settings['TWITTER_TOKENSECRET']
            )

    @is_staff()
    @commands.command()
    async def follow(self, ctx, username: str):
        user_response = await self.twitter.get_user(username=username, user_auth=True)
        await self.twitter.follow_user(user_response.data.id, user_auth=True)
        await ctx.send(f"Success! {self.bot.user.mention} is now following {user_response.data.username}.")


async def setup(bot):
    await bot.add_cog(Twitter(bot))
