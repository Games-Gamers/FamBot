from discord.ext import commands
import random
from structs.responses import gottems
from config.settings import COFFEE_CHANNEL

coffeegifs = [
    "https://tenor.com/zmOp.gif",
    "https://tenor.com/bFJlh.gif",
    "https://tenor.com/bG2QW.gif",
    "https://tenor.com/bhfNl.gif",
    "https://tenor.com/bkXud.gif"
]

class CoffeeResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Message Responses
        - Adds the :FAM: reaction whenever a user sends a message containing 'fam'
        - 'lmao gottem' responses
        Args:
            msg (Message): Discord Message object
        """
        # msg.content = msg.content.lower()
        if msg.author == self.bot.user or str(msg.channel.id) != COFFEE_CHANNEL:
            return

        if len(msg.stickers) == 0:
            return
        
        coffeetime = 0
        for sticker in msg.stickers:
            if 'coffee' in sticker.name.lower():
                coffeetime += 1
        
        
        channel = await self.bot.fetch_channel(COFFEE_CHANNEL)
        async for message in channel.history(limit=10):
            if message.author == self.bot.user: # Bail out because we already sent a message about coffee recently
                return
            for sticker in message.stickers:
                if 'coffee' in sticker.name.lower():
                    coffeetime += 1

        if coffeetime > 3:
            await msg.channel.send(random.choice(coffeegifs))

async def setup(bot):
	await bot.add_cog(CoffeeResponder(bot))
