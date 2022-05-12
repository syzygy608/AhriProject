from discord import SlashOption
from nextcord.ext import commands
from nextcord import Interaction, slash_command, Colour, Embed, ui, ButtonStyle
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
import time
 
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
        embed = Embed(title = "洗衣機狀態列", description = f'[洗衣站URL](http://monitor.isesa.com.tw/monitor/?code={place})', color = Colour.magenta(), timestamp = datetime.now(tz))
        options = webdriver.ChromeOptions() # 使用chromedriver
        options.add_argument('headless') # 隱藏視窗
        options.add_argument("disable-gpu")
        options.add_argument('blink-settings=imagesEnabled=false')
        edge = webdriver.Chrome('./chromedriver', options = options)
        edge.get(f"http://monitor.isesa.com.tw/monitor/?code={place}",)
        time.sleep(1)
        soup = BeautifulSoup(edge.page_source, 'html.parser')
        success = soup.find_all("span", "label label-success glyphicon glyphicon-ok")
        using = soup.find_all("span", "label label-primary")
        count = [0, 0, 0]
        for span in success:
            if span.text == "空機":
                count[0] += 1
            else:
                count[1] += 1
        count[2] = len(using)
        embed.add_field(name = "空機 🟢", value = count[0], inline = False)
        embed.add_field(name = "運轉結束 🟡", value = count[1], inline = False)
        embed.add_field(name = "運轉中 🔴", value = count[2], inline = False)
        await interaction.send(embed = embed)

def setup(bot: commands.Bot):
    bot.add_cog(Washing(bot))