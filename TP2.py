import pandas as pd 
import seaborn as sns

df_entite = pd.read_csv("full-oldb-20220110/nodes-addresses.csv")
df_officers = pd.read_csv("full-oldb-20220110/nodes-officers.csv")

print("\n\nExo 1 : \n")

print("Nombre d'entitÃ©es : " + str(len(df_entite[df_entite["sourceID"].str.lower() == "offshore leaks"]["countries"].value_counts())))
print("Irland apparait : " + str(len(df_entite[df_entite["countries"].str.lower() == "ireland"])) + " fois.")
print("El Portador appait : " + str(len(df_officers[df_officers["name"].str.lower() == "el portador"])) + " fois.")


print("\n\nExo 2 : \n")

sns.countplot(x="countries", data=df_entite[df_entite["sourceID"].str.lower() == "offshore leaks"])

df_entite[df_entite["sourceID"].str.lower() == "offshore leaks"].groupby(["countries"]).size().sort_values(ascending=False)[:20]