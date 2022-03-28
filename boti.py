import os
from custom_client import Custom_client
from dotenv import load_dotenv

# Creating the connection with the Discord servers
client = Custom_client()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)


