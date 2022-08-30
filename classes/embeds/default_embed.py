import discord
from datetime import datetime


class DefaultEmbed(discord.Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_footer(text=f"🚀 Powered by Esie")
        self.timestamp = datetime.now()
