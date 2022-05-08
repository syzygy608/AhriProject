from nextcord.ext import commands
from nextcord import Interaction, slash_command, Colour, Embed, ui, ButtonStyle
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours = +8))

class Help(commands.Cog, name = "Help"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description = "return help dashboard", force_global = True)
    async def help(self, interaction: Interaction):
        embed = Embed(title = "機器人指令表", description = "`<一般指令>`", color = Colour.magenta(), timestamp = datetime.now(tz))
        embed.add_field(name = "/bot", value = "查看機器人相關介紹資訊", inline = False)
        embed.add_field(name = "/ping", value = "查看機器人延遲", inline = False)
        embed.add_field(name = "/user_info", value = "查看使用者帳號資訊", inline = False)
        embed.add_field(name = "/links", value = "查看常用連結", inline = False)
        embed.add_field(name = "/weather", value = "查看縣市之三天內天氣預報", inline = False)
        embed.add_field(name = "/cov19", value = "查看中正最新疫情資訊", inline = False)
        embed.add_field(name = "/news", value = "查看中正最新消息/公告", inline = False)
        embed.add_field(name = "/bus_info", value = "查看中正周邊公車資訊", inline = False)
        embed.add_field(name = "/train_info", value = "查看中正周邊火車資訊", inline = False)
        await interaction.send(embed = embed)

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))