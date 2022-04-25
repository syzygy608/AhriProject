from nextcord.ext import commands
from nextcord import Interaction, slash_command, Colour, Embed
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours = +8))

class Help(commands.Cog, name = "Help"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description = "return help dashboard", force_global = True)
    async def help(self, interaction: Interaction):
        embed = Embed(title = "機器人指令表", description = "阿梨 bot version a0.0.4", color = Colour.magenta(), timestamp = datetime.now(tz))
        embed.add_field(name = "/bot", value = "查看機器人相關介紹資訊", inline = False)
        embed.add_field(name = "/ping", value = "查看機器人延遲", inline = False)
        embed.add_field(name = "/user_info", value = "查看使用者帳號資訊", inline = False)
        await interaction.send(embed = embed)

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))