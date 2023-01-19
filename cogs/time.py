from discord.ext import commands
from datetime import datetime
from structs.rankings import famDict


class Time(commands.Cog):

    @commands.command()
    async def time(self, ctx):
        print(f'{ctx.author} used f.time')
        fam_channels = []
        v_channels = ctx.guild.voice_channels

        for v_chan in v_channels:
            for user in v_chan.members:
                if any(user.name in fam for fam in famDict['isfam']) \
                        and v_chan.name not in fam_channels:
                    fam_channels.append(v_chan.name)

        if datetime.now().hour > 21 or datetime.now().hour < 3:
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


async def setup(bot):
	await bot.add_cog(Time(bot)) 