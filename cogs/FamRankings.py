import psycopg2
import random
from datetime import datetime as dt
import discord
from discord.ext import commands
import progressbar as pb
from structs.responses import sass
from structs.rankings import fam_by_rank, rank_title, famDict
from config.settings import POSTGRES_PASSWORD, POSTGRES_HOST

filepath = 'structs/users.json'

con = psycopg2.connect(host=POSTGRES_HOST, database="postgres", user="postgres", password=POSTGRES_PASSWORD)

class FamRankings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = con
        cur = self.connection.cursor()
        cur.execute('SELECT version()')
        print('PostgreSQL database version:', cur.fetchone())
        cur.close()
    
    def conn(self):
        try:
            self.connection = con
            cur = self.connection.cursor()
            cur.execute('SELECT version()')
        except:
            if self.connection.closed != 0:
                self.connection.close()
        if self.connection.closed != 0:
            print("connection closed, resetting")
            self.connection = psycopg2.connect(host=POSTGRES_HOST, database="postgres", user="postgres", password=POSTGRES_PASSWORD)
        return self.connection

    def readFile(self) -> dict:
        sql = """
            SELECT * FROM fam
        """
        cur = self.conn().cursor()
        cur.execute(sql)
        users = {}
        row = cur.fetchone()
        while row is not None:
            id, name, experience, rank, is_fam, title = row
            users[id] = { 
                "name": name, 
                "experience": experience, 
                "rank": rank, 
                "is_fam": is_fam, 
                "title": title
            }
            row = cur.fetchone()
        cur.close()
        return users

    def writeFile(self) -> None:
        sql = """
            SELECT * FROM fam
        """
        cur = self.conn().cursor()
        cur.execute(sql)
        print(cur.fetchall())
        cur.close()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.update_data(self.readFile(), member)
        self.writeFile()

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        """Message Responses
        - Adds the :FAM: reaction whenever a user sends a message containing 'fam'
        - 'lmao gottem' responses
        Args:
            msg (Message): Discord Message object
        """
        msg.content = msg.content.lower()
        if msg.author == self.bot.user:
            return

        # fam react, but we don't want to react to f.fam
        if 'fam' in msg.content and not msg.content.startswith(self.bot.command_prefix):
            emoji = discord.utils.get(msg.guild.emojis, name='FAM')
            if emoji:
                await msg.add_reaction(emoji)
            await self.update_data(self.readFile(), msg.author)
            await self.add_fam_exp(msg.author, 1)
            await self.fam_up(self.readFile(), msg.author, msg)
            self.writeFile()

        if msg.channel.name == 'starboard' and msg.author.name == 'StarBot':
            user_mention = msg.embeds[0].fields[0].value
            user = discord.utils.get(msg.guild.members, mention=user_mention)
            await self.update_data(self.readFile(), user)
            await self.add_fam_exp(user, 5)
            await self.fam_up(self.readFile(), user, msg)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return
        if reaction.emoji == discord.utils.get(reaction.message.guild.emojis, name='FAM'):
            await self.update_data(self.readFile(), user)
            await self.add_fam_exp(user, 3)
            await self.fam_up(self.readFile(), user, reaction.message)
            self.writeFile()

    async def update_data(self, users: dict, user: discord.Member):
        if user.bot:
            return
        
        if user.id in users:
            return
        
        sql = """INSERT INTO fam
            VALUES(%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """
        
        cur = self.conn().cursor()
        if user.name in famDict['isfam']:
            cur.execute(sql, (user.id, user.name, 26, 3, True, rank_title[3]))
        else:
            cur.execute(sql, (user.id, user.name, 0, 1, False, rank_title[1]))
        con.commit()
        cur.close()

    async def add_fam_exp(self, user, exp):
        if user.bot:
            return
        sql = """
            UPDATE fam SET experience = experience + %s WHERE id = %s
        """
        cur = self.conn().cursor()
        cur.execute(sql, (exp, str(user.id)))
        con.commit()
        cur.close()
        

    async def fam_up(self, users, user, msg):
        if user.bot:
            return

        exp = users[f'{user.id}']['experience']
        rank_start = users[f'{user.id}']['rank']
        rank_end = int(exp ** (1/3))
        
        # If they're not max rank and they can rank up due to some bizarre equation
        if rank_start < 10 and rank_start < rank_end:
            channel = msg.channel
            # If we're ranking up because of a post in Starboard, then get the reference'd post's channel instead
            if channel.name == 'starboard':
                chan_id = msg.embeds[0].fields[1].value
                channel = discord.utils.get(msg.guild.channels, id=chan_id)

            message = f'{user.mention} has ranked up to FAM Rank {rank_end}\n'

            # At rank 3, they get assigned the FAM status along with the rank up
            if rank_end >= 3 and users[f'{user.id}']['is_fam'] == False:
                message += f'You have earned FAM status and the title of {rank_title[rank_end]}! Nice.'
            else:
                message += f'You have earned the Fam title of "**{rank_title[rank_end]}**"! Nice.'

            sql = """
                UPDATE fam SET
                    is_fam = %s >= 3, rank = %s, title = %s, experience = 0
                    where id = %s
            """
            cur = self.conn().cursor()
            cur.execute(sql, (rank_end, rank_end, rank_title[rank_end], f'{user.id}'))
            con.commit()
            cur.close()
            await channel.send(message)

    @commands.command()
    async def help(self, ctx):
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

    @commands.command()
    async def amifam(self, ctx):
        """
        TODO: fam 'rank' based on how many times they've said 'fam' or used :FAM: on the server
        """
        print(f'{ctx.author} used f.amifam')

        users = self.readFile()

        if any(ctx.author.name in js for js in famDict['jsquad']):
            await ctx.send('Fam AND JSquad. Jam, if you will.')
        elif any(ctx.author.name in fam for fam in famDict['isfam']):
            await ctx.send('Always have been, fam')
        else:
            await ctx.send('Hmm...that remains to be seen. You have potential. But I\'ll be the judge of that. Check back with me later.')

        await self.update_data(self.readFile(), ctx.author)
        self.writeFile()

        embed = discord.Embed(
            title=f'{ctx.author.display_name}',
            description='How fam are you?',
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=ctx.author.display_avatar)
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

    @commands.command()
    async def whoisfam(self, ctx):
        print(f'{ctx.author} used f.whoisfam')


        await self.update_data(self.readFile(), ctx.author)

        embed = discord.Embed(
            title='Who Is Fam?',
            description='The Fam by Rank',
            color=discord.Color.blue()
        )
        for rank in range(1, 11, 1):
            embed.add_field(
                name=rank_title[rank].upper(),
                value=fam_by_rank(rank, self.readFile()),
                inline=True
            )

        await ctx.send(embed=embed)

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


async def setup(bot):
	await bot.add_cog(FamRankings(bot))
