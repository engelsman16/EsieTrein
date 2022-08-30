from discord.ui import Button, View
import discord
from discord import Embed, app_commands

from discord.ext import commands
from datetime import timedelta

from classes.embeds.default_embed import DefaultEmbed

from classes.modals.ns_modal import NS_Modal

from classes.views.ns_views import NS_View
from guildlist import guildlist


class NS(commands.Cog, name="ns"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(
        name="ns",
        description="check your train",
    )
    @app_commands.checks.cooldown(1, 60, key=lambda i: (i.guild.id, i.user.id))
    async def set(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=DefaultEmbed(
                title="Mineuk!",
                description="Please select a route",
                color=discord.Color.from_rgb(255, 201, 23),
            ),
            view=NS_View(),
            ephemeral=True,
        )

    @set.error
    async def commandSet_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(timedelta(seconds=int(error.retry_after)))
            embed = DefaultEmbed(
                title=f"⛔ Error!",
                description=f"Please wait {timeRemaining} seconds before executing this command again!",
                color=discord.Color.from_rgb(255, 0, 0),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(NS(bot), guilds=guildlist)
