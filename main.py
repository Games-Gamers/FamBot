#!/usr/bin/env python3

import random
import os
import discord
from discord.ext import commands
from config.settings import DISCORD_TOKEN, ERROR_CHANNEL, LOG_CHANNEL
from structs.responses import err_msg
import asyncio

bot = commands.Bot(command_prefix='f.', intents=discord.Intents.all())
bot.remove_command('help')



@bot.event
async def on_ready():
    random.seed()
    print("suh fam")
    if (LOG_CHANNEL is not None):
        chan = await bot.fetch_channel(int(LOG_CHANNEL))
        await chan.send("suh fam")

@bot.event
async def on_command_error(ctx, error):
    print(f'{ctx.author} tried to use {ctx.message.content}')
    print(error)
    chan = ctx.guild.get_channel(int(ERROR_CHANNEL))
    await chan.send(f'yo...so...my moves were kinda weak in {ctx.message.jump_url}\n{error}')
    await ctx.send(random.choice(err_msg))

async def setup(bot: commands.Bot):
    # Grab all the .py files from the cogs directory and load them into the bot
    # This lets us keep the main file simple and exports all command logic to the cogs files
    cogs = [x.replace('.py', '') for x in os.listdir('cogs') if x.endswith('.py')]
    for extension in cogs:
        try:
            await bot.load_extension(f'cogs.{extension}')
            print(f'Loaded extension: {extension}')
        except Exception as e:
            print(f'LoadError: {extension}\n'
                    f'{type(e).__name__}: {e}')

async def main():
    await setup(bot)
    await bot.start(DISCORD_TOKEN)

asyncio.run(main())
