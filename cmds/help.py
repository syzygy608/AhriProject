from nextcord.ext import commands
from nextcord import Interaction, slash_command, Colour, Embed
from datetime import datetime, timezone, timedelta

guilds = []
tz = timezone(timedelta(hours = +8))

class Help(commands.Cog, name = "Help Command"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        for el in self.bot.guilds:
            guilds.append(int(el))

    @slash_command(description = "return help dashboard", guild_ids = guilds)
    async def help(self, interaction: Interaction):
        embed = Embed(title = '機器人指令表', description = '阿梨bot version a0.0.4', color = Colour.brand_green(), timestamp = datetime.now(tz))
        embed.add_field(name = "`/bot`", value = "查看機器人相關介紹資訊", inline = False)
        embed.add_field(name = "`/ping`", value = "查看機器人延遲", inline = False)
        await interaction.send(embed = embed)

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))