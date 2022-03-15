from discord.ext import commands
import random
from structs.responses import gottems
from re import search



class KeywordResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Message Responses
        - Adds the :FAM: reaction whenever a user sends a message containing 'fam'
        - 'lmao gottem' responses
        Args:
            msg (Message): Discord Message object
        """
        msg.content = msg.content.lower()
        if msg.author == self.bot.user:
            return

        # lmao gottem
        if 'gottem' in msg.content:
            await msg.channel.send(random.choice(gottems))

        # butthole
        if (search('looking for ', msg.content) \
            or search('where is ', msg.content) \
            or search('where are ', msg.content)) \
            and random.randint(1, 100) >= 90:
            await msg.channel.send('https://c.tenor.com/hmwml17QnQ8AAAAC/tom-cardy-butthole.gif')




def setup(bot):
	bot.add_cog(KeywordResponder(bot))
