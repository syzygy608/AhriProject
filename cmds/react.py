from nextcord.ext import commands
from nextcord import __version__, Interaction, slash_command, Colour, Embed
from datetime import datetime, timezone, timedelta
import sys

tz = timezone(timedelta(hours = +8))

class React(commands.Cog, name = "React"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description = "return with latency", force_global = True)
    async def ping(self, interaction: Interaction):
        embed = Embed(title = "機器人延遲狀態", description = "Pong !", color = Colour.brand_green(), timestamp = datetime.now(tz))
        embed.add_field(name = "Bot Latency", value = f"{round(self.bot.latency * 1000)} ms")
        await interaction.send(embed = embed)

    @slash_command(description = "return bot infomation", force_global = True)
    async def bot(self, interaction: Interaction):
        embed = Embed(
            title = "機器人相關資訊", description = "你好，我是阿梨bot，專屬於中正大學師生的資訊統整助手", color = Colour.brand_green(), timestamp = datetime.now(tz)
        )
        embed.add_field(name = "開發語言", value = f"Python 3")
        embed.add_field(name = "使用函式庫", value = f"Nextcord {__version__}")
        embed.add_field(name = "幫助指令", value = "使用`/help`來查看你想要使用的指令", inline = False)
        embed.set_thumbnail(url = self.bot.user.avatar.url)
        await interaction.send(embed = embed)

def setup(bot: commands.Bot):
    bot.add_cog(React(bot))