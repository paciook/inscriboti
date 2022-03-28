import os
import discord
from data_sheet import Datasheet
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
CHANNEL_NAME="administrativo-ingreso"

# Creating the connection with the Discord servers
client = discord.Client()

""" When connected, prints the a list of every server using it"""
@client.event
async def on_ready():
        print(f"{client.user} se conecto a Discord!")

        print("Estoy conectado a los siguientes servidores:")
        for guild in client.guilds:
            print(f"{guild}")


"""This function reads a new message only if it was sent on the Channel name specified when
    instanced. If a number, the bot checks that 'padron' over the spreadsheet given,
    adds a 'D' on its '_Discord' column, and reacts to the message"""
@client.event
async def on_message(message):
        # If my message or not in the correct channel dont do nothing
        if message.author == client.user or message.channel.name != CHANNEL_NAME:
            return

        # Thumbs down if it's not an int
        if(not message.content.isnumeric()):
            await message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        id_padron = int(message.content)
        alumnos = Datasheet(creds_path='credentials.json', spreadsheetId=SPREADSHEET_ID)

        # Search for the 'padron' on the spreadsheet. If not there, says it and leaves        
        if not alumnos.doesExist(id_padron):
            await message.reply("Mmm... perdoname, pero no tengo tu padron en mi lista")
            return
        
        # If the 'padron' is valid, it sets the user's nickname as his real name
        name = alumnos.getName(id_padron).split(', ')
        try:
            await message.author.edit(nick=f"{name[1]} {name[0]}")
        except:
            print("No puedo cambiarle el nickname al Dios del server")
        
        # Sets a 'D' on the '_Discord' column corresponding to that 'padron' and reacts
        # to the message
        alumnos.loggedInDiscord(id_padron)
        role = discord.utils.get(client.guilds[0].roles, name='1C2022')
        await message.author.add_roles(role)
        await message.add_reaction('\N{THUMBS UP SIGN}')

client.run(TOKEN)
