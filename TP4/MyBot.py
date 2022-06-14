import discord
from dotenv import load_dotenv
import os
from argparse import ArgumentParser
import logging
from base64 import b64decode
from shodan import Shodan

#je declare l'objet Mybot qui repart de la base de la class deicord.Client
class MyBot(discord.Client):
    def __init__(self, configFile: str):
        #appel le constructeur de la class mere
        super().__init__()
        self.configFile = configFile
        self.logFile = "botLog.log"
        #defini une bibliothèque de fonctionnalité du bot
        self.command = {
            "!help": self.help,
            "!info" : self.info,
            "!geoloc" : self.geoloc,
            "!syracuse" : self.syracuse,
            "!egypt" : self.egypt,
            "!??" : self.wht}
        #appel le constructeur fait par nous
        self._localinit()
    
    def _localinit(self):
        #configure le fichier de log avec une information de niveau 'DEBUG'
        logging.basicConfig(filename=self.logFile, level=logging.DEBUG)
        #export les valuer du fichier en variables d'environnement
        load_dotenv(dotenv_path=self.configFile)
        #recupere les variables et les decodes (j'ai préférer les encodé legerement pour evire les problemes avec github)
        self.discordtoken = str(b64decode(os.getenv("DISCORD_TOKEN")).decode())
        self.shodantoken = str(b64decode(os.getenv("SHODAN_TOKEN")).decode())
        #lance le bot
        self.run(self.discordtoken)
        
    async def on_ready(self):
        #quand le bot est pres je m'informe sur le terminal et dans le logfile
        print("Bot ready !")
        logging.debug(f"{self.user} has connected to Discord!\n")

    async def on_message(self, message):
        #je teste le message reçu pour savoir s'il s'agit d'une commande ou non
        try :
            if message.content[0] == '!':
                logging.info(f"user {message.author} have used {message.content.split()[0]} \n")
        except IndexError:
            pass
        
        #selon la commande si elle est presente dans notre bibliothèque de fonctions
        for key in self.command:
            if message.content.startswith(key):
                #ici j'utilise *args pour centraliser l'appel des fonction peux importe le nombre d'args attendus
                await message.channel.send(self.command[key](*message.content.split()[1:]))

    #je defini cette methode en tant que detaché de la class elle n'attend pas d'ojet en parametre
    @staticmethod
    def help(*args):
        return """
            Voici votre aide ! \n\
                    !help -> affiche cette aide  \n\
                    !info -> information sur le createur  \n\
                    !geoloc <IP> -> geolocalise l'ip  \n\
                    !syracuse <valeur> -> calcule la valeur de syracuse \n\
                    !egypt <valeur1> <valeur2> -> multiplication egyptienne  \n\
                    !?? -> il n'y a rien...
            """
    #via cette fonction j'affiche les informtions
    @staticmethod
    def info(*args):
        return "Ce Bot a été réalisé par Rida VERDU en U32 à l'ESIA !"

    #petit easter egg ;)
    @staticmethod
    def wht(*args):
        return "aHR0cHM6Ly9iaXQubHkvM3h0OG9oYw=="
    
    def geoloc(self, *args):
        #ici je teste l'entree de l'utiliateur pour voir s'il s'agis au minimun d'une ip et si des arguments sont passé
        try : 
            if len(args[0]) <= 7 :
                return "Utilisez !help pour apprendre a utiliser cette commande"
        except IndexError:
            return "Utilisez !help pour apprendre a utiliser cette commande"
        #j'instancie une connection a l'api avec mon token api
        api = Shodan(self.shodantoken)
        #je requete l'api pour avoir les info par rapport a l'api
        rep = api.host(args[0])
        #je formate les donnée pour afficher les coordoné"
        coordonnee = f"{rep['latitude']}/{rep['longitude']}"
        #je retourne les coordonée et un lien pour une visualisation directe sur openstreetmap 
        return f"Voici les coordonée : {coordonnee} -> https://www.openstreetmap.org/#map=19/{coordonnee}"
        
    @staticmethod
    def syracuse(*args):
        #je teste le nombre d'arguments passé
        if len(args) != 1:
            return "Utilisez !help pour apprendre a utiliser cette commande"
        
        valeurs = [int(args[0])]
        for i in range(10):
            valeurs.append(valeurs[i]/2 if valeurs[i]%2==0 else (3*valeurs[i]+1))
        return str(valeurs).replace('[', ' ').replace(']', ' ')

    @staticmethod
    def egypt(*args):
        if len(args) != 2:
            return "Utilisez !help pour apprendre a utiliser cette commande"
        
        a = int(args[0])
        b = int(args[1])
        if not a > 0 or not b > 0:
            return ("Les deux valeurs doivent etres > 0 !")
        z = 0
        while(a != 0):
            if a%2 != 0:
                z = z + b
            b *= 2
            a = int(a // 2)
        return z

#dans cette focntion recupere le nom du fichier de config avec les token api
def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "-c", "--config", help="Config file", required=True, dest="config"
    )
    return parser.parse_args()

def main():
    #on récupères les argumetn passé au script
    args = parse_args()
    #récupere la valeur passé a l'execution du script
    configFile = args.config
    #instancie et lance le Bot
    TP4_pythonBot = MyBot(configFile)

if __name__ == "__main__":
    #execute la fonction main
    main()
