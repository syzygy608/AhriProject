from discord import SlashOption
from nextcord.ext import commands
from nextcord import __version__, Interaction, slash_command, Colour, Embed, SelectOption, ui
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
from dotenv import load_dotenv
import requests
from wsgiref.handlers import format_date_time
from hashlib import sha1
import hmac
import base64

load_dotenv()

class PageButton(ui.Button):
    def __init__(self, id, emojis, embeds):
        super().__init__(emoji = emojis)
        self.id = id
        self.embeds = embeds
    
    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(embed = self.embeds[self.id], view = self.view)

class PageView(ui.View):
    def __init__(self, embeds):
        super().__init__()
        emojis = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣"]
        for i in range(len(embeds)):
            self.add_item(PageButton(i, emojis[i], embeds))

class Auth():
    def __init__(self):
        self.app_id = os.getenv("APP_ID")
        self.app_key = os.getenv("APP_KEY")

    def get_auth_header(self):
        xdate = format_date_time(time.mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), (f'x-date: {xdate}').encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()
        authorization = (f'hmac username="{self.app_id}", algorithm="hmac-sha1"' +
                         f', headers="x-date", signature="{signature}"')
        return {
            'Authorization': authorization,
            'x-date': xdate,
            'Accept-Encoding': 'gzip'
        }

def busID_status(ID, direction):
    driverPATH = './chromedriver' # driver 路徑
    options = webdriver.ChromeOptions() # 使用chromedriver
    options.add_argument('headless')
    options.add_argument("disable-gpu")
    options.add_argument('blink-settings=imagesEnabled=false')
    edge = webdriver.Chrome(driverPATH, options = options)
    edge.get(f"https://www.taiwanbus.tw/eBUSPage/Query/QueryResult.aspx?rno={ID}")
    # 路線編號
    # 7309: rno=73090
    #  106: rno=07460
    # 7306: rno=73060
    if(direction):
        edge.find_element_by_id('pills-back').click()

    time.sleep(1)
    soup = BeautifulSoup(edge.page_source, 'html.parser')
    stop = soup.find_all("div", {"class": "bus-route__stop"})

    stations = []
    for tag in stop:
        name = tag.find('a', {"class": "bus-route__stop-name"})
        status = tag.find('div', {"class": "bus-route__stop-status"})
        stationdir = {"name": name.text, "time": status.text}
        stations.append(stationdir)

    return stations #stations["name"]: 站名,  stations["time"]: 進站時間

#取得指定當日的站別時刻表資料
def train_station(stationID, direction):# stationID= 0: 民雄,  1: 嘉義. direction= 0:順行, 1:逆行
    stationPATH = ["4060", "4080"]
    auth = Auth()
    dtime = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    dt = dtime.strftime("%Y-%m-%d") # 將時間轉換為 string
    url = f'https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/DailyTimetable/Station/{stationPATH[stationID]}/{dt}?&%24format=JSON'
    response = requests.get(url, headers=auth.get_auth_header())

    dt = dtime.strftime("%H:%M") # 將時間轉換為 string
    data = response.json()
    trains = []
    for train in data:
        if train['Direction'] == direction and train['ArrivalTime'] > dt: # 指定方向，未經過得車
            t = {"type": train['TrainTypeName']['Zh_tw'][:2], # 車種
                 "id": train['TrainNo'], # 車號
                 "way": f"{train['StationName']['Zh_tw']}->{train['EndingStationName']['Zh_tw']}", # 方向
                 "time": train["ArrivalTime"] # 抵達時間
                 }
            trains.append(t)
    return trains

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
            }),
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
        stations = busID_status(line, direction)
        direction_list = ["順行", "逆行"]
        compare = {
            "73090": "7309",
            "07460": "106",
            "73060": "7306"
        }
        embeds = []
        for i in range(round(len(stations) / 20)):
            temp = Embed(title = f"{compare[line]} {direction_list[direction]}", description = "`<公車路線狀態>`", color = Colour.dark_gold(), timestamp = datetime.now(tz))
            temp_stations = stations[i * 20 : i * 20 + 20]
            for station in temp_stations:
                temp.add_field(name = station['name'], value = station['time'])
            embeds.append(temp)
        if len(embeds) == 1:
            await interaction.send(embed = embeds[0])
        else:
            await interaction.send(embed = embeds[0], view = PageView(embeds))

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
        embed = Embed(title = f"{station_list[station]}{direction_list[direction]} 火車資訊", description = "`<嘉義、民雄火車資訊>`", color = Colour.dark_gold(), timestamp = datetime.now(tz))
        for train in trains:
            embed.add_field(name = f"{train['type']} {train['id']} {train['way']}", value = train['time'])
        await interaction.send(embed = embed)

def setup(bot: commands.Bot):
    bot.add_cog(Transportation(bot))