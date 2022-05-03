from nextcord.ext import commands
from nextcord import __version__, Interaction, slash_command, Colour, Embed, SelectOption, ui
from datetime import datetime, timezone, timedelta
import requests
from bs4 import BeautifulSoup

index_to_title = {
    0: "確診日期",
    1: "確診者身分",
    3: "課程",
    6: "備註"
}
tz = timezone(timedelta(hours = +8))

def getInfo():
    response = requests.get("https://www.ccu.edu.tw/2019-nCoV_caseInfo.php")
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    tr = table.find_all("tr")
    return tr

class Dropdown(ui.Select):
    def __init__(self, length, tr, date):
        self.tr = tr
        options = []
        for i in range(length):
            options.append(SelectOption(label = i + 1, description = date[i]))
        embeds = []
        for i in range(2, len(self.tr)):
            embed = Embed(title = "中正疫情資訊", description = "`<from 中正疫情專區>`", color = Colour.magenta(), timestamp = datetime.now(tz))
            td = self.tr[i].find_all("td")
            for j in [0, 1, 3, 6]:
                href = td[j].find("a", href = True)
                if href != None:
                    embed.add_field(name = index_to_title[j], value = f"[相關連結](https://www.ccu.edu.tw/{href['href']})", inline = False)
                else:
                    embed.add_field(name = index_to_title[j], value = f"`{td[j].text}`", inline = False)   
            embeds.append(embed)
        self.embeds = embeds
        super().__init__(placeholder = 'Choose the date you want to view ...', min_values = 1, max_values = 1, options = options)

    async def callback(self, interaction: Interaction):
        await interaction.send(embed = self.embeds[int(self.values[0]) - 1])

class DropdownView(ui.View):
    def __init__(self, length, tr, date):
        super().__init__()
        self.add_item(Dropdown(length, tr, date))

class Cov19(commands.Cog, name = "Covid-19"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description = "get the covid-19 information of CCU", force_global = True)
    async def cov19(self, interaction : Interaction, ):
        await interaction.response.defer(with_message = True)
        tr = getInfo()
        date = []
        embed = Embed(title = "中正疫情資訊", description = "`<from 中正疫情專區>`", color = Colour.magenta(), timestamp = datetime.now(tz))
        embed.add_field(name = "說明", value = "選擇你想查詢的日期")
        for i in range(2, len(tr)):
            td = tr[i].find_all("td")
            date.append(td[0].text)
        
        await interaction.send(embed = embed, view = DropdownView(len(tr) - 2, tr, date))
   
def setup(bot: commands.Bot):
    bot.add_cog(Cov19(bot))