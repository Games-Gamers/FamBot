#!/usr/bin/env python3

import random
import os
import discord
from discord.ext import commands
from config.settings import DISCORD_TOKEN
from structs.responses import err_msg

client = discord.Client
bot = commands.Bot(command_prefix='f.')
bot.remove_command('help')



@bot.event
async def on_ready():
    random.seed()
    print("suh fam")

@bot.event
async def on_command_error(ctx, error):
    print(f'{ctx.author} tried to use {ctx.message.content}')
    print(error)
    await ctx.send(random.choice(err_msg))


# Grab all the .py files from the cogs directory and load them into the bot
# This lets us keep the main file simple and exports all command logic to the cogs files
cogs = [x.replace('.py', '') for x in os.listdir('cogs') if x.endswith('.py')]
for extension in cogs:
    try:
        bot.load_extension(f'cogs.{extension}')
        print(f'Loaded extension: {extension}')
    except Exception as e:
        print(f'LoadError: {extension}\n'
                f'{type(e).__name__}: {e}')

bot.run(DISCORD_TOKEN)
