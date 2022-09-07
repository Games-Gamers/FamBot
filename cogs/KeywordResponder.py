from discord.ext import commands
import random
from structs.responses import gottems
from re import search
from datetime import datetime

drinked_fam = [
    'bossanova#1337',
    'Mulchbutler#5390',
    'amatt#6812',
    'Corpse Eye#0069',
    'Cooler Guy Theoren#1597',
    'The Mongoose#9414',
    'ToeUp#8008',
    'RuneCatCora#9833',
    'The Dream#2457',
    'shaggyzero#3303',
    'Swegabyte#4151',
    'Death(Lee)Hallows#9795',
    'Jumper11550#7419',
    'Llama Flow D#7971'
]

class KeywordResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start = datetime.today().timestamp()

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Message Responses
        - Adds the :FAM: reaction whenever a user sends a message containing 'fam'
        - 'lmao gottem' responses
        Args:
            msg (Message): Discord Message object
        """
        msg.content = msg.content.lower()
        if msg.author == self.bot.user:
            return

        # hava nice day
        if (search(' hava ', msg.content) \
            or msg.content.startswith('hava ') \
            or msg.content.endswith(' hava') \
            or msg.content == 'hava') \
            and not msg.content.startswith("f.") \
            and random.randint(1, 100) >= 90:
            print(f'responding to "hava" from {msg.author}')
            await msg.channel.send('hava nice day fam lmao gottem')

        # lmao gottem
        if 'gottem' in msg.content \
            and random.randint(1, 100) >= 90:
            print(f'responding to "gottem" from {msg.author}')
            await msg.channel.send(random.choice(gottems))

        # butthole
        if (search('looking for ', msg.content) \
            or search('where is ', msg.content) \
            or search('where are ', msg.content)) \
            and random.randint(1, 100) >= 90:
            print(f'responding to "looking for / where is / where are" from {msg.author}')
            await msg.channel.send('https://c.tenor.com/hmwml17QnQ8AAAAC/tom-cardy-butthole.gif')

        # suh
        if (search('suh', msg.content)):
            print(f'responding to "suh" from {msg.author}')
            await msg.channel.send('https://gfycat.com/adventurousfarazurewingedmagpie')
            
        # get drinked sticker response
        if len(msg.stickers) != 0 \
            and random.randint(1, 100) >= 60:
            for sticker in msg.stickers:
                if 'drinked' in sticker.name.lower():
                    await msg.channel.send('IDIOT GOT DRINKED')
        
        # get drinked sticker post
        if msg.author.name in drinked_fam \
            and random.randint(1, 100) >= 90 \
            and datetime.today().timestamp() - self.start > 21600.0:
            # posts sticker if its been at least 6 hours since last trigger
            stkr_drinked = self.bot.get_sticker(974028812838895726)
            await msg.channel.send(stickers=[stkr_drinked])
            if random.randint(1, 10) >= 5:
                await msg.channel.send("get drinked idiot")
            self.start = datetime.today().timestamp()
        
async def setup(bot):
	await bot.add_cog(KeywordResponder(bot))
