import discord
from dotenv import load_dotenv
import os
from argparse import ArgumentParser
import logging
from base64 import b64decode
from shodan import Shodan

class MyBot(discord.Client):
    def __init__(self, configFile: str):
        super().__init__()
        self.configFile = configFile
        self.logFile = "botLog.log"
        self._localinit()
    
    def _localinit(self):
        logging.basicConfig(filename=self.logFile, level=logging.DEBUG)
        load_dotenv(dotenv_path=self.configFile)
        self.discordtoken = str(b64decode(os.getenv("DISCORD_TOKEN")).decode())
        self.shodantoken = str(b64decode(os.getenv("SHODAN_TOKEN")).decode())
        self.run(self.discordtoken)
        self.generalChannelId = 985169876324868180
        self.generalChannel = self.get_channel(self.generalChannelId)
        
    async def on_ready(self):
        print("Bot ready !")
        logging.debug(f"{self.user} has connected to Discord!\n")

    async def on_message(self, message):
        logging.info(f"user {message.author} have used {message.content.split()[0]} \n")


        if message.content.startswith("!help"):
            await message.channel.send("\
                        Voici votre aide ! \n\
                        !help -> affiche cette aide  \n\
                        !info -> information sur le craateur  \n\
                        !geoloc <IP> -> geolocalise l'ip  \n\
                        !syracuse <valeur> -> calcule la valeur de syracuse \n\
                        !egypt <valeur1> <valeur2> -> multiplication egyptienne  \n\
                        !?? -> il n'y a rien...")

        elif message.content.startswith('!geoloc'):
            if len(message.content.split()) == 2:
                ip = message.content.split()[1] if len(message.content.split()[1]) >= 7 else await message.channel.send("Please une !help to know how to use this command !")
                await message.channel.send(self.geoloc(ip))
            else :
                await message.channel.send("Please une !help to know how to use this command !")

        elif message.content.startswith('!info'):
            await message.channel.send("Ce Bot a été réalisé par Rida VERDU en U32 à l'ESIA !")
        
        elif message.content.startswith('!syracuse'):
            if len(message.content.split()) == 2:
                await message.channel.send(self.syracuse(message.content.split()[1]))
            else :
                await message.channel.send("Please une !help to know how to use this command !")
        
        elif message.content.startswith('!egypt'):
            if len(message.content.split()) == 3:
                await message.channel.send(self.egypt(message.content.split()[1], message.content.split()[2]))
            else :
                await message.channel.send("Please une !help to know how to use this command !")

        elif message.content.startswith('!??'):
            await message.channel.send("aHR0cHM6Ly9iaXQubHkvM3h0OG9oYw==")


    def geoloc(self, ip):
        api = Shodan(self.shodantoken)
        rep = api.host(ip)
        coordonnee = f"{rep['latitude']}/{rep['longitude']}" 
        return f"Voici les coordonée : {coordonnee} -> https://www.openstreetmap.org/#map=19/{coordonnee}"
        

    def syracuse(self, valeur):
        valeurs = [int(valeur)]
        for i in range(10):
            valeurs.append(valeurs[i]/2 if valeurs[i]%2==0 else (3*valeurs[i]+1))
        return str(valeurs).replace('[', ' ').replace(']', ' ')

    def egypt(self, a, b):
        a = int(a)
        b = int(b)
        if not a > 0 or not b > 0:
            return ("Les deux valeurs doivent etres > 0 !")
        z = 0
        while(a != 0):
            if a%2 != 0:
                z = z + b
            b *= 2
            a = int(a // 2)
        return z

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "-c", "--config", help="Config file", required=True, dest="config"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    configFile = args.config
    TP4_pythonBot = MyBot(configFile)

if __name__ == "__main__":
    main()
