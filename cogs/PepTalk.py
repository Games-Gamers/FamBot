from discord.ext import commands
import random
from structs.responses import sass, err_msg


part1 = [
    "Champ,",
    "Fact:",
    "Everybody says",
    "Dang...",
    "Check it:",
    "Just saying...",
    "Superstar,",
    "Tiger,",
    "Self,",
    "Know this:",
    "News alert:",
    "Girl,",
    "Ace,",
    "Excuse me but",
    "Experts agree:",
    "In my opinion,",
    "Hear ye, hear ye:",
    "Okay, listen up:"
]
part2 = [
    "the mere idea of you",
    "your soul",
    "your hair today",
    "everything you do",
    "your personal style",
    "every thought you have",
    "that sparkle in your eye",
    "your presence here",
    "what you got going on",
    "the essential you",
    "your life's journey",
    "that saucy personality",
    "your DNA",
    "that brain of yours",
    "your choice of attire",
    "the way you roll",
    "whatever your secret is",
    "all of y'all"
]
part3 = [
    "has serious game,",
    "rains magic,",
    "deserves the Nobel Prize,",
    "raises the roof,",
    "breeds miracles,",
    "is paying off big time,",
    "shows mad skills,",
    "just shimmers,",
    "is a national treasure,",
    "gets the party hopping,",
    "is the next big thing,",
    "roars like a lion,",
    "is a rainbow factory,",
    "is made of diamonds,",
    "makes birds sing,",
    "should be taught in school,",
    "makes my world go 'round,",
    "is 100%% legit,"
]
part4 = [
    "24/7.",
    "can I get an amen?",
    "and that's a fact.",
    "so treat yourself.",
    "you feel me?",
    "that's just science.",
    "would I lie?",
    "for reals.",
    "mic drop.",
    "you hidden gem.",
    "snuggle bear.",
    "period.",
    "now let's dance.",
    "high five.",
    "say it again!",
    "according to CNN.",
    "so get used to it."
]

class PepTalk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def peptalk(self, ctx):
        message = random.choice(part1) + \
            "\n" + \
            random.choice(part2) + \
            "\n" + \
            random.choice(part3) + \
            "\n" + \
            random.choice(part4)

        await ctx.send(message)

async def setup(bot):
	await bot.add_cog(PepTalk(bot)) 
