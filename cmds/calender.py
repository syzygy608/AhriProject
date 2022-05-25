from nextcord.ext import commands, application_checks
from nextcord import Interaction, slash_command, Colour, Embed, SlashOption
import json
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours = +8))

with open("./calender/data.json", encoding = "utf8") as jfile:
    data = json.load(jfile)

class Calender(commands.Cog, name = "Calender"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description = "get the calender of this month", force_global = True)
    async def calender(self, interaction: Interaction):
        embed = Embed(title = "中正大學本月行事曆", description = f'[行事曆來源](https://www.ccu.edu.tw/calender.php)', color = Colour.dark_gold(), timestamp = datetime.now(tz))
        time_now = datetime.now(tz).strftime('%Y%m')
        embed.add_field(name = time_now, value = data[time_now])
        embed.set_image(url = "https://i.imgur.com/WyDiNMK.png")
        await interaction.send(embed = embed)

def setup(bot: commands.Bot):
    bot.add_cog(Calender(bot))