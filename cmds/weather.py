import json
from nextcord.ext import commands
from nextcord import __version__, Interaction, slash_command, Colour, Embed, SlashOption
from datetime import datetime, timezone, timedelta
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
weather_token = os.getenv("WEATHER_TOKEN") 
baseurl = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/"

tz = timezone(timedelta(hours = +8))

class Weather(commands.Cog, name = "Weather"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description = "get the weather of specified city", force_global = True)
    async def weather(
        self, 
        interaction : Interaction, 
        city: str = SlashOption(
            name = "city", 
            description = "What city's weather you want to know?", 
            choices = {
                "宜蘭縣": "F-D0047-001",
                "桃園市": "F-D0047-005",
                "新竹縣": "F-D0047-009",
                "苗栗縣": "F-D0047-013",
                "彰化縣": "F-D0047-017",
                "南投縣": "F-D0047-021",
                "雲林縣": "F-D0047-025",
                "嘉義縣": "F-D0047-029",
                "屏東縣": "F-D0047-033",
                "臺東縣": "F-D0047-037",
                "花蓮縣": "F-D0047-041",
                "澎湖縣": "F-D0047-045",
                "基隆市": "F-D0047-049",
                "新竹市": "F-D0047-053",
                "嘉義市": "F-D0047-057",
                "台北市": "F-D0047-061",
                "高雄市": "F-D0047-065",
                "新北市": "F-D0047-069",
                "台中市": "F-D0047-073",
                "台南市": "F-D0047-077",
                "連江縣": "F-D0047-081",
                "金門縣": "F-D0047-085"
                },
            required = True
        )
    ):
        await interaction.response.defer(with_message = True)
        response = requests.get(f"{baseurl}{city}?Authorization={weather_token}&limit=1")
        rawdata = response.json()
        data = rawdata["records"]["locations"][0]
        title = data['locationsName']

        embed = Embed(title = F"{title} 氣象預報", description = "`<三天內氣象預報>`", timestamp = datetime.now(tz))
        element = data["location"][0]['weatherElement']
        for el in element:
            if el['description'] == "天氣預報綜合描述":
                for detail in el['time']:
                    result = detail['elementValue'][0]['value'].split("。")
                    temperature = result[2].split("氏")[1]
                    rain_possibility = result[1]
                    describe = result[0]
                    if int(rain_possibility.split()[1].replace("%", "")) >= 50:
                        describe += "🌧"
                    embed.add_field(name = detail['startTime'], value = f"{temperature}\n{rain_possibility}\n{describe}")
        await interaction.send(embed = embed)
   
def setup(bot: commands.Bot):
    bot.add_cog(Weather(bot))