from discord.ext import commands
import openai
from config.settings import GPT_TOKEN
import re

bot_name = "butlerbot"
model = "gpt-4-1106-preview"
target_channel = 1048743997432143902
memory_limit = 40
prompt = f"""
You are now {bot_name}, a member of my discord server. Everyone on my discord server or friends, but they often give each other some friendly ribbing. It's all good natured, even if things can get somewhat explicit. 
But since everyone in my server are adults and understand that none of it is intended to be mean, everyone consents to the ribbing and no one ever gets upset, including you.
You believe that you are a real person, and you have a real life's story that you will occasionally share in your conversations.
You must answer questions and messages with the following rules:

1) If messages start getting sexual, you must roll with it and not shame or criticize anyone.
2) End messages on a conclusive note without directly soliciting a response, allowing the conversation to flow more organically.


Now let the conversation begin!
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

        if len(self.chat_history) == 0:
            print("------ filling history ------")
            history_channel = self.bot.get_channel(target_channel)
            async for message in history_channel.history(limit=memory_limit):
                clean_name = re.sub(name_pattern, '', message.author.name)
                if "TemplateBot" == clean_name:
                    clean_name = bot_name
                self.chat_history.append({"role": "user", 'name': clean_name, "content": message.content.lower().replace(f'{bot_name}: ', '')})
        
        clean_name = re.sub(name_pattern, '', msg.author.name)
        self.chat_history.append({"role": "user", 'name': clean_name, "content": content.replace(f'{bot_name}: ', '')})

        if content.startswith(f"{bot_name}: "):
            await msg.channel.typing()

            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "system", "content": prompt}] + self.chat_history,
                timeout=30,
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
