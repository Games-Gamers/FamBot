from discord.ext import commands
import re
import random
import openai

model = "gpt-4"
resp_prompt = f"""
I have a discord bot, "FamBot", that fixes links shared in the chat. Generate a response that the bot would reply with when posting the fixed link. Use a personality for the bot that's akin to a gamer, internet commenter, and zoomer. Just include the response without quotes or a placeholder for the link like '[fixed link]`
"""
class VideoLinkEmbeds(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = GPT_TOKEN

    @commands.Cog.listener()
    async def on_message(self, msg):
        # substrings to be inserted in url for fixing embeds
        sources = {
            "instagram.com": "dd",
            "tiktok.com": "vx",
            "twitter.com": "vx",
            "x.com": "vx",
        }

        ### hardcoded responses if gpt doesn't work out
        # responses = {
        #     "I gotchu, Fam",
        #     "Oopsie daisy, someone was lazy, but I'll fix it cuz I'm cRaZy lmao",
        #     "Well that didn't work. Here ya go.",
        #     "smh, I'll fix it",
        #     "Let's just go ahead and fix up that link real quick",
        #     "They really need to fix this already, but I gotchu",
        #     "That's another nickle in the 'Fambot is the GOAT' jar",
        #     "And some of yall have me blocked when I'm out here being helpful, smh"
        # }

        url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')

        msg.content = msg.content.lower()

        if msg.author == self.bot.user:
            return
        
        found_url = url_pattern.search(msg.content)

        # add substring into url
        if found_url:
            url = found_url.group()
            await msg.channel.typing()

            # gpt generated response
            gpt_response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": resp_prompt}],
                timeout=30
                user.msg.author.name
            )
            print(gpt_response)
            fambot_response = gpt_response.choices[0].message.content
            print("------ ai response generated ------")
            print(f"- {fambot_response}")

            for base, modification in sources.items():
                embed_url = url.replace(base, f"{modification}{base}")
                # await msg.channel.send(f'{random.choice(responses)}\n{embed_url}')
                await msg.channel.send(f'{fambot_response}\n{embed_url}')
                break # only fix a single link

async def setup(bot):
    await bot.add_cog(VideoLinkEmbeds(bot))