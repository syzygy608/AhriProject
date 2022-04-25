from nextcord.ext import commands, application_checks
from nextcord import Interaction, slash_command, Colour, Embed, SlashOption

class Admin(commands.Cog, name = "Admin"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description = "loading target cog", force_global = True)
    @application_checks.is_owner()
    async def reload(self, interaction: Interaction, module: str = SlashOption(name = "module", description = "Enter module's name", required = True)):
        try:
            self.bot.unload_extension(f"cmds.{module}")
            self.bot.load_extension(f"cmds.{module}")
        except Exception as e:
            await interaction.send(f"**{type(e).__name__}: {e}**")
        else:
            await interaction.send(f"**Module {module} reloaded.**")

def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))

