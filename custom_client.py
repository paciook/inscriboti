import os
import discord
from dsheet import Datasheet

import configsenvs as cfg

class Custom_client(discord.Client):
    async def on_ready(self):
        print(f"{self.user} se conecto a Discord!")

        print("Estoy conectado a los siguientes servidores:")
        for guild in self.guilds:
            print(f"{guild}")

    async def on_message(self, message):
        if message.author == self.user or message.channel.name != cfg.CHANNEL_NAME:
            return


        if(not message.content.isnumeric()):
            return
        id_padron = int(message.content)


        alumnos = Datasheet(creds_path='credentials.json')
        
        if alumnos.doesExist(id_padron):
            await message.channel.send("El alumno con el padron " + str(id_padron) + " se llama " + alumnos.getName(id_padron))
            alumnos.inDiscord(id_padron)
