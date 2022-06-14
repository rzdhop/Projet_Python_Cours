from fastapi import FastAPI
import requests

#Instantiation de fastapi
app = FastAPI()

#Défini le chemin de l'API et les variables attendues
@app.get("/{IP}/{API}")
def read_root(IP, API):
    #ici l'on defini le header de la requete afin que le server traite notre requete comme
    #nous le voulons
    header = {
        "Authorization":f"apiKey {API}",
        "Content-Type":"application/json"
    }
    #ici on process la request GET et stock la réponse dans la variable reponse
    reponse = requests.get(f"https://www.onyphe.io/api/v2/simple/geoloc/{IP}", headers=header)
        
    #on retourne ensuite une reponse au demandeur de fastAPI au format json
    return reponse.json()


#uvicorn TP3_server:app --reload
#sample ip 149.62.158.57 (esiea.fr)
# email jetable...
#login : rida@e-mail.cafe:FzugGiaNs6 key:603d5d2937621744d6de5519f2283155a32af272