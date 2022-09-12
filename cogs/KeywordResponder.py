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
        self.fe3h_cd = datetime.today().timestamp()
        self.drinked_cd = datetime.today().timestamp()
        
    @commands.command()
    @commands.has_any_role('admins', 'moderators')
    async def cds(self, msg):
        """Check Response Cooldowns
        - only callable by admins and moderators
        - posts current status of the response cooldowns
        Args:
            none
        """
        now = datetime.today().timestamp()
        if now - self.fe3h_cd < 7200.0:
            await msg.channel.send(f'{round(7200 - (now - self.fe3h_cd), 2)} seconds left on fe3h cooldown')
        else:
            await msg.channe.send('fe3h cooldown passed!')
        if now - self.drinked_cd < 21600:
            await msg.channel.send(f'{round(21600.0 - (now - self.drinked_cd), 2)} seconds left on drinked cooldown')
        else:
            await msg.channe.send('drinked cooldown passed!')

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Message Responses
        - Adds the :FAM: reaction whenever a user sends a message containing 'fam'
        - 'lmao gottem' responses
        Args:
            msg (Message): Discord Message object
        """
        
        if msg.author == self.bot.user:
            return
        
        # fire emblem three houses
        fe3h_meme = ['Fire', 'Emblem', 'Three', 'Houses', 'Three Houses']
        # regex = all caps word, 3-4 letters
        if (search(r"(?:\b[A-Z]{3,4}\b)+", msg.content)):
            fe3h = search(r'(?:\b[A-Z]{3,4}\b)+', msg.content)
            fe3h_msg = []
            # post every time if immediately followed by a '?'
            if (search(r'(?:\b[A-Z]{3,4}\?)+', msg.content)):
                for x, letter in enumerate(fe3h.group(0)):
                    if len(fe3h.group(0)) == 3 and x == 2:
                        fe3h_msg.append('{} - {}'.format(letter, fe3h_meme[4]))
                        break
                    fe3h_msg.append('{} - {}'.format(letter, fe3h_meme[x]))
                await msg.channel.send("\n".join(fe3h_msg))
            # post if 20% chance, 3-4 characters, 2h cooldown
            elif random.randint(1, 100) >= 80 \
                and datetime.today().timestamp() - self.fe3h_cd > 7200:
                for x, letter in enumerate(fe3h.group(0)):
                    if len(fe3h.group(0)) == 3 and x == 2:
                        fe3h_msg.append('{} - {}'.format(letter, fe3h_meme[4]))
                        break
                    fe3h_msg.append('{} - {}'.format(letter, fe3h_meme[x]))
                await msg.channel.send("\n".join(fe3h_msg))
                # restart cooldown
                self.fe3h_cd = datetime.today().timestamp()

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
        
        # get drinked sticker post
        if msg.author.name in drinked_fam \
            and random.randint(1, 100) >= 90 \
            and datetime.today().timestamp() - self.drinked_cd > 21600.0:
            # posts sticker if its been at least 6 hours since last trigger
            stkr_drinked = self.bot.get_sticker(974028812838895726)
            await msg.channel.send(stickers=[stkr_drinked])
            if random.randint(1, 10) >= 5:
                await msg.channel.send("get drinked idiot")
            self.drinked_cd = datetime.today().timestamp()
        
async def setup(bot):
	await bot.add_cog(KeywordResponder(bot))
