import discord
from discord.ext import commands

bot = commands.Bot()

@bot.slash_command(name="gm", description="Test command")
async def test_sign_in(ctx):
    print("Command received")  # 用于在控制台中观察命令接收情况
    await ctx.respond("Testing response")  # 使用 respond 而非 send


bot.run('MTI1OTgzNjkzMDY1MzQyNTcxNQ.GL-7pF.pikPoXKg7O1ZiD8-nZ8NxKOLt1ruP10blNJywk', reconnect=True)
