import os
from dotenv import load_dotenv

load_dotenv()

# Discord
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GG_GUILD = os.getenv('GG_GUILD')
ERROR_CHANNEL = os.getenv('ERROR_CHANNEL')
LOG_CHANNEL = os.getenv('LOG_CHANNEL')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
COFFEE_CHANNEL = os.getenv('COFFEE_CHANNEL')
GPT_TOKEN = os.getenv('GPT_TOKEN')