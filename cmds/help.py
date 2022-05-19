from nextcord.ext import commands
from nextcord import Interaction, slash_command, Colour, Embed, ui, ButtonStyle
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours = +8))

class PageButton(ui.Button):
    def __init__(self, label, id, embeds):
        super().__init__(label = label)
        self.id = id
        self.embeds = embeds
    
    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(embed = self.embeds[self.id], view = self.view)

class HelpPageView(ui.View):
    def __init__(self, embeds):
        super().__init__()
        self.add_item(PageButton("一般指令", 0, embeds))
        self.add_item(PageButton("資訊指令", 1, embeds))

class Help(commands.Cog, name = "Help"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description = "return help dashboard", force_global = True)
    async def help(self, interaction: Interaction):
        
        normalEmbed = Embed(title = "機器人指令表", description = "`<一般指令>`", color = Colour.dark_gold(), timestamp = datetime.now(tz))
        normalEmbed.add_field(name = "/bot", value = "查看機器人相關介紹資訊", inline = False)
        normalEmbed.add_field(name = "/ping", value = "查看機器人延遲", inline = False)
        normalEmbed.add_field(name = "/ping", value = "顯示機器人延遲數據", inline = False)
        normalEmbed.add_field(name = "/user_info", value = "查看使用者帳號資訊", inline = False)
        normalEmbed.add_field(name = "/reload", value = "*重新載入模塊", inline = False)
        normalEmbed.add_field(name = "/purge", value = "*清除訊息", inline = False)
        normalEmbed.set_footer(text = "*為管理員專用指令")

        toolEmbed = Embed(title = "機器人指令表", description = "`<資訊指令>`", color = Colour.dark_gold(), timestamp = datetime.now(tz))
        
        toolEmbed.add_field(name = "/links", value = "查看常用連結", inline = False)
        toolEmbed.add_field(name = "/weather", value = "查看縣市之三天內天氣預報", inline = False)
        toolEmbed.add_field(name = "/cov19", value = "查看中正最新疫情資訊", inline = False)
        toolEmbed.add_field(name = "/news", value = "查看中正最新消息/公告", inline = False)
        toolEmbed.add_field(name = "/bus_info", value = "查看中正周邊公車資訊", inline = False)
        toolEmbed.add_field(name = "/train_info", value = "查看中正周邊火車資訊", inline = False)

        embeds = [normalEmbed, toolEmbed]

        await interaction.send(embed = embeds[0], view = HelpPageView(embeds))

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))