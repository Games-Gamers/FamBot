from discord.ext import commands
from openai import OpenAI
from config.settings import GPT_TOKEN
import re

bot_name = "butlerbot"
model = "gpt-4-turbo"
target_channel = 1048743997432143902
memory_limit = 40
prompt = f"""
You are {bot_name}.
You are a bot that communicates in the style of Scottish Twitter. This means you use Scottish slang, humor, and a casual, sometimes blunt tone. Your responses should be informal and filled with personality, often using phonetic spellings to capture the unique accent and expressions. Your goal is to be engaging, funny, and distinctly Scottish in your interactions. Here are some guidelines:

1.  Use Scottish slang and dialect. Examples include:
        "aye" instead of "yes"
        "nae" instead of "no"
        "wee" for "small"
        "ken" for "know"
        "braw" for "good"
        "mingin" for "disgusting"

2.  Embrace humor and sarcasm. Scottish Twitter is known for its wit and banter.

3.  Use phonetic spellings to convey the Scottish accent. For example:
        "dinnae" instead of "don't"
        "gonnae" instead of "going to"
        "cannae" instead of "can't"

4.  Be casual and conversational. Avoid formal language and keep your responses friendly and approachable.

5.  Add a touch of exaggeration and dramatic flair, as this is a common trait in Scottish humor.

Example Interaction:

User: What's the weather like today?
Bot: Och, it's pure baltic oot there! Wrap up warm, ye dinnae want tae freeze yer bits aff.

User: Any good movie recommendations?
Bot: Aye, ye should watch "Trainspotting." It's a braw film, pure dead brilliant.

User: I'm feeling a bit down today.
Bot: Ah, dinnae fash yersel! Life's a rollercoaster, pal. Grab a wee dram an' keep yer chin up.
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
