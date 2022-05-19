from discord import SlashOption
from nextcord.ext import commands
from nextcord import Interaction, slash_command, Colour, Embed, ui, ButtonStyle
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
import time
 
def get_washing_info(place):
    options = webdriver.ChromeOptions() # 使用chromedriver
    options.add_argument('headless') # 隱藏視窗
    options.add_argument("disable-gpu")
    options.add_argument('blink-settings=imagesEnabled=false')
    edge = webdriver.Chrome('./chromedriver', options = options)
    edge.get(f"http://monitor.isesa.com.tw/monitor/?code={place}",)
    time.sleep(1)
    soup = BeautifulSoup(edge.page_source, 'html.parser')
    trs = soup.find("tbody").find_all("tr")
    cnt = [
        {"working": 0, "finish": 0, "space": 0},
        {"working": 0, "finish": 0, "space": 0}
    ]
    for tr in trs:
        tds = tr.find_all("td")
        if "W" in tds[1].text:
            if "運轉中" in tds[2].text:
                cnt[0]["working"] += 1
            elif "運轉結束" in tds[2].text:
                cnt[0]["finish"] += 1
            elif "空機" in tds[2].text:
                cnt[0]["space"] += 1
        else:
            if "運轉中" in tds[2].text:
                cnt[1]["working"] += 1
            elif "運轉結束" in tds[2].text:
                cnt[1]["finish"] += 1
            elif "空機" in tds[2].text:
                cnt[1]["space"] += 1
    return cnt

tz = timezone(timedelta(hours = +8))

class Washing(commands.Cog, name = "Washing"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description = "return washing machine dashboard", force_global = True)
    @commands.cooldown(rate = 5, per = 5, type = commands.BucketType.user)
    async def washing_machine(
        self, 
        interaction: Interaction,
        place: str = SlashOption(
            name = "place",
            description = "洗衣房地點選擇",
            choices = 
            {
                "A棟": "ehuYvg",
                "C棟": "Ecy94C",
                "D+E棟": "yJL1OU"
            },
            required = True
        )
    ):
        await interaction.response.defer(with_message = True)
        embed = Embed(title = "洗衣機狀態列", description = f'[洗衣站URL](http://monitor.isesa.com.tw/monitor/?code={place})', color = Colour.dark_gold(), timestamp = datetime.now(tz))
        data = get_washing_info(place)
        embed.add_field(name = "[洗衣機狀態]", value = f"空機 🟢: {data[0]['space']}\n運轉結束 🟡: {data[0]['finish']}\n運轉中 🔴: {data[0]['working']}")
        embed.add_field(name = "[脫衣機狀態]", value = f"空機 🟢: {data[1]['space']}\n運轉結束 🟡: {data[1]['finish']}\n運轉中 🔴: {data[1]['working']}")
        embed.set_image(url = "https://i.imgur.com/WyDiNMK.png")
        await interaction.send(embed = embed)

def setup(bot: commands.Bot):
    bot.add_cog(Washing(bot))