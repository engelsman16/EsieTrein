import json
import discord
from discord.ext import commands, tasks
import http.client, urllib.request, urllib.parse, urllib.error, base64

class TreinCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check.start()
        
    def cog_unload(self):
      self.check.cancel()
    
    @commands.Cog.listener()
    async def on_ready_cock(self):
      print("TreinCheck is ready")

    @tasks.loop(seconds=10)
    async def check(self):
        headers = {
          # Request headers
          'Ocp-Apim-Subscription-Key': 'f299fb5b81e8454bade4f07770d1b5e5',
        }
        
        params = urllib.parse.urlencode({
          # Request parameters
          'originUicCode': '8400339',
          'destinationUicCode': '8400206',
          'dateTime': '2022-09-01T08:00',
        })
        
        try:
          conn = http.client.HTTPSConnection('gateway.apiportal.ns.nl')
          conn.request("GET", "/reisinformatie-api/api/v3/trips?%s" % params, "{body}", headers)
          response = conn.getresponse()
          data = response.read().decode('utf-8')
          dataobj = json.loads(data)
          print(dataobj["trips"][0]['status'])
          conn.close()
        except Exception as e:
          print(e)

    @check.before_loop
    async def before_check(self):
        print('waiting...')
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(TreinCheck(bot))