from discord import SlashOption
from nextcord.ext import commands
from nextcord import Interaction, slash_command, Colour, Embed, ui, ButtonStyle
from datetime import datetime, timezone, timedelta
import requests
from bs4 import BeautifulSoup
import time
 
tz = timezone(timedelta(hours = +8))

def get_data(): # 取得最新資訊 type: list
    url = "https://www.ccu.edu.tw/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    context = soup.find(id = 'bulletin_feature').find_all(title = "(另開新視窗)", limit = 8)
    news = []
    for s in context:
        t = []
        link = url + s['href'].split('/')[1].split(" ")[0]
        t.append(s.string)
        t.append(link)
        news.append(t)
    return news #news[0]: 標題, news[1]:連結

class News(commands.Cog, name = "News"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description = "return CCU news", force_global = True)
    async def news(self, interaction: Interaction,):
        await interaction.response.defer(with_message = True)
        embed = Embed(title = "中正最新消息", description = f'[最新消息來源](https://www.ccu.edu.tw/bullentin_list.php?id=1)', color = Colour.magenta(), timestamp = datetime.now(tz))
        ccu_news = get_data()
        for news in ccu_news:
            embed.add_field(name = news[0], value = f"[開啟連結]({news[1]})", inline = False)
        await interaction.send(embed = embed)

def setup(bot: commands.Bot):
    bot.add_cog(News(bot))