import json
import nextcord
from nextcord.ext import commands
import os

intents = nextcord.Intents.default()
intents.members = True

with open("./config.json", 'r') as f:
    data = json.load(f)

bot = commands.Bot(command_prefix = '+', intents = intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(status = nextcord.Status.idle, activity = nextcord.Activity(name = "挖鳳梨比賽中...", type = nextcord.ActivityType.competing))
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

for Filename in os.listdir('./cmds'):
    if Filename.endswith('.py'):
        bot.load_extension(f'cmds.{Filename[:-3]}')

bot.run(data['token'])