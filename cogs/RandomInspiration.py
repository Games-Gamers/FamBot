from discord.ext import commands
import random
import openai
from config.settings import GPT_TOKEN
import asyncio

url = "https://inspirobot.me/api?generateFlow=1"
min_hours = 1
max_hours = 12

bot_name = "butlerbot"
model = "gpt-4"

class RandomInspiration(commands.Cog):
    chat_history = []

    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.inspirationLoop())
        
        
    async def inspirationLoop(self):
        while True:
            sleep_hours = random.randint(min_hours, max_hours)
            print(f"RandomInspiration: sleeping for {sleep_hours} hours")
            chan = await self.bot.fetch_channel(382924474573389828)
            self.inspiration(chan)
    
    
    @commands.command()
    async def inspiration(self, ctx):
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": "generate an original toxic inspirational quote that isn't actually inspirational"}],
            timeout=30,
            temperature=1
        )
        print(response)
        message = response.choices[0].message.content
        await ctx.send(message)

async def setup(bot):
	await bot.add_cog(RandomInspiration(bot))
