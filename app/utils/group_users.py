import os

import discord

intents = discord.Intents.default()
intents.members = True  # 必须启用成员意图来获取成员信息

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    guild = discord.utils.get(client.guilds, name="madrid的服务器")  # 替换为你的服务器名称
    if guild:
        members = await guild.fetch_members(limit=None).flatten()  # 获取所有成员
        for member in members:
            print(f'{member.name}##{member.id}')  # 打印成员用户名和标签
    else:
        print("Guild not found!")


client.run(os.getenv('TOKEN'), reconnect=True)
