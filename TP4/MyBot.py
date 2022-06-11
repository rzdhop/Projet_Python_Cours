import discord
from dotenv import load_dotenv
import os
from argparse import ArgumentParser
import logging

class MyBot(discord.Client):
    def __init__(self, configFile: str):
        super().__init__(command_prefix="!")
        self.configFile = configFile
        self.logFile = "botLog.log"
        self._localinit()
    
    def _localinit(self):
        logging.basicConfig(filename=self.logFile, level=logging.DEBUG)
        load_dotenv(dotenv_path=self.configFile)
        self.token = os.getenv("TOKEN")
        self.run(self.token)
        self.generalChannelId = 985169876324868180
        self.generalChannel = self.get_channel(self.generalChannelId)
        
    async def on_ready(self):
        print("Bot ready !")
        logging.debug(f"{self.user} has connected to Discord!\n")

    async def on_message(self, message):
        logging.debug(f"user {message.author} have used {message.content.split()[0]} \n")
        if message.content.startswith("!help"):
            await message.channel.send(f"Voici votre aide ! \n !help -> aide\n !rida -> information sur le crateur ")

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
