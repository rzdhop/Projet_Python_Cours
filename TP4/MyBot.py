import discord
from dotenv import load_dotenv
import os
from argparse import ArgumentParser
import logging
from base64 import b64decode
from shodan import Shodan

#je declare l'objet Mybot qui repart de la base de la class discord.Client
class MyBot(discord.Client):
    def __init__(self, configFile: str):
        #appel le constructeur de la class mère
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
        #appelle le second constructeur
        self._localinit()
    
    def _localinit(self):
        #configure le fichier de log avec les informations au niveau 'DEBUG'
        logging.basicConfig(filename=self.logFile, level=logging.DEBUG)
        #exporte les valeurs du fichier en variables d'environnement du script
        load_dotenv(dotenv_path=self.configFile)
        #recupere les variables et les decodes (j'ai préféré les encodé légerement pour eviter les problemes avec github)
        self.discordtoken = str(b64decode(os.getenv("DISCORD_TOKEN")).decode())
        self.shodantoken = str(b64decode(os.getenv("SHODAN_TOKEN")).decode())
        #lance le bot
        self.run(self.discordtoken)
        
    async def on_ready(self):
        #quand le bot est prèt je m'informe sur le terminal et dans le logfile
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
                #ici j'utilise *args pour centraliser l'appel des fonctions peux importe le nombre d'args attendus
                #cela rend aussi facile la fututre implementation de fonctions
                await message.channel.send(self.command[key](*message.content.split()[1:]))

    #je defini cette methode en tant que detaché de la class elle n'attend pas d'objet en parametre
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
        
    #via cette fonction j'affiche les informations
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
        #je requete l'api pour avoir les infos par rapport a l'api
        try :
            rep = api.host(args[0])
        except Exception as e:
            return f"Attention ! {e}"
        #je formate les données pour afficher les coordonées
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

#dans cette fonction je recupère le nom du fichier de config contenant les clé d'API
def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "-c", "--config", help="Config file", required=True, dest="config"
    )
    return parser.parse_args()

def main():
    #on récupères les arguments passé au script
    args = parse_args()
    #récupere la valeur passé à l'execution du script
    configFile = args.config
    #instancie etlance le Bot
    TP4_pythonBot = MyBot(configFile)

if __name__ == "__main__":
    #execute la fonction main
    main()