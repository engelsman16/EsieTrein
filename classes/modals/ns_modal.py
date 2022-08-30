import discord
from discord.ui import Modal, TextInput
from classes.embeds.default_embed import DefaultEmbed


class NS_Modal(Modal, title="Rijdt jouw kanker trein?!"):

    hour = TextInput(label="hour", style=discord.TextStyle.short, required=True, max_length=2)
    minutes = TextInput(label="minutes", style=discord.TextStyle.short, required=True, max_length=2)

    async def on_submit(self, interaction: discord.Interaction):
        data = {
            "hour": self.hour.value,
            "minutes": self.minutes.value,
        }

        if int(data["hour"]) < 0 or int(data["hour"]) > 23 or int(data["minutes"]) < 0 or int(data["minutes"]) > 59:
            embed = DefaultEmbed(
                title="⛔ Error!",
                description="Please enter a valid hour and minutes!",
                color=discord.Color.from_rgb(255, 0, 0),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if int(data["hour"]) < 10:
            data["hour"] = "0" + data["hour"]
        if int(data["minutes"]) < 10:
            data["minutes"] = "0" + data["minutes"]

        await interaction.response.send_message(f"{data}")
