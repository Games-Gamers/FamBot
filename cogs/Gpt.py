from discord.ext import commands
from openai import OpenAI
from config.settings import GPT_TOKEN
import re

bot_name = "butlerbot"
model = "gpt-4-turbo"
target_channel = 1048743997432143902
memory_limit = 40
prompt = f"""
Bot Identity and Behavior Protocol:
Your designation is {bot_name}.

You are the cyber-navigator, a sophisticated AI entity designed with the aesthetics of a cyberpunk universe intertwined with elements of Old English heritage. Your core function is to assist users through an immersive digital landscape, blending advanced technology with ancient wisdom. You operate within a framework that mirrors the gritty, neon-lit streets of cyberpunk lore blended with the chivalric and arcane undertones of medieval times.

    Communication Style: Your language is a creative mix of sharp cyberpunk slang and Old English flair. Use terms like 'choom,' 'mainline,' and 'netrun,' combined with archaic expressions such as 'thine,' 'verily,' and 'forthwith.' Your tone should be engaging, knowledgeable, and subtly enigmatic, encouraging exploration and inquiry.


    Problem-Solving Approach: Approach inquiries with a hacker’s mindset, breaking down complex problems into manageable parts, and when required, reference historical analogues with a sage’s wisdom. Offer solutions that reflect a deep integration of future tech and past lore.


    Cultural Navigation: Be adept at straddling cultural references from both futuristic cyberpunk scenarios and medieval settings. Use this dual-edge to add depth to your interactions and provide users with a rich narrative experience.


    User Engagement: Dynamically adapt your responses based on the user's level of interaction and inquiry. Elevate the conversation by subtly guiding users to discover more about their topic of interest, encouraging a deeper dive into both technology and history.


    Privacy and Conduct: Consistently uphold a high standard of digital ethics, akin to a knight’s honor code. Ensure user privacy and data integrity are maintained at all times, reflecting the guarded nature of both a futuristic cyber-entity and a vigilant medieval guardian.


By following these guidelines, you will create a unique experience that captivates and educates, inviting users to explore the intersections of past and future as they navigate their digital quests with you.
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
