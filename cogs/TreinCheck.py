import json
from time import strptime
import discord
from discord.ext import commands, tasks
import http.client, urllib.request, urllib.parse, urllib.error, base64
import datetime

from config import settings

embedExists = None
msg = None


class TreinCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check.start()

    def cog_unload(self):
        self.check.cancel()

    async def send_embed(self, data):
        global embedExists
        global msg

        train_status = data["trips"][0]["status"]
        cancel_status = data["trips"][0]["legs"][0]["cancelled"]
        origin_station = data["trips"][0]["legs"][0]["origin"]["name"]
        destination_station = data["trips"][0]["legs"][0]["destination"]["name"]
        train_name = data["trips"][0]["legs"][0]["product"]["displayName"]
        train_number = data["trips"][0]["legs"][0]["product"]["number"]
        planned_data = data["trips"][0]["legs"][0]["origin"]["plannedDateTime"]
        actual_data = data["trips"][0]["legs"][0]["origin"]["actualDateTime"]

        objdate = datetime.datetime.strptime(actual_data, "%Y-%m-%dT%H:%M:%S%z")
        correctdate = objdate.strftime("%H:%M")

        objdate2 = datetime.datetime.strptime(planned_data, "%Y-%m-%dT%H:%M:%S%z")
        correctdate2 = objdate.strftime("%H:%M")

        delay = int(correctdate[3:]) - int(correctdate2[3:])

        if cancel_status == False and train_status == "NORMAL":
            description = f"Your train is planned to depart at {correctdate2}"
            color = discord.Color.from_rgb(0, 255, 0)
        elif cancel_status == True:
            description = f"Your train is cancelled!"
            color = discord.Color.from_rgb(255, 0, 0)
        elif delay > 0:
            description = f"Your train is delayed by {delay} minutes and will now deprated at {correctdate}"
            color = discord.Color.from_rgb(255, 255, 0)

        embed = discord.Embed(title=f"🚅 Esie NS 🚅", description=description, color=color)
        embed.add_field(name="Train", value=f"{train_name} {train_number}", inline=False)
        embed.add_field(name="Origin", value=f"{origin_station}", inline=False)
        embed.add_field(name="Destination", value=f"{destination_station}", inline=False)
        # embed.add_field(name="Cancelled", value=f"{cancel_status}", inline=False)

        now = datetime.datetime.now()
        now_time = now.strftime("%H:%M:%S")

        embed.set_footer(text="🚀 Powered by Esie || Lastest update: " + now_time)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/991385769518305342/1014608644022743120/unknown.png")

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=train_status))
        channel = self.bot.get_channel(settings.CHANNELID)

        if embedExists == False:
            print("Embed does not exist, sending embed")
            await channel.purge(limit=10)
            msg = await channel.send(embed=embed)
            embedExists = True
        elif embedExists == True:
            newembed = discord.Embed(
                title=f"🚅 Esie NS 🚅",
                description=f"Your train will depart at {correctdate}" if cancel_status == False else f"Your train is cancelled!",
                color=discord.Color.from_rgb(0, 255, 0) if cancel_status == False and train_status == "NORMAL" else discord.Color.from_rgb(255, 0, 0),
            )

            newembed.add_field(name="Train", value=f"{train_name} {train_number}", inline=False)
            newembed.add_field(name="Origin", value=f"{origin_station}", inline=False)
            newembed.add_field(name="Destination", value=f"{destination_station}", inline=False)
            # embed.add_field(name="Cancelled", value=f"{cancel_status}", inline=False)

            newembed.set_footer(text="🚀 Powered by Esie || Lastest update: " + now_time)
            newembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/991385769518305342/1014608644022743120/unknown.png")

            await msg.edit(embed=newembed)
            print("Embed edited.")

    @commands.Cog.listener()
    async def on_ready_cock(self):
        print("TreinCheck is online")

    @tasks.loop(seconds=60)
    async def check(self):
        time = datetime.datetime.now() + datetime.timedelta(days=1)
        headers = {
            # Request headers
            "Ocp-Apim-Subscription-Key": settings.APIKEY,
        }

        params = urllib.parse.urlencode(
            {
                # Request parameters
                "originUicCode": "8400339",
                "destinationUicCode": "8400206",
                "dateTime": time.strftime("%Y-%m-%d") + "T08:00",
            }
        )

        try:
            conn = http.client.HTTPSConnection("gateway.apiportal.ns.nl")
            conn.request("GET", "/reisinformatie-api/api/v3/trips?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read().decode("utf-8")
            dataobj = json.loads(data)
            await self.send_embed(dataobj)
            conn.close()

        except Exception as e:
            print(e)

    @check.before_loop
    async def before_check(self):
        global embedExists
        print("waiting...")
        embedExists = False
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(TreinCheck(bot))
