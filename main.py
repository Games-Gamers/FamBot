#!/usr/bin/env python3

import random
import json
import discord
from datetime import datetime as dt
from discord.ext import commands
from config.settings import DISCORD_TOKEN
from structs.responses import *
from structs.rankings import rank_title
import progressbar as pb
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
    "jsquad": [
        "WikiWikiWasp",
        "Wirt.zirp",
        "shaggyzero",
    ]
}

@bot.event
async def on_ready():
    random.seed()
    print("suh fam")

@bot.event
async def on_command_error(ctx, error):
    print(f'{ctx.author} tried to use {ctx.message.content}')
    print(error)
    await ctx.send(random.choice(err_msg))

@bot.event
async def on_member_join(member):
    with open('structs/users.json', 'r') as f:
        users = json.load(f)
    await update_data(users, member)
    with open('structs/users.json', 'w') as f:
        json.dump(users, f, indent=2)

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
        with open('structs/users.json', 'r') as f:
            users = json.load(f)
        await update_data(users, msg.author)
        await add_fam_exp(users, msg.author, 1)
        await fam_up(users, msg.author, msg)
        with open ('structs/users.json', 'w') as f:
            json.dump(users, f, indent=2)

    # lmao gottem
    if search(' hava ', msg.content) \
        or msg.content.startswith('hava ') \
        or msg.content.endswith(' hava') \
        or msg.content == 'hava' \
        and not msg.content.startswith("f."):
        await msg.channel.send('hava nice day fam lmao gottem')
    if 'gottem' in msg.content:
        await msg.channel.send(random.choice(gottems))

    # butthole
    if (search('looking for ', msg.content) \
        or search('where is', msg.content) \
        or search('where are', msg.content)) \
        and random.randint(1, 100) <= 10:
        await msg.channel.send('https://c.tenor.com/hmwml17QnQ8AAAAC/tom-cardy-butthole.gif')
        
    if msg.channel.name == 'starboard' and msg.author.name == 'StarBot':
        user_mention = msg.embeds[0].fields[0].value
        user = discord.utils.get(msg.guild.members, mention=user_mention)
        with open('structs/users.json', 'r') as f:
            users = json.load(f)
        await update_data(users, user)
        await add_fam_exp(users, user, 5)
        await fam_up(users, user, msg)
        

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return
    if reaction.emoji == discord.utils.get(reaction.message.guild.emojis, name='FAM'):
        with open('structs/users.json', 'r') as f:
            users = json.load(f)
        await update_data(users, user)
        await add_fam_exp(users, user, 3)
        # msg = user.fetch_message()
        await fam_up(users, user, reaction.message)
        with open ('structs/users.json', 'w') as f:
            json.dump(users, f, indent=2)

async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['name'] = user.name
        if user.name in famDict['isfam']:
            users[f'{user.id}']['experience'] = 26
            users[f'{user.id}']['rank'] = 3
            users[f'{user.id}']['is_fam'] = True
            users[f'{user.id}']['title'] = rank_title[3]
        else:
            users[f'{user.id}']['experience'] = 0
            users[f'{user.id}']['rank'] = 1
            users[f'{user.id}']['is_fam'] = False
            users[f'{user.id}']['title'] = rank_title[1]

async def add_fam_exp(users, user, exp):
    users[f'{user.id}']['experience'] += exp

async def fam_up(users, user, msg):
    # with open('structs/ranking.json', 'r') as g:
    #     rankings = json.load(g)
    exp = users[f'{user.id}']['experience']
    rank_start = users[f'{user.id}']['rank']
    rank_end = int(exp ** (1/3))
    
    if rank_start < rank_end:
        if msg.channel.name != 'starboard':
            await msg.channel.send(f'{user.mention} has ranked up to FAM Rank {rank_end}')
        else:
            chan_id = msg.embeds[0].fields[1].value
            chan = discord.utils.get(msg.guild.channels, id=chan_id)
            await chan.send(f'{user.mention} has ranked up to FAM Rank {rank_end}')
            
        users[f'{user.id}']['rank'] = rank_end
        
        if rank_end == 3 and users[f'{user.id}']['is_fam'] == False:
            if msg.channel.name != 'starboard':
                await msg.channel.send(f'You have earned FAM status and the title of {rank_title[rank_end]}! Nice.')
            else:
                chan_id = msg.embeds[0].fields[1].value
                chan = discord.utils.get(msg.guild.channels, id=chan_id)
                await chan.send(f'You have earned FAM status and the title of {rank_title[rank_end]}! Nice.')

            users[f'{user.id}']['is_fam'] = True
            famDict['isfam'].append(user.name)
        else:
            await msg.channel.send(f'You have earned the Fam title of "**{rank_title[rank_end]}**"! Nice.')
            
        users[f'{user.id}']['title'] = rank_title[rank_end]

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

    with open('structs/users.json', 'r') as f:
            users = json.load(f)

    if any(ctx.author.name in js for js in famDict['jsquad']):
        await ctx.send('Fam AND JSquad. Jam, if you will.')
    elif any(ctx.author.name in fam for fam in famDict['isfam']):
        await ctx.send('Always have been, fam')
    else:
        await ctx.send('Hmm...that remains to be seen. You have potential. But I\'ll be the judge of that. Check back with me later.')

    await update_data(users, ctx.author)
    embed = discord.Embed(
        title=f'{ctx.author.display_name}',
        description='How fam are you?',
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=ctx.author.avatar_url)
    if users[f'{ctx.author.id}']['is_fam'] or ctx.author.name in famDict['isfam']:
        embed.add_field(
            name='FAM?',
            value='<:FAM:848761741102153739>',
            inline=True
        )
    else:
        embed.add_field(
            name='FAM?',
            value='<:thor:669591170095120424>',
            inline=True
        )
    embed.add_field(
        name='RANK',
        value=users[f'{ctx.author.id}']['rank'],
        inline=True
    )
    embed.add_field(
        name='TITLE',
        value=users[f'{ctx.author.id}']['title'],
        inline=True
    )

    pb.generate_bar(users[f'{ctx.author.id}']['experience'], users[f'{ctx.author.id}']['rank'])
    exp_bar = discord.File("expbar.png")
    embed.set_image(url="attachment://expbar.png")

    await ctx.send(file=exp_bar, embed=embed)

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
            await ctx.send(f'We famming in **BOTH #{fam_channels[0]} _and_ #{fam_channels[1]}!**')
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
    else:
        await ctx.send(random.choice(err_msg))

bot.run(DISCORD_TOKEN)
