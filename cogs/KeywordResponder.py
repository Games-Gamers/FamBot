import discord
from discord.ext import commands
import random
from structs.responses import gottems
from re import search, findall
from datetime import datetime
from structs.responses import blowing

drinked_fam = [
    'bossanova',
    'Mulchbutler',
    'amatt',
    'Corpse Eye',
    'Cooler Guy Theoren',
    'The Mongoose',
    'ToeUp',
    'RuneCatCora',
    'The Dream',
    'shaggyzero',
    'Swegabyte',
    'Death(Lee)Hallows',
    'Jumper11550',
    'Pizza Brat'
]

class KeywordResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.drinked_cd = datetime.today().timestamp()
        
    @commands.command()
    @commands.has_any_role('admins', 'moderators')
    async def cds(self, msg: discord.Message):
        """Check Response Cooldowns
        - only callable by admins and moderators
        - posts current status of the response cooldowns
        Args:
            none
        """
        now = datetime.today().timestamp()
        if now - self.drinked_cd < 324000.0:
            await msg.channel.send(f'{round(324000.0 - (now - self.drinked_cd), 2)} seconds left on drinked cooldown')
        else:
            await msg.channel.send('drinked cooldown passed!')

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        """Message Responses
        - Adds the :FAM: reaction whenever a user sends a message containing 'fam'
        - 'lmao gottem' responses to "gottem" in msg
        - Get Drinked sticker post and sticker post reponse
        - Hava Nice Day meme response to "hava" in message
        - HYCYBH gif reponse to "where is/are" or "looking for" in msg
        - Manifesting response to matt's candle manifesting messages
        Args:
            msg (Message): Discord Message object
        """
        
        if msg.author == self.bot.user:
            return

        # lower case message content for remaining keywords
        content = msg.content.lower()

        # hava nice day
        if (search(' hava ', content) \
            or content.startswith('hava ') \
            or content.endswith(' hava') \
            or content == 'hava') \
            and not content.startswith("f.") \
            and random.randint(1, 100) >= 90:
            print(f'responding to "hava" from {msg.author}')
            await msg.channel.send('hava nice day fam lmao gottem')

        # lmao gottem
        if 'gottem' in content \
            and random.randint(1, 100) >= 90:
            print(f'responding to "gottem" from {msg.author}')
            await msg.channel.send(random.choice(gottems))

        # butthole
        if (search('looking for ', content) \
            or search('where is ', content) \
            or search('where are ', content)) \
            and random.randint(1, 100) >= 90:
            print(f'responding to "looking for / where is / where are" from {msg.author}')
            await msg.channel.send('https://c.tenor.com/hmwml17QnQ8AAAAC/tom-cardy-butthole.gif')

        # suh
        if (search('suh', content)):
            print(f'responding to "suh" from {msg.author}')
            await msg.channel.send('https://gfycat.com/adventurousfarazurewingedmagpie')
            
        # get drinked sticker response
        if len(msg.stickers) != 0:
            for sticker in msg.stickers:
                if 'drinked' in sticker.name.lower() \
                    and random.randint(1, 100) >= 60:
                    await msg.channel.send('IDIOT GOT DRINKED')
            
        # blow out matt's candles
        if msg.author.name == 'amatt' \
            and "🕯️" in content:
            # uwu ex dee
            await msg.reply("uwu :3")
            # r = random.randint(1, 100)
            # if r >= 66:
            #     print("reacting with emoji")
            #     await msg.add_reaction("🌬️")
            #     await msg.add_reaction("🕯️")
            # elif r >= 33:
            #     #candle blowing gifs
            #     await msg.reply(random.choice(blowing))
            # else:
            #     print("sending emoji")
            #     await msg.reply(":wind_blowing_face: :candle:")
        
async def setup(bot):
	await bot.add_cog(KeywordResponder(bot))
