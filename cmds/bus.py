from discord import SlashOption
from nextcord.ext import commands
from nextcord import __version__, Interaction, slash_command, Colour, Embed, SelectOption, ui
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def busID_status(busID):
    driverPATH = './chromedriver' # driver 路徑
    options = webdriver.ChromeOptions() # 使用chromedriver
    options.add_argument('headless')
    options.add_argument("disable-gpu")
    edge = webdriver.Chrome(driverPATH, options = options)
    edge.get(f"https://www.taiwanbus.tw/eBUSPage/Query/QueryResult.aspx?rno={busID}")
    time.sleep(1)
    soup = BeautifulSoup(edge.page_source, 'html.parser')
    stop = soup.find_all("div", {"class": "bus-route__stop"})

    stations = []
    for tag in stop:
        name = tag.find('a', {"class": "bus-route__stop-name"})
        status = tag.find('div', {"class": "bus-route__stop-status"})
        stationdir = {"name": name.text, "time": status.text}
        stations.append(stationdir)
    return stations

tz = timezone(timedelta(hours = +8))
class Bus(commands.Cog, name = "Bus"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description = "get the bus information", force_global = True)
    @commands.cooldown(rate = 5, per = 5, type = commands.BucketType.user)
    async def bus_info(
        self,
        interaction : Interaction,
        line: str = SlashOption(
            name = "bus_line", 
            description = "choose the train line you want to look up.",
            choices = {
                "7309": "73090",
                "106": "07460",
                "7306": "73060"
            })
    ):
        await interaction.response.defer(with_message = True)
        stations = busID_status(line)
        compare = {
            "73090": "7309",
            "07460": "106",
            "73060": "7306"
        }
        embed = Embed(title = f"公車 {compare[line]} 資訊", description = "`<嘉義、民雄公車資訊>`", color = Colour.magenta(), timestamp = datetime.now(tz))
        for station in stations:
            embed.add_field(name = station['name'], value = station['time'])
        await interaction.send(embed = embed)
   
def setup(bot: commands.Bot):
    bot.add_cog(Bus(bot))