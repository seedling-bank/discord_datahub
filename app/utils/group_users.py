import os
import traceback
from datetime import datetime

import discord
import loguru
import pytz
from sqlalchemy import event, insert
from sqlalchemy.exc import DisconnectionError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models.user_models import t_discord_users
from app.utils.send_lark_message import send_a_message

intents = discord.Intents.default()
intents.members = True  # 必须启用成员意图来获取成员信息

client = discord.Client(intents=intents)

def checkout_listener(dbapi_connection, connection_record, connection_proxy):
    try:
        dbapi_connection.ping(reconnect=True)
    except dbapi_connection.OperationalError as exc:
        raise DisconnectionError() from exc

engine = create_async_engine(
    "mysql+aiomysql://cb:cryptoBricks123@34.218.139.166:3306/da_test?charset=utf8mb4",
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
)
event.listen(engine.sync_engine, "checkout", checkout_listener)


async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
    formatted_utc_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')
    timestamp = int(utc_time.timestamp() * 1000)

    guild = discord.utils.get(client.guilds, name="Deagent.AI")  # 替换为你的服务器名称
    if guild:
        members = await guild.fetch_members(limit=None).flatten()  # 获取所有成员
        for member in members:
            print(member.joined_at)
            information = {
                "discord_id": member.id,
                "discord_name": member.name,
                "joined_at": member.joined_at,
                "create_time": timestamp,
                "update_time": timestamp,
                "time_at": formatted_utc_time
            }
            try:
                async with async_session() as session:
                    query = insert(t_discord_users).prefix_with("IGNORE").values(information)
                    await session.execute(query)
                    await session.commit()
            except Exception as e:
                loguru.logger.error(traceback.format_exc())
                send_a_message(traceback.format_exc())

            print(f'{member.name}##{member.id}')  # 打印成员用户名和标签
    else:
        print("Guild not found!")


client.run(os.getenv('TOKEN'), reconnect=True)
