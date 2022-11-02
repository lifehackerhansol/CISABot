#
# CISA 2022 Discord server bot
# Copyright (C) 2021-2022 lifehackerhansol
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#

import sqlite3
from datetime import datetime

import aiosqlite
from discord.utils import time_snowflake


class SQLDB():
    def __init__(self, bot):
        self.bot = bot

    dbpath = "cisabot.db"

    def generate_id(self) -> int:
        return time_snowflake(datetime.now())

    async def get_guild(self, guild_id: int):
        async with aiosqlite.connect(self.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            return await conn.execute_fetchall(f"SELECT * FROM guilds WHERE id={guild_id};")

    async def add_guild(self, guild_id: int):
        async with aiosqlite.connect(self.dbpath) as conn:
            await conn.execute_insert(f"INSERT INTO guilds (id) VALUES ({guild_id});")
            await conn.commit()

    async def get_reminders(self, user_id: int):
        async with aiosqlite.connect(self.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            return await conn.execute_fetchall(f"SELECT * FROM reminders WHERE user_id={user_id} AND guild_id={guild_id};")

    async def add_reminder(self, user_id: int, channel_id: int, expiry: datetime, content: str):
        async with aiosqlite.connect(self.dbpath) as conn:
            await conn.execute_insert(
                f"INSERT INTO reminders (id, user_id, channel_id, time_expired, content) VALUES ({self.generate_id()}, {user_id}, {channel_id}, {time_snowflake(expiry)}, '{content}');"
            )
            await conn.commit()

    async def remove_reminder(self, user_id: int, index: int):
        async with aiosqlite.connect(self.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            reminders = await conn.execute_fetchall(f"SELECT * FROM reminders WHERE user_id={user_id};")
            reminderid = reminders[index - 1]["id"]
            await conn.execute(f"DELETE FROM reminders WHERE id={reminderid};")
            await conn.commit()

    async def add_modrole(self, guild_id: int, role_id: int):
        guild = await self.get_guild(guild_id)
        if not guild:
            await self.add_guild(guild_id)
        async with aiosqlite.connect(self.dbpath) as conn:
            await conn.execute_insert(f"INSERT INTO modroles (id, guild_id) VALUES ({role_id}, {guild_id});")
            await conn.commit()

