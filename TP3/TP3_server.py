from fastapi import FastAPI
import requests

app = FastAPI()

#Défini le chemin de l'API 
@app.get("/{IP}/{API}")
def read_root(IP, API):
    header = {
        "Authorization":f"apiKey {API}",
        "Content-Type":"application/json"
    }
    r = requests.get(f"https://www.onyphe.io/api/v2/simple/geoloc/{IP}", headers=header)

    return r.json()["results"]


#uvicorn TP3_server:app --reload
#login : rida@e-mail.cafe:FzugGiaNs6 key:603d5d2937621744d6de5519f2283155a32af272
#source ../../PythonVenv/bin/activate
#/mnt/c/Users/ridap/Documents/GitHub/Projet_Python_Cours