from discord.ext import commands
from config.settings import DISCORD_TOKEN
import discord

bot = commands.Bot(command_prefix='f.')
bot.remove_command('help')

@bot.event
async def on_message(msg):
    """Add FAM Reaction
    Adds the :FAM: reaction whenever a user sends a message containing 'fam'
    Args:
        msg (Message): Discord Message object
    """
    msg.content = msg.content.lower()
    if msg.author == bot.user:
        return
    if 'fam' in msg.content:
        emoji = discord.utils.get(msg.guild.emojis, name='FAM')
        if emoji:
            await msg.add_reaction(emoji)

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
    pass

@bot.command()
async def amifam(ctx):
    """
    TODO: fam 'rank' based on how many times they've said 'fam' or used :FAM: on the server
    """
    pass

bot.run(DISCORD_TOKEN)
