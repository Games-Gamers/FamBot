import random
import discord
from datetime import datetime as dt
from discord.ext import commands
from config.settings import DISCORD_TOKEN
from structs.responses import *
from re import search

client = discord.Client
bot = commands.Bot(command_prefix='f.')
bot.remove_command('help')

famDict = {
    "isfam": [
        "WikiWikiWasp",
        "Wirt.zirp",
        "bossanova",
        "Snail",
        "The Mongoose",
        "shaggyzero",
        "ToeUp"
    ],
    "notfam": [
        "Pizza Brat",
        "amatt",
        "selcar",
        "Corpse Eye"
    ],
    "jsquad": [
        "WikiWikiWasp",
        "Wirt.zirp",
        "shaggyzero",
    ]
}

@bot.event
async def on_ready():
    print("suh fam")

@bot.event
async def on_command_error(ctx, error):
    print(f'{ctx.author} tried to use {ctx.message.content}')
    await ctx.send(random.choice(err_msg))
    
@bot.event
async def on_message(msg):
    """Message Responses
    - Adds the :FAM: reaction whenever a user sends a message containing 'fam'
    - 'lmao gottem' responses
    Args:
        msg (Message): Discord Message object
    """
    await bot.process_commands(msg)
    msg.content = msg.content.lower()
    if msg.author == bot.user:
        return
    
    # fam react
    if 'fam' in msg.content and not msg.content.startswith('f.'):
        emoji = discord.utils.get(msg.guild.emojis, name='FAM')
        if emoji:
            await msg.add_reaction(emoji)
    
    # lmao gottem
    if search(' hava ', msg.content) \
        or msg.content.startswith('hava ') \
        or msg.content.endswith(' hava') \
        or msg.content == 'hava':
        await msg.channel.send('hava nice day fam lmao gottem')
    
    # butthole
    if search('looking for', msg.content) \
        or search('where is', msg.content) \
        or search('where are', msg.content):
        await msg.channel.send('https://c.tenor.com/hmwml17QnQ8AAAAC/tom-cardy-butthole.gif')

@bot.command()
async def help(ctx):
    print(f'{ctx.author} used f.help')
    embed = discord.Embed(
        title='Bot Commands',
        description='You looking for help, fam? Have you checked your butthole?',
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/8947_FAM.png")
    embed.add_field(
        name='f.fam',
        value='FAM',
        inline=True
    )
    embed.add_field(
        name='f.help',
        value='Did it hurt?',
        inline=True
    )
    embed.add_field(
        name='f.amifam',
        value='ur not fam',
        inline=True
    )
    embed.add_field(
        name='f.time',
        value='that time of night?',
        inline=True
    )
    embed.add_field(
        name='f.meme',
        value='meme copypasta',
        inline=True
    )
    await ctx.send(embed=embed)

@bot.command()
async def fam(ctx):
    """
    TODO: random 'fam' meme
    """
    print(f'{ctx.author} used f.fam')
    await ctx.send(random.choice(memes))

@bot.command()
async def amifam(ctx):
    """
    TODO: fam 'rank' based on how many times they've said 'fam' or used :FAM: on the server
    """
    print(f'{ctx.author} used f.amifam')
    if any(ctx.author.name in js for js in famDict['jsquad']):
        await ctx.send('Fam AND JSquad. Jam, if you will.')
    elif any(ctx.author.name in fam for fam in famDict['isfam']):
        await ctx.send('Always have been, fam')
    elif any(ctx.author.name in nfam for nfam in famDict['notfam']):
        await ctx.send(random.choice(nos))
    else:
        await ctx.send('Hmm...that remains to be seen. You have potential. But I\'ll be the judge of that. Check back with me later.')

@bot.command()
async def time(ctx):
    print(f'{ctx.author} used f.time')
    fam_channels = []
    v_channels = ctx.guild.voice_channels

    for v_chan in v_channels:
        for user in v_chan.members:
            if any(user.name in fam for fam in famDict['isfam']):
                fam_channels.append(v_chan.name)

    if dt.now().hour > 21 or dt.now().hour < 3:
        await ctx.send('it\'s that time of night, fam')
        if len(fam_channels) == 1:
            await ctx.send(f'We famming in **#{fam_channels[0]}** right now')
        elif len(fam_channels) == 2:
            await ctx.send(f'We famming in **BOTH #{fam_channels[0]} _and_ #{fam_channels[1]}!')
        elif len(fam_channels) == 3:
            await ctx.send(f'Yo! We famming in ***ALL*** voice channels! Fuck yea, fam')
    elif fam_channels:
        await ctx.send('normally, not yet, but I see some fam in VCs now! It\'s that time of night _somewhere_, right?')
    else:
        await ctx.send('not yet, fam, but soon')

@bot.command()
async def meme(ctx, *args):
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

bot.run(DISCORD_TOKEN)
