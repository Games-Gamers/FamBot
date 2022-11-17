from discord.ext import commands
import discord
import random

class VCManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
            
        if before.afk != after.afk and after.afk:
            print(f'{member.name} is afk')
            

    # @commands.Cog.listener()
    # async def on_presence_update(self, before: discord.Member, after: discord.Member):
    #     print(f'{after.name}')
    #     if after.activity is not None \
    #         and after.activity.type == discord.ActivityType.watching:
    #             print(f'{after.name} is watching')

        
async def setup(bot):
    await bot.add_cog(VCManagement(bot))
