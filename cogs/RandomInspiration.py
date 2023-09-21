from discord.ext import commands
import random
from config.settings import LOG_CHANNEL
import asyncio
import requests
import re


url = "https://inspirobot.me/api?generateFlow=1"
min_hours = 1
max_hours = 12


class RandomInspiration(commands.Cog):
    chat_history = []

    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.inspirationLoop())
        
        
    async def inspirationLoop(self):
        while True:
            sleep_minutes = random.randint(min_hours, max_hours)
            print(f"RandomInspiration: sleeping for {sleep_hours} hours")
            await asyncio.sleep(sleep_hours * 60 * 60)
            x = requests.get(url)  
            message = re.sub("\[.+\]", '', x.json()['data'][1]['text'])
            chan = await self.bot.fetch_channel(382924474573389828)
            await chan.send(message)


async def setup(bot):
	await bot.add_cog(RandomInspiration(bot))
