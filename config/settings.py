import os
from dotenv import load_dotenv

load_dotenv()

# Discord
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GG_GUILD = os.getenv('GG_GUILD')
ERROR_CHANNEL = os.getenv('ERROR_CHANNEL')
