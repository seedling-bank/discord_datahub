import json
import os
import traceback
from datetime import datetime, timedelta

import aioredis
import discord
import loguru
import pytz
from databases import Database
from discord.ext import commands
from sqlalchemy import insert, select, and_, event
from sqlalchemy.exc import DisconnectionError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.con.config import settings
from app.models.user_models import t_discord_users, t_discord_sign_in, t_users
from app.utils.send_lark_message import send_a_message

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# client = discord.Client(intents=intents)

engine = create_async_engine(
    "mysql+aiomysql://cb:cryptoBricks123@34.218.139.166:3306/da_test?charset=utf8mb4",
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
)

# REDIS_URL = "redis://10.244.4.140:6379"
REDIS_URL = "redis://10.244.4.202:6379"
pool = aioredis.ConnectionPool.from_url(REDIS_URL, max_connections=10)
redis_client = aioredis.Redis(connection_pool=pool)


def checkout_listener(dbapi_connection, connection_record, connection_proxy):
    try:
        dbapi_connection.ping(reconnect=True)
    except dbapi_connection.OperationalError as exc:
        raise DisconnectionError() from exc


# 添加监听事件，在每次从池中获取连接时执行
event.listen(engine.sync_engine, "checkout", checkout_listener)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_member_join(member):
    try:

        utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
        formatted_utc_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')
        timestamp = int(utc_time.timestamp() * 1000)

        information = {
            "discord_id": member.id,
            "discord_name": member.name,
            "joined_at": member.joined_at,
            "time_at": formatted_utc_time,
            "create_time": timestamp,
            "update_time": timestamp
        }
        try:
            async with async_session() as session:
                query = insert(t_discord_users).prefix_with("IGNORE").values(information)
                await session.execute(query)
                await session.commit()
            message = json.dumps(information, default=datetime_handler)
            await redis_client.publish('update_discord_user', message)
        except Exception as e:
            loguru.logger.error(traceback.format_exc())
            send_a_message(traceback.format_exc())
    except Exception as e:
        loguru.logger.error(traceback.format_exc())
        send_a_message(traceback.format_exc())


@bot.event
async def on_ready():
    loguru.logger.info(f'Logged in as {bot.user}!')


@bot.slash_command(name="GM", description="Sign in for today")
async def sign_in(ctx):
    try:
        await ctx.defer(ephemeral=True)

        utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
        timestamp = int(utc_time.timestamp() * 1000)
        formatted_utc_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')

        user_discord_id = ctx.author.id
        username = ctx.author.name
        loguru.logger.info(f"The user with ID {user_discord_id} and username {username} has signed in.")

        try:
            user_query = select(t_users).where(t_users.c.discord_id == user_discord_id)
            async with async_session() as session:
                result = await session.execute(user_query)
                user = result.scalars().first()
        except Exception as e:
            loguru.logger.error(traceback.format_exc())
            send_a_message(traceback.format_exc())

        if user is None:
            await ctx.followup.send("Please come to the DeAgent website to connect Discord.", ephemeral=True)
        else:

            start_of_today_utc = utc_time.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_today_utc = start_of_today_utc + timedelta(days=1, microseconds=-1)
            start_timestamp = int(start_of_today_utc.timestamp() * 1000)
            end_timestamp = int(end_of_today_utc.timestamp() * 1000)

            query = (
                select(t_discord_sign_in)
                .where(
                    and_(
                        t_discord_sign_in.discord_id == user_discord_id,
                        t_discord_sign_in.create_time >= start_timestamp,
                        t_discord_sign_in.create_time <= end_timestamp
                    ))
            )

            try:
                async with async_session() as session:
                    result = await session.execute(query)
                    sign_in_record = result.scalars().first()
            except Exception as e:
                loguru.logger.error(traceback.format_exc())
                send_a_message(traceback.format_exc())

            if sign_in_record is None:
                information = {
                    "discord_id": user_discord_id,
                    "discord_name": username,
                    "create_time": timestamp,
                    "update_time": timestamp,
                    "time_at": formatted_utc_time,
                }
                try:
                    async with async_session() as session:
                        query = insert(t_discord_sign_in).values(information)
                        await session.execute(query)
                        await session.commit()

                    message = json.dumps(information, default=datetime_handler)
                    await redis_client.publish('update_discord_sign_in', message)
                except Exception as e:
                    loguru.logger.error(traceback.format_exc())
                    send_a_message(traceback.format_exc())
                await ctx.followup.send("Sign in successfully!", ephemeral=True)
            else:
                await ctx.followup.send("You have already signed in today.", ephemeral=True)
    except Exception as e:
        loguru.logger.error(traceback.format_exc())
        send_a_message(traceback.format_exc())


def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


# @client.event
# async def on_message(message):
#     global result
#
#     utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
#     start_of_today_utc = utc_time.replace(hour=0, minute=0, second=0, microsecond=0)
#     end_of_today_utc = start_of_today_utc + timedelta(days=1, microseconds=-1)
#
#     start_timestamp = int(start_of_today_utc.timestamp() * 1000)
#     end_timestamp = int(end_of_today_utc.timestamp() * 1000)
#     formatted_utc_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')
#     timestamp = int(utc_time.timestamp() * 1000)
#
#     if message.content.lower() == settings.Sign_In_Word:
#
#         user_discord_id = message.author.id
#         username = message.author.name
#         loguru.logger.info(f"The user with ID {user_discord_id} and username {username} has signed in.")
#
#         user_query = select(t_users).where(t_users.c.discord_id == user_discord_id)
#
#         async with async_session() as session:
#             try:
#                 result = await session.execute(user_query)
#                 result = result.fetchall()
#             except Exception as e:
#                 loguru.logger.error(e)
#                 loguru.logger.error(traceback.format_exc())
#
#         user_data = [{
#             'id': obj.id,
#             'username': obj.username,
#             'avatar': obj.avatar,
#             'create_time': obj.create_time,
#             'discord_id': obj.discord_id,
#             'twitter_id': obj.twitter_id,
#             'twitter_token': obj.twitter_token,
#             'discord_name': obj.discord_name,
#             'country': obj.country,
#             'email': obj.email,
#             'verified': obj.verified,
#             'tg_id': obj.tg_id,
#             'tg_username': obj.tg_username,
#             'address': obj.address,
#             'platform': obj.platform
#         } for obj in result]
#
#         if len(user_data) == 0:
#             await message.author.send("请到da官网来保存discord")
#             # await message.reply("请到da官网来保存discord")
#         else:
#             query = (
#                 select(t_discord_sign_in)
#                 .where(
#                     and_(
#                         t_discord_sign_in.discord_id == user_discord_id,
#                         t_discord_sign_in.create_time >= str(start_timestamp),
#                         t_discord_sign_in.create_time <= str(end_timestamp)
#                     ))
#             )
#
#             async with async_session() as session:
#                 try:
#                     result = await session.execute(query)
#                     results = result.scalars()
#                 except Exception as e:
#                     loguru.logger.error(e)
#                     loguru.logger.error(traceback.format_exc())
#
#             data = [{
#                 'id': obj.id,
#                 'discord_id': obj.discord_id,
#                 'discord_name': obj.discord_name,
#                 'create_time': obj.create_time,
#                 'update_time': obj.update_time,
#                 'time_at': obj.time_at
#             } for obj in results]
#
#             if len(data) == 0:
#                 information = {
#                     "discord_id": user_discord_id,
#                     "discord_name": username,
#                     "create_time": timestamp,
#                     "update_time": timestamp,
#                     "time_at": formatted_utc_time,
#                 }
#                 async with async_session() as session:
#                     try:
#                         query = insert(t_discord_sign_in).values(information)
#                         await session.execute(query)
#                         await session.commit()
#                     except Exception as e:
#                         loguru.logger.info(e)
#                         loguru.logger.error(traceback.format_exc())
#
#                 await message.author.send("签到成功")

bot.run(os.getenv('TOKEN'), reconnect=True)
