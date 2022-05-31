from nextcord.ext import commands
from nextcord import __version__, Interaction, slash_command, Colour, Embed
from datetime import datetime, timezone, timedelta
import requests
from bs4 import BeautifulSoup

index_to_title = {
    0: "日期",
    1: "確診人數",
    4: "備註"
}

tz = timezone(timedelta(hours = +8))

def getInfo():
    response = requests.get("https://www.ccu.edu.tw/2019-nCoV_caseInfo.php")
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    tr = table.find_all("tr", limit = 5)
    return tr

class Cov19(commands.Cog, name = "Covid-19"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description = "get the covid-19 information of CCU", force_global = True)
    async def cov19(self, interaction : Interaction):
        await interaction.response.defer(with_message = True)
        tr = getInfo() # 回傳整個table

        embed = Embed(title = "中正疫情資訊", description = "`<最近三筆確診資訊>`", color = Colour.dark_gold(), timestamp = datetime.now(tz))
        for i in range(2, 5):
            td = tr[i].find_all("td")
            for j in [0, 1, 4]:
                href = td[j].find("a", href = True)
                if href != None:
                    embed.add_field(name = index_to_title[j], value = f"[相關連結](https://www.ccu.edu.tw/{href['href']})", inline = True)
                else:
                    text = (td[j].text).replace("*", "x")
                    if text == "":
                        text = "無"
                    embed.add_field(name = index_to_title[j], value = f" {text} ", inline = True)   
        embed.set_image(url = "https://i.imgur.com/hiYOyUD.png")        
        await interaction.send(embed = embed)
   
def setup(bot: commands.Bot):
    bot.add_cog(Cov19(bot))