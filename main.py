from datetime import datetime
from config import settings
import discord
from discord.ext import commands


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
            application_id=settings.APPID,
            activity=discord.Activity(type=discord.ActivityType.watching, name="rule 34 mineuk"),
        )

    async def setup_hook(self):
        await bot.tree.sync(guild=discord.Object(id=959010133273370664))  # Esie
        bot.remove_command("help")

    async def on_ready(self):
        print(f"{self.user} Initialised {datetime.now()}")


bot = MyBot()
bot.run(settings.TOKEN)
