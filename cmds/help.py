from nextcord.ext import commands
from nextcord import Interaction, slash_command, Colour, Embed, ui, ButtonStyle
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours = +8))

class Page(ui.View):
    def __init__(self, normal_embed, admin_embed):
        super().__init__(timeout = None)
        self.normal = normal_embed
        self.admin = normal_embed

    @ui.button(label = '一般指令', style = ButtonStyle.gray)
    async def delete(self, button: ui.Button, interaction: Interaction):
        await interaction.edit(embed = self.normal, view = self)

    @ui.button(label = '管理員指令', style = ButtonStyle.green)
    async def change_position(self, button: ui.Button, interaction: Interaction):
        await interaction.edit(embed = self.admin, view = self)

class Help(commands.Cog, name = "Help"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description = "return help dashboard", force_global = True)
    async def help(self, interaction: Interaction):
        normal_embed = Embed(title = "機器人指令表", description = "`<一般指令>`", color = Colour.magenta(), timestamp = datetime.now(tz))
        normal_embed.add_field(name = "/bot", value = "查看機器人相關介紹資訊", inline = False)
        normal_embed.add_field(name = "/ping", value = "查看機器人延遲", inline = False)
        normal_embed.add_field(name = "/user_info", value = "查看使用者帳號資訊", inline = False)
        normal_embed.add_field(name = "/links", value = "查看常用連結", inline = False)

        admin_embed = Embed(title = "機器人指令表", description = "`<管理員指令>`", color = Colour.magenta(), timestamp = datetime.now(tz))
        admin_embed.add_field(name = "/purge", value = "清除頻道訊息", inline = False)
        # view = Page(normal_embed, admin_embed)
        await interaction.send(embed = normal_embed)

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))