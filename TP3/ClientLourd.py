from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys, requests

#on clée une class qui va permettre de gerer les element 
#QT de notre application
class Window(QWidget):
    def __init__(self):
        #on redefinit la class mère
        super().__init__()
        #j'initialise des valeures immuables au debut
        self.x = 500
        self.y = 400
        #je lance une fonction d'initalisation de la fenetre
        self.initUI()

    def initUI(self):
        #definit une taile fixe
        self.setFixedSize(self.x, self.y)
        #definit le nom de la fenetre QT
        self.setWindowTitle('Client Lourd par Rida')
        #instancie un label QT pour afficher du texte
        self.ipLabel = QLabel(self)
        self.ipLabel.setText("Entrez l'ip a geolocaliser :")
        #instancie un entree pour la saisie utilisateur
        self.ipEntree = QLineEdit(self)
        self.APILabel = QLabel(self)
        self.APILabel.setText("Entrez l'API :")
        self.APIEntree = QLineEdit(self)
        #definit les differents bouttons et le texte qu'ils contiennent
        self.submitButton = QPushButton(self)
        self.submitButton.setText("Envoyer !")
        self.exitButton = QPushButton(self)
        self.exitButton.setText("Quitter")
        self.responseLabel = QPlainTextEdit(self)

        #definit la position sur la fenetre des different widgets 
        self.ipLabel.move(10, 10)
        self.ipEntree.move(10, 30)
        self.APILabel.move(10, 55)
        self.APIEntree.move(10, 75)
        self.submitButton.move(10, 100)
        self.exitButton.move(120, 100)
        self.responseLabel.move(10, 140)

        #definit l'interuption lorque les bonttons sont cliqués
        self.submitButton.clicked.connect(self.request)
        self.exitButton.clicked.connect(self.echap)
        
        #affiches les differents widgets
        self.show()

    def request(self):
        #récupere les valeurs des differents champs
        IP = self.ipEntree.text()
        API = self.APIEntree.text()
        #verifie que l'ip fait la taille minimal
        if len(IP) < 7 :
            return
        #requete l'api local avec les donné fournis par les differents champs
        response = requests.get(f"http://localhost:8000/{IP}/{API}").json()["results"]
        
        #differentes modificvation pour formatter les données a l'usage de l'utilisateur
        loclist = [loc["location"].replace(',', '/') for loc in response]
        output = ""
        for loc in loclist:
            output += f"{loc} -> https://www.openstreetmap.org/#map=18/{loc}\n"

        #affiche les donnée formatter dans un chhamps prévu a cet effet
        self.responseLabel.insertPlainText(output)

    def echap(self):
        #si l'utilisateur quite l'application
        exit()



def main():
    #instancie l'application QT
    app = QApplication(sys.argv)
    #definit la fenetre QT (class ci-dessus)
    mainWindow = Window()
    #quit l'application apres l'execution du code (rentre aussi dans une boucle infini)
    sys.exit(app.exec_())

if __name__ == "__main__":
    #execute la fonction main
    main()

 