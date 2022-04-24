from nextcord.ext import commands 
from nextcord import *

guilds = []

class React(commands.Cog, name = "Reaction Command"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        for el in self.bot.guilds:
            guilds.append(int(el))

    @slash_command(description = "return with latency", guild_ids = guilds)
    async def ping(self, interaction: Interaction):
        embed = Embed(title = '機器人延遲狀態', description = 'Pong !', color = Colour.dark_gold())
        embed.add_field(name = "Latency", value = f"{round(self.bot.latency * 1000)} ms")
        await interaction.send(embed = embed)

def setup(bot: commands.Bot):
    bot.add_cog(React(bot))