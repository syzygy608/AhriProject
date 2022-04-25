from nextcord.ext import commands
from nextcord import __version__, Interaction, slash_command, Colour, Embed
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours = +8))

class React(commands.Cog, name = "React"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description = "return with latency", force_global = True)
    async def ping(self, interaction: Interaction):
        embed = Embed(title = "機器人延遲狀態", description = "Pong !", color = Colour.magenta(), timestamp = datetime.now(tz))
        embed.add_field(name = "Bot Latency", value = f"{round(self.bot.latency * 1000)} ms")
        await interaction.send(embed = embed)

    @slash_command(description = "return bot infomation", force_global = True)
    async def bot(self, interaction: Interaction):
        embed = Embed(
            title = "機器人相關資訊", 
            description = 
                "你好，我是阿梨bot，\n" + 
                "專屬於中正大學師生的資訊統整助手\n\n" +
                "꙳✧˖°⌖꙳✧˖°⌖꙳✧˖°⌖꙳✧˖°⌖꙳✧˖°⌖꙳✧˖°⌖꙳✧˖°⌖꙳✧˖°\n"
                , 
            color = Colour.magenta(), 
            timestamp = datetime.now(tz)
        )
        embed.add_field(name = "開發語言", value = f"Python 3")
        embed.add_field(name = "使用函式庫", value = f"Nextcord {__version__}")
        embed.add_field(
            name = "功能",
            value = 
            "1. 洗衣部洗衣機狀態列\n" +
            "2. 中正火車公車交通資訊\n" +
            "3. 校網最新消息\n" +
            "4. 校內疫情資訊（確診資訊）\n" +
            "5. 行事曆\n" + 
            "6. 常用連結\n" + 
            "7. 美食地圖",
            inline = False
        )
        embed.add_field(name = "幫助指令", value = "使用`/help`來查看你想要使用的指令", inline = False)
        embed.set_thumbnail(url = self.bot.user.avatar.url)
        embed.set_image(url = "https://cdngarenanow-a.akamaihd.net/webmain/static/pss/lol/items_splash/ahri_27.jpg")
        embed.set_footer(text = "你的中正資訊小助手")
        await interaction.send(embed = embed)

    @slash_command(description = "show up user's information", force_global = True)
    async def user_info(self, interaction: Interaction):
        embed = Embed(
            title = "使用者資訊", description = f"關於{interaction.user}", color = interaction.user.color, timestamp = datetime.now(tz)
        )
        embed.add_field(name = "Account ID", value = interaction.user.id, inline = False)
        embed.add_field(name = "Created At", value = interaction.user.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'), inline = False)
        embed.set_thumbnail(url = interaction.user.avatar.url)
        embed.set_footer(text = f"{interaction.user.name}的個人資訊", icon_url = interaction.user.avatar.url)
        await interaction.send(embed = embed)

def setup(bot: commands.Bot):
    bot.add_cog(React(bot))