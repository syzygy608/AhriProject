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

def train_station(stationID, direction): # stationID= 0: 民雄,  1: 嘉義. dirction= 0:順行, 1:逆行
    stationPATH = ["4060-%E6%B0%91%E9%9B%84", "4080-%E5%98%89%E7%BE%A9"]

    # 現在時間
    dt = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    dt = dt.strftime("%H:%M") # 將時間轉換為 string

    driverPATH = './chromedriver' # driver 路徑
    options = webdriver.ChromeOptions() # 使用chromedriver

    options.add_argument('headless')
    options.add_argument("disable-gpu")

    edge = webdriver.Chrome(driverPATH, options = options)
    edge.get(f"https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybystationblank?rideDate=2022/05/08&station={stationPATH[stationID]}")
    time.sleep(1)
    soup = BeautifulSoup(edge.page_source, 'html.parser')
    context = soup.find_all("tbody")

    trains = []
    trs = context[direction].find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds):
            name = tds[1].find('a')
            way = []
            name = name.text
            for c in tds[1].find_all('span'):
                way.append(c.text)
            way = ''.join(way)
            arriveTime = tds[2].text
            if arriveTime > dt: # 儲存還未經過的車
                train = {"name": name,
                         "way": way,
                         "time": arriveTime
                         }
                trains.append(train)

    return trains  #trians["name"]: name, trians["way"]: 出發->抵達, trians["time"]: 到站時間

tz = timezone(timedelta(hours = +8))
class Transportation(commands.Cog, name = "transportation"):
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

    @slash_command(description = "get the train information", force_global = True)
    @commands.cooldown(rate = 5, per = 5, type = commands.BucketType.user)
    async def train_info(
        self,
        interaction: Interaction,
        station: int = SlashOption
        (
            name = "station",
            description = "choose the station you want to check",
            choices = 
            {
                "嘉義": 1,
                "民雄": 0
            }
        ),
        direction: int = SlashOption
        (
            name = "direction",
            description = "choose the direction you want to check",
            choices = 
            {
                "順行": 0,
                "逆行": 1
            }
        ),
    ):
        await interaction.response.defer(with_message = True)
        trains = train_station(station, direction)
        station_list = ["民雄", "嘉義"]
        direction_list = ["順行", "逆行"]
        embed = Embed(title = f"{station_list[station]}{direction_list[direction]} 火車資訊", description = "`<嘉義、民雄火車資訊>`", color = Colour.magenta(), timestamp = datetime.now(tz))
        for train in trains:
            embed.add_field(name = f"{train['name']} {train['way']}", value = train['time'])
        await interaction.send(embed = embed)

def setup(bot: commands.Bot):
    bot.add_cog(Transportation(bot))