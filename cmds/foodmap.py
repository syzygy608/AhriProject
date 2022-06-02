from nextcord.ext import commands
from nextcord import Interaction, slash_command, Colour, Embed, utils
from datetime import datetime, timezone, timedelta
import requests
import random

tz = timezone(timedelta(hours = +8))

def get_resturants():
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    node(around:1200.00,23.557038,120.471707)["amenity"="restaurant"];

    out body;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    restaurants = []
    for r in data['elements']:
        info = {'name':r['tags']['name'], # node name
                'link': "https://www.openstreetmap.org/node/" + str(r['id']) #node link
               }
        restaurants.append(info)
    return restaurants # restaurants['name']:餐廳名稱, restaurants['link']: 位置連結

class Foodmap(commands.Cog, name = "food map"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description = "return a list of restaurants around CCU", force_global = True)
    async def restaurant_list(self, interaction: Interaction):
        restaurants = get_resturants()
        text = ""
        arr = set()
        for restaurant in restaurants:
            arr.add(restaurant['name'])
        arr = sorted(list(arr), key = lambda k: (len(k), k))
        for el in arr:
            text += el + "\n"    
        embed = Embed(title = "中正周邊餐廳列表", description = text, color = Colour.dark_gold(), timestamp = datetime.now(tz))
        await interaction.send(embed = embed)

    @slash_command(description = "choose a restaurant around CCU", force_global = True)
    async def restaurant_pick(self, interaction: Interaction,):
        restaurants = get_resturants()
        pickup = random.choice(restaurants)
        emoji = "<a:arrow:981828049635004426>"
        text = f"☰☰☰☰☰☰☰☰☰☰☰☰◈☰☰☰☰☰☰☰☰☰☰☰☰\n\n{emoji} **{pickup['name']}**\n\n[位置資訊]({pickup['link']})\n\n☰☰☰☰☰☰☰☰☰☰☰☰◈☰☰☰☰☰☰☰☰☰☰☰☰"
        embed = Embed(title = "🍽 中正餐廳隨機推薦", description = text, color = Colour.dark_gold(), timestamp = datetime.now(tz))
        embed.set_image(url = "https://i.imgur.com/sGx2Z9M.png")
        await interaction.send(embed = embed)

def setup(bot: commands.Bot):
    bot.add_cog(Foodmap(bot))
