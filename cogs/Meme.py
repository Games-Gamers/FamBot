from discord.ext import commands
import random
from structs.responses import memes, err_msg


class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx, *args):
        print(f'{ctx.author} used f.meme')
        meme_arg = ' '.join(args)
        if 'wets' in meme_arg:
            await ctx.send('https://c.tenor.com/AxZlzVC4rrMAAAAM/parmesan-parmiggiano.gif')
        elif 'hurt' in meme_arg:
            await ctx.send('when you fell from someone\'s butthole into toilet water you piece of shit')
        elif 'hava'  in meme_arg:
            await ctx.send('HAVA NICE DAY LMAO GOTTEM FAM')
        elif 'moves' in meme_arg or 'weak' in meme_arg:
            await ctx.send('https://c.tenor.com/ULv-OVA89isAAAAM/moves-are-weak-upper-hook.gif')
        elif 'butthole' in meme_arg:
            await ctx.send('_ski-bap ba-dap **butthole**_')
            await ctx.send('https://c.tenor.com/fYkgtSeoiokAAAAC/tomcardy-have-you-checked-your-butthole.gif')
        else:
            await ctx.send(random.choice(err_msg))
        
    
    @commands.command()
    async def fam(self, ctx):
        """
        TODO: random 'fam' meme
        """
        print(f'{ctx.author} used f.fam')
        await ctx.send(random.choice(memes))

def setup(bot):
	bot.add_cog(Meme(bot)) 
