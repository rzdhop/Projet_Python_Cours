from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json
import sys, requests


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.x = 500
        self.y = 400
        self.initUI()

    def initUI(self):

        self.setFixedSize(self.x, self.y)
        self.setWindowTitle('Client Lourd par Rida')
        self.ipLabel = QLabel(self)
        self.ipLabel.setText("Entrez l'ip a geolocaliser :")
        self.ipEntree = QLineEdit(self)
        self.APILabel = QLabel(self)
        self.APILabel.setText("Entrez l'API :")
        self.APIEntree = QLineEdit(self)
        self.submitButton = QPushButton(self)
        self.submitButton.setText("Envoyer !")
        self.exitButton = QPushButton(self)
        self.exitButton.setText("Quitter")
        self.responseLabel = QPlainTextEdit(self)

       
        self.ipLabel.move(10, 10)
        self.ipEntree.move(10, 30)
        self.APILabel.move(10, 55)
        self.APIEntree.move(10, 75)
        self.submitButton.move(10, 100)
        self.exitButton.move(120, 100)
        self.responseLabel.move(10, 140)

        self.submitButton.clicked.connect(self.request)
        self.exitButton.clicked.connect(self.echap)

        self.show()

    def request(self):
        IP = self.ipEntree.text()
        API = self.APIEntree.text()
        if len(IP) < 7 :
            return
        response = requests.get(f"http://localhost:8000/{IP}/{API}")
        #https://www.openstreetmap.org/#map=18/
        loclist = [loc["location"].replace(',', '/') for loc in json.loads(response.json())]
        self.responseLabel.insertPlainText(f"{loc} -> https://www.openstreetmap.org/#map=18/{loc}" for loc in loclist)

    def echap(self):
        exit()



def main():
    app = QApplication(sys.argv)
    mainWindow = Window()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

 