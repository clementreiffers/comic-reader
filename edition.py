from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
class Edition(QMainWindow):
    def __init__(self):
        super().__init__()
        self.verif = False
        self.app()
    def app(self):
        self.setWindowTitle('Première Fenêtre')
