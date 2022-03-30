from discord.ext import commands
import random
from structs.responses import sass, err_msg


memes = {
    'wets': [
        'https://c.tenor.com/AxZlzVC4rrMAAAAM/parmesan-parmiggiano.gif'
    ],
    'hurt': [
        'when you fell from someone\'s butthole into toilet water you piece of shit'
    ],
    'hava': [
        'HAVA NICE DAY LMAO GOTTEM FAM'
    ],
    'moves': [
        'https://c.tenor.com/ULv-OVA89isAAAAM/moves-are-weak-upper-hook.gif'
    ],
    'butthole': [
        '_ski-bap ba-dap **butthole**_\nhttps://c.tenor.com/fYkgtSeoiokAAAAC/tomcardy-have-you-checked-your-butthole.gif'
    ]
}


class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx, *args):
        meme_arg = ' '.join(args)
        print(f'{ctx.author} used f.meme: {meme_arg}')
        if 'wets' in meme_arg:
            await ctx.send(random.choice(memes['wets']))
        elif 'hurt' in meme_arg:
            await ctx.send(random.choice(memes['hurt']))
        elif 'hava'  in meme_arg:
            await ctx.send(random.choice(memes['hava']))
        elif 'moves' in meme_arg or 'weak' in meme_arg:
            await ctx.send(random.choice(memes['moves']))
        elif 'butthole' in meme_arg:
            await ctx.send(random.choice(memes['butthole']))
        else:
            ms = []
            for v in memes.values():
                ms= ms + v
            print(ms)
            await ctx.send(random.choice(ms))
        
    
    @commands.command()
    async def fam(self, ctx):
        """
        TODO: random 'fam' meme
        """
        print(f'{ctx.author} used f.fam')
        await ctx.send(random.choice(sass))

def setup(bot):
	bot.add_cog(Meme(bot)) 
