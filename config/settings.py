import os
from dotenv import load_dotenv

load_dotenv()

# Discord
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GG_GUILD = os.getenv('GG_GUILD')
ERROR_CHANNEL = os.getenv('ERROR_CHANNEL')
LOG_CHANNEL = os.getenv('LOG_CHANNEL')
POSTGRES_PASSWORD = os.getenv('LOG_CHANNEL')