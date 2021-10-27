import random
import discord
from discord.ext import commands
from config.settings import DISCORD_TOKEN
from re import search

client = discord.Client
bot = commands.Bot(command_prefix='f.')
bot.remove_command('help')

@bot.event
async def on_ready():
    print("suh")
    
@bot.event
async def on_message(msg):
    """Add FAM Reaction
    Adds the :FAM: reaction whenever a user sends a message containing 'fam'
    Args:
        msg (Message): Discord Message object
    """
    await bot.process_commands(msg)
    msg.content = msg.content.lower()
    if msg.author == bot.user or msg.content.startswith('f.'):
        return
    
    # fam react
    if 'fam' in msg.content:
        emoji = discord.utils.get(msg.guild.emojis, name='FAM')
        if emoji:
            await msg.add_reaction(emoji)
    
    # lmao gottem
    # if ' hava ' in msg.content:
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
    await ctx.send('idk yet, still feelin yall out')


bot.run(DISCORD_TOKEN)
