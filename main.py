import json
import nextcord
from nextcord.ext import commands
import os

intents = nextcord.Intents.default()
intents.members = True

with open("./config.json", 'r') as f:
    data = json.load(f)

bot = commands.Bot(command_prefix = '+', intents = intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

for Filename in os.listdir('./cmds'):
    if Filename.endswith('.py'):
        bot.load_extension(f'cmds.{Filename[:-3]}')

bot.run(data['token'])