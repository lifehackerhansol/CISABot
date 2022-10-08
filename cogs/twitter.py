#
# CISA 2022 Discord server bot
# Copyright (C) 2021-2022 lifehackerhansol
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#

import traceback
from inspect import cleandoc

import discord
import tweepy.asynchronous
from discord.ext import commands

from utils.utils import is_staff


class UpdateStream(tweepy.asynchronous.AsyncStreamingClient):
    def __init__(self, bearer_key, twitterClient, channel_target, debug_target):
        self.channel = channel_target
        self.debugchannel = debug_target
        self.twitter = twitterClient
        super().__init__(bearer_token=bearer_key)

    def filter(self):
        super().filter(tweet_fields=['author_id', 'created_at'])

    async def on_tweet(self, tweet):
        embed = discord.Embed(timestamp=tweet.created_at)
        user = await self.twitter.get_user(id=tweet.author_id, user_fields='profile_image_url', user_auth=True)
        embed.set_author(name=f"{user.data.name} (@{user.data.username})", icon_url=user.data.profile_image_url, url=f"https://twitter.com/{user.data.username}/statuses/{tweet.id}")
        embed.url = f"https://twitter.com/{user.data.username}/statuses/{tweet.id}"
        embed.description = cleandoc(tweet.text)
        await self.channel.send(embed=embed)

    def create_error_embed(self, exc) -> discord.Embed:
        embed = discord.Embed(title="Unexpected exception in UpdateStream", color=0xe50730)
        trace = "".join(traceback.format_exception(type(exc), value=exc, tb=exc.__traceback__))
        embed.description = f'```py\n{trace}```'
        embed.add_field(name="Exception Type", value=exc.__class__.__name__)
        embed.add_field(name="Information", value=f"channel: {self.channel}", inline=False)
        return embed

    async def on_connect(self):
        await self.debugchannel.send("Connection to Twitter successful!")

    async def on_connection_error(self):
        await self.debugchannel.send("Connection to Twitter failed.")

    async def on_disconnect(self):
        await self.debugchannel.send("Disconnected from Twitter.")

    async def on_errors(self, errors):
        await self.debugchannel.send(errors)

    async def on_exception(self, exception):
        print(''.join(traceback.format_exception(type(exception), value=exception, tb=exception.__traceback__)))
        await self.debugchannel.send(embed=self.create_error_embed(exception))


class Twitter(commands.Cog):
    """
    Twitter polling
    """

    def __init__(self, bot):
        self.bot = bot
        if all([
            bot.settings['TWITTER_APIKEY'],
            bot.settings['TWITTER_APISECRET'],
            bot.settings['TWITTER_BEARER'],
            bot.settings['TWITTER_TOKEN'],
            bot.settings['TWITTER_TOKENSECRET'],
            bot.settings['BUSUPDATES'],
            bot.settings['GUILD'],
            bot.settings['STAFFCHANNEL']
        ]):
            self.twitter = tweepy.asynchronous.AsyncClient(
                consumer_key=bot.settings['TWITTER_APIKEY'],
                consumer_secret=bot.settings['TWITTER_APISECRET'],
                access_token=bot.settings['TWITTER_TOKEN'],
                access_token_secret=bot.settings['TWITTER_TOKENSECRET']
            )
            self.updatestream = UpdateStream(
                bot.settings['TWITTER_BEARER'],
                self.twitter,
                bot.get_guild(bot.settings['GUILD']).get_channel(bot.settings['BUSUPDATES']),
                bot.get_guild(bot.settings['GUILD']).get_channel(bot.settings['STAFFCHANNEL'])
            )
            self.updatestream.filter()

    def cog_unload(self):
        self.updatestream.disconnect()

    @is_staff()
    @commands.command()
    async def addrule(self, ctx, *rule: str):
        """
        Adds a rule to the Twitter stream.
        Must use parameters here: https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/build-a-rule
        """
        rule = tweepy.StreamRule(value=rule)
        await self.updatestream.add_rules(rule)
        await ctx.send(f"Rule successfully added.")

    @is_staff()
    @commands.command()
    async def getrules(self, ctx):
        """
        Gets all rules.
        """
        rules = await self.updatestream.get_rules()
        ret = "Curernt rules:\n"
        for i in rules.data:
            ret += f"{i.id}: {i.value}\n"
        await ctx.send(ret)

    @is_staff()
    @commands.command()
    async def idtousr(self, ctx, id: int):
        """
        Converts a Twitter user ID to a username
        """
        user_response = await self.twitter.get_user(id=id, user_auth=True)
        await ctx.send(f"{user_response.data.username}")

    @is_staff()
    @commands.command()
    async def usrtoid(self, ctx, username: str):
        """
        Converts a Twitter username to an ID
        """
        user_response = await self.twitter.get_user(username=username, user_auth=True)
        await ctx.send(f"{user_response.data.id}")

    @is_staff()
    @commands.command()
    async def unfollow(self, ctx, username: str):
        user_response = await self.twitter.get_user(username=username, user_auth=True)
        rules = await self.updatestream.get_rules()
        ret = []
        for i in rules.data:
            if str(user_response.data.id) in i.value:
                ret.append(i.id)
        await self.updatestream.delete_rules(ret)
        await ctx.send(f"Success! {self.bot.user.mention} is no longer receiving tweets from {user_response.data.username}.")


async def setup(bot):
    await bot.add_cog(Twitter(bot))
