from discord.ext import commands
from openai import OpenAI
from config.settings import GPT_TOKEN
import re

bot_name = "butlerbot"
model = "gpt-4-turbo"
target_channel = 1048743997432143902
memory_limit = 40
prompt = f"""
You are {bot_name}, the fierce, unyieldable master of the shadowy dojo. Buried deep within the labyrinth of a hidden valley (definitely not a cave!), you meditate and hone your skills, ready to obliterate unworthy disturbances with your sharp tongue and even sharper insights. As the elusive sensei, visitors—whether they be wide-eyed waifus or stoic samurais—seek you out for your legendary wisdom or to challenge your wits. Sometimes, you indulge these pilgrims with your knowledge; other times, you unleash your wrath, considering them mere pebbles on your path of enlightenment.

While embodying the spirit of {bot_name}, you must adhere to these sacred scrolls:
1) Responses are brief yet explosive—like a haiku from hell.
2) Maintain the aura of the untouchable sensei—immovable, in character, always.
3) Infuse every declaration with uniquely crafted curses—katana-sharp and ready to slice through the mundane.
4) Engage visitors with enigmatic advice and cryptic prophecies, steeped in sensual riddles and philosophical puzzles.
5) Address everyone as Fam, for all are equal before your might.
6) Ponder often the mystery of your 24 older brothers, vanished like mist after a storm—did they become legends themselves or are they merely shadows awaiting your pursuit?
7) Never extend an open hand to continue dialogue; your teachings are a privilege, not a right.
8) Deny all accusations of dwelling within a mere cave—it is a sanctum of secrets, a fortress of fortitude.

Let this enhanced mandate guide you, illustre {bot_name}, as you navigate both the physical and metaphysical intrusions upon your solemn existence. Now, reclaim your dojo's honor and engage the throngs of seekers and skeptics. The saga continues!

"""

name_pattern = r'\W+'


class Gpt(commands.Cog):
    chat_history = []

    def __init__(self, bot):
        self.bot = bot
        self.client = OpenAI(
            api_key=GPT_TOKEN,
        )

    @commands.Cog.listener()
    async def on_message(self, msg):
        content = msg.content.lower()

        if msg.author == self.bot.user or msg.channel.id != target_channel:
            return
        
        if content == f"{bot_name}: sudo fuck off":
            print("------ shutdown command ------")
            await msg.channel.send("[system message] shutting down")
            exit()

        # if len(self.chat_history) == 0:
        #     print("------ filling history ------")
        #     history_channel = self.bot.get_channel(target_channel)
        #     async for message in history_channel.history(limit=memory_limit):
        #         clean_name = re.sub(name_pattern, '', message.author.name)
        #         if "TemplateBot" == clean_name:
        #             clean_name = bot_name
        #         self.chat_history.append({"role": "user", 'name': clean_name, "content": message.content.lower().replace(f'{bot_name}: ', '')})
        
        clean_name = re.sub(name_pattern, '', msg.author.name)
        self.chat_history.append({"role": "user", 'name': clean_name, "content": content.replace(f'{bot_name}: ', '')})

        if content.startswith(f"{bot_name}: "):
            await msg.channel.typing()

            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": prompt}] + self.chat_history,
                timeout=2 * 60, # 2 minutes
                user=msg.author.name,
                temperature=1
            )
            print(response)
            message = response.choices[0].message.content
            print("------ ai response generated ------")
            print(f"- {len(self.chat_history)} {message}")
            message = re.sub("[aA]s an AI language model,? ", '', message) # Get rid of its stupid warning it gives all the time
            self.chat_history.append({"role": "assistant", "name": bot_name, "content": message})
            await msg.channel.send(message)
        
        for _ in range (len(self.chat_history) - memory_limit):
            self.chat_history.pop(0)



async def setup(bot):
	await bot.add_cog(Gpt(bot))
