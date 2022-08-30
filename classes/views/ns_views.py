import discord
from discord.ui import View
from discord import SelectOption

from classes.modals.ns_modal import NS_Modal


class NS_View(View):
    @discord.ui.select(
        placeholder="Select a route",
        options=[SelectOption(label="To School", value="0"), SelectOption(label="To Home", value="1")],
    )
    async def select_callback(self, interaction, select):
        if select.values[0] == "0":
            await interaction.response.send_modal(NS_Modal())
        elif select.values[0] == "1":
            await interaction.response.send_message(NS_Modal())
