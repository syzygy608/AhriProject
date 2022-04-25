import json
import nextcord
from nextcord.ext import commands, tasks
from itertools import cycle
import os

intents = nextcord.Intents.default()
intents.members = True

with open("./config.json", 'r') as f:
    data = json.load(f)

status = cycle(
    ["使用/help來查看指令表", "中正資訊整理助手", "挖鳳梨大賽進行中..."])

bot = commands.Bot(command_prefix = '+', intents = intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    status_loop.start()
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@tasks.loop(seconds = 5)
async def status_loop():
    await bot.change_presence(status = nextcord.Status.idle, activity = nextcord.Activity(name = next(status), type = nextcord.ActivityType.listening))

for Filename in os.listdir('./cmds'):
    if Filename.endswith('.py'):
        bot.load_extension(f'cmds.{Filename[:-3]}')

bot.run(data['token'])