import json
import os
import traceback
from datetime import datetime, timedelta, timezone

import aioredis
import discord
import loguru
import pytz
from databases import Database
from discord.ext import commands
from sqlalchemy import insert, select, and_, event, update
from sqlalchemy.exc import DisconnectionError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.con.config import settings
from app.models.user_models import t_discord_users, t_discord_sign_in, t_users, t_lumoz_discord_users_info, \
    t_lumoz_discord_users, t_B2_user, B2_discord_info
from app.utils.send_lark_message import send_a_message

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# client = discord.Client(intents=intents)

engine = create_async_engine(
    "mysql+aiomysql://cb:cryptoBricks123@cb-rds.cw5tnk9dgstt.us-west-2.rds.amazonaws.com/da_test?charset=utf8mb4",
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
)


# REDIS_URL = "redis://10.244.4.140:6379"
# REDIS_URL = "redis://10.244.4.58:6379"
# pool = aioredis.ConnectionPool.from_url(REDIS_URL, max_connections=100000)
# redis_client = aioredis.Redis(connection_pool=pool)


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
        # DA discord
        if member.guild.id == 1194935697665167392:
            utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
            formatted_utc_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')
            timestamp = int(utc_time.timestamp() * 1000)

            loguru.logger.info(f"user id is {member.id} and user name is {member.name} join da {formatted_utc_time}")

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
                    user_data = {
                        "discord_code": 1
                    }
                    query1 = (
                        update(t_users)
                        .where(t_users.c.discord_id == str(member.id))
                        .values(**user_data)
                    )
                    await session.execute(query1)
                    await session.commit()
                    query = insert(t_discord_users).prefix_with("IGNORE").values(information)
                    await session.execute(query)
                    await session.commit()

                    # query = select(t_users.c.id).where(t_users.c.discord_id == member.id)
                    # try:
                    #     async with async_session() as session:
                    #         result = await session.execute(query)
                    #         user = result.scalars().first()
                    #
                    #     if user:
                    #         message = json.dumps(information, default=datetime_handler)
                    #         await redis_client.publish(f'update_discord_user_{user}', message)
                    # except Exception as e:
                    #     loguru.logger.error(traceback.format_exc())
                    #     send_a_message(traceback.format_exc())
            except Exception as e:
                loguru.logger.error(traceback.format_exc())
                send_a_message(traceback.format_exc())

        # LUMOZ discord
        if member.guild.id == 1007087464550256791:

            utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
            formatted_utc_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')
            timestamp = int(utc_time.timestamp() * 1000)

            loguru.logger.info(f"user id is {member.id} and user name is {member.name} join LUMOZ {formatted_utc_time}")

            information = {
                "discord_id": member.id,
                "discord_name": member.name,
                "joined_at": member.joined_at,
                "time_at": formatted_utc_time,
                "create_time": timestamp,
                "update_time": timestamp
            }
            #
            try:
                async with async_session() as session:

                    user_data = {
                        "discord_code": 1
                    }
                    query1 = (
                        update(t_lumoz_discord_users)
                        .where(t_lumoz_discord_users.c.discord_id == int(member.id))
                        .values(**user_data)
                    )
                    await session.execute(query1)
                    await session.commit()

                    query = insert(t_lumoz_discord_users_info).prefix_with("IGNORE").values(information)
                    await session.execute(query)
                    await session.commit()

                    # query = select(t_users.c.id).where(t_users.c.discord_id == member.id)
                    # try:
                    #     async with async_session() as session:
                    #         result = await session.execute(query)
                    #         user = result.scalars().first()
                    #
                    #     if user:
                    #         message = json.dumps(information, default=datetime_handler)
                    #         await redis_client.publish(f'update_discord_user_{user}', message)
                    # except Exception as e:
                    #     loguru.logger.error(traceback.format_exc())
                    #     send_a_message(traceback.format_exc())
            except Exception as e:
                loguru.logger.error(traceback.format_exc())
                send_a_message(traceback.format_exc())

        # B2 discord
        if member.guild.id == 1166991951149682698:

            utc_time = datetime.now(timezone.utc)
            formatted_utc_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')
            timestamp = int(utc_time.timestamp() * 1000)

            loguru.logger.info(f"user id is {member.id} and user name is {member.name} join B2 {formatted_utc_time}")

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

                    user_data = {
                        "task_discord_code": 1
                    }
                    query1 = (
                        update(t_B2_user)
                        .where(t_B2_user.c.discord_id == int(member.id))
                        .values(**user_data)
                    )
                    await session.execute(query1)
                    await session.commit()

                    query = insert(B2_discord_info).prefix_with("IGNORE").values(information)
                    await session.execute(query)
                    await session.commit()

            except Exception as e:
                loguru.logger.error(traceback.format_exc())
                send_a_message(traceback.format_exc())

    except Exception as e:
        loguru.logger.error(traceback.format_exc())
        send_a_message(traceback.format_exc())


@bot.event
async def on_ready():
    loguru.logger.info(f'Logged in as {bot.user}!')


@bot.slash_command(name="gm", description="Sign in for today")
async def sign_in(ctx):
    try:

        await ctx.defer()

        utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
        timestamp = int(utc_time.timestamp() * 1000)
        formatted_utc_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')

        user_discord_id = ctx.author.id
        username = ctx.author.name
        loguru.logger.info(f"The user with ID {user_discord_id} and username {username} has signed in.")

        try:
            user_query = select(t_users.c.id).where(t_users.c.discord_id == user_discord_id)
            async with async_session() as session:
                result = await session.execute(user_query)
                user = result.scalars().first()
        except Exception as e:
            loguru.logger.error(traceback.format_exc())
            send_a_message(traceback.format_exc())

        if user is None:
            embed = discord.Embed(
                title=":dizzy: Wallet Not Linked! :dizzy: ",
                description="Your Discord account is not linked to a wallet. Please visit https://deagent.ai/reward to link your wallet and then check in.",
                color=discord.Color.blue()
            )
            file = discord.File("20240813-144605.png", filename="image.png")
            embed.set_image(url="attachment://image.png")

            await ctx.respond(file=file, embed=embed)
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

                    # query = select(t_users.c.id).where(t_users.c.discord_id == user_discord_id)
                    # try:
                    #     async with async_session() as session:
                    #         result = await session.execute(query)
                    #         user = result.scalars().first()
                    #
                    #     if user:
                    #         message = json.dumps(information, default=datetime_handler)
                    #         await redis_client.publish(f'update_discord_sign_in_{user}', message)
                    # except Exception as e:
                    #     loguru.logger.error(traceback.format_exc())
                    #     send_a_message(traceback.format_exc())
                except Exception as e:
                    loguru.logger.error(traceback.format_exc())
                    send_a_message(traceback.format_exc())

                embed = discord.Embed(
                    title=":dizzy: Check-in completed! :dizzy: ",
                    description="Please visit https://deagent.ai/reward to view using the wallet linked to your Discord.",
                    color=discord.Color.blue()
                )
                file = discord.File("20240813-144605.png", filename="image.png")
                embed.set_image(url="attachment://image.png")

                await ctx.respond(file=file, embed=embed)
            else:
                embed = discord.Embed(
                    title=":dizzy: You’ve already checked in.  :dizzy: ",
                    description="Our daily check-in resets at 12:00 UTC. Please try again after the reset.",
                    color=discord.Color.blue()
                )
                file = discord.File("20240813-144605.png", filename="image.png")
                embed.set_image(url="attachment://image.png")

                await ctx.respond(file=file, embed=embed)

    except Exception as e:
        loguru.logger.error(traceback.format_exc())
        send_a_message(traceback.format_exc())


def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")



bot.run(os.getenv('TOKEN'), reconnect=True)
