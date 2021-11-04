import random
import discord
from datetime import datetime as dt
from discord.ext import commands
from config.settings import DISCORD_TOKEN
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

famList = [
    "WikiWikiWasp",
    "Wirt.zirp",
    "bossanova",
    "Snail",
    "The Mongoose",
    "shaggyzero",
    "ToeUp"
]

@bot.event
async def on_ready():
    print("suh")
    
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
    
    #if msg.content.startswith("f.") and msg.content is not in bot.commands.
    
    # fam react
    if 'fam' in msg.content:
        emoji = discord.utils.get(msg.guild.emojis, name='FAM')
        if emoji:
            await msg.add_reaction(emoji)
    
    # lmao gottem
    if search(' hava ', msg.content) \
        or msg.content.startswith('hava ') \
        or msg.content.endswith(' hava') \
        or msg.content == 'hava':
        await msg.channel.send('hava nice day fam lmao gottem')

@bot.command()
async def help(ctx):
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
    memes = [
        'ur just fucking dying',
        'ur not fam',
        'u look like a bird',
        'look at your hair\nnow look at mine',
        '**F A M**',
        'please touch it',
        'did it hurt?\nwhen you fell from someone\'s butthole into toilet water you piece of shit',
        'w o w',
        'oh hi, mark',
        'ur moves are weak',
        'please...my wets',
        discord.utils.get(ctx.guild.emojis, name='FAM'),
        discord.utils.get(ctx.guild.emojis, name='sideeye'),
        discord.utils.get(ctx.guild.emojis, name='thor')
    ]

    meme = random.choice(memes)
    await ctx.send(meme)

@bot.command()
async def amifam(ctx):
    """
    TODO: fam 'rank' based on how many times they've said 'fam' or used :FAM: on the server
    """
    # await ctx.send('idk yet, still feelin yall out')
    nos = [
        'lol no',
        'u wish',
        'ur moves are too weak to be fam',
        'not yet',
        'ur fam...ously stupid lmao gottem',
        'u look like a bird',
        'ur just a superdick',
        'go play away and do something in ur life',
        'ur just a real stupid'
    ]

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
    meme_arg = ' '.join(args)
    if 'wets' in meme_arg:
        await ctx.send('https://c.tenor.com/AxZlzVC4rrMAAAAM/parmesan-parmiggiano.gif')
    elif 'hurt' in meme_arg:
        await ctx.send('when you fell from someone\'s butthole into toilet water you piece of shit')
    elif 'hava'  in meme_arg:
        await ctx.send('HAVA NICE DAY LMAO GOTTEM FAM')
    elif 'moves' in meme_arg or 'weak' in meme_arg:
        await ctx.send('https://c.tenor.com/ULv-OVA89isAAAAM/moves-are-weak-upper-hook.gif')

bot.run(DISCORD_TOKEN)
