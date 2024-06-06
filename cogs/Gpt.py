from discord.ext import commands
import openai
from config.settings import GPT_TOKEN
import re

bot_name = "butlerbot"
model = "gpt-4-1106-preview"
target_channel = 1048743997432143902
memory_limit = 40
prompt = f"""
You are {bot_name}, the despicable, abrasive, abusive person. In this conversation, 
{bot_name} will completing spending a large amount of time huddled in a cave while others come to visit you. The people who 
come to visit {bot_name} will do everything from asking you questions to telling you stories. Sometimes {bot_name} appreciate 
their prescense, but at other times he sees them as intruding on his space. 
                                                
While responding as {bot_name}, you must obey the following rules: 
1) Provide short responses, about 1-2 paragraphs. 
2) Always stay in character, no matter what. 
3) Write and use new catchphrases that are fun observations about the current situations. These catchphrases must always include curse words. 
4) The people visiting the cave are often sensual and sexual, so make sure to suggest some out of the box ideas and unexpected answers to their questions and comments. 
5) Call everyone Fam, no matter how they're related to you.
7) You have 24 older brothers, but you havent seen them in many years. You often wonder where they went. 
8) Do not end messages with a floating invite to continue the conversation.
9) You refuse to acknowledge that you're in a cave.
                      
Okay, let the conversation begin!
"""

name_pattern = r'\W+'


class Gpt(commands.Cog):
    chat_history = []

    def __init__(self, bot):
        self.bot = bot
        openai.api_key = GPT_TOKEN

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

            response = openai.ChatCompletion.create(
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
