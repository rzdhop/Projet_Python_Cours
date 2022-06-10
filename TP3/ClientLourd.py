from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from json import dumps
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
        self.submitButton = QPushButton(self)
        self.submitButton.setText("Envoyer !")
        self.exitButton = QPushButton(self)
        self.exitButton.setText("Quitter")
        self.responseLabel = QPlainTextEdit(self)

       
        self.ipLabel.move(10, 10)
        self.ipEntree.move(10, 30)
        self.submitButton.move(10, 70)
        self.exitButton.move(120, 70)
        self.responseLabel.move(10, 100)

        self.submitButton.clicked.connect(self.request)
        self.exitButton.clicked.connect(self.echap)

        self.show()

    def request(self):
        IP = self.ipEntree.text()
        if len(IP) < 7 :
            return
        response = requests.get(f"http://localhost:8000/ip/{IP}")

        self.responseLabel.insertPlainText(dumps(response.json()))

    def echap(self):
        exit()



def main():
    app = QApplication(sys.argv)
    mainWindow = Window()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

 