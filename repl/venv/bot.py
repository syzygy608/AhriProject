import nextcord
from nextcord.ext import commands, tasks
from itertools import cycle
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("BOT_TOKEN") # 取得.env檔案中的 bot token

intents = nextcord.Intents.default() 
intents.members = True # 開啟bot 讀取 member 權限

status = cycle(["使用/help來查看指令表", "中正資訊整理助手", "挖鳳梨大賽進行中..."]) # 狀態循環

bot = commands.Bot(command_prefix = '/', intents = intents)
bot.remove_command("help") # 移除內建 help 指令

@bot.event
async def on_ready():
    status_loop.start()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(f"指令的冷卻時間還有 {round(error.retry_after, 2)} 秒")

@tasks.loop(seconds = 5) # 建立五秒更新一次機器人狀態的循環
async def status_loop():
    await bot.change_presence(status = nextcord.Status.idle, activity = nextcord.Activity(name = next(status), type = nextcord.ActivityType.listening))

for Filename in os.listdir("./cmds"): # Loading bot cogs
    if Filename.endswith(".py"):
        bot.load_extension(f"cmds.{Filename[:-3]}")

bot.run(token)