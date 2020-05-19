#APPLICATION MINIMALE
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import comics as c
class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Première Fenêtre')

        self.pageLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.stackedLayout = QStackedLayout()

        self.livre = c.COMICParser("spidersurf.cbz")
        self.liste = self.livre.read_book()

        for i in self.liste :
            self.label = QLabel()
            self.pixmap= QPixmap("./"+self.livre.name + "/" + i)
            self.scaledPixmap= self.pixmap.scaledToWidth(self.width() * 0.5)  # Pour prendre 80 % de la largeur
            self.label.setPixmap(self.scaledPixmap)
            self.stackedLayout.addWidget(self.label)

        self.pageLayout.addLayout(self.stackedLayout)
        self.pageLayout.addLayout(self.buttonLayout) #ajout d'une première sous disposition à pageLayout

        self.widgetCentral = QWidget()
        self.widgetCentral.setLayout(self.pageLayout)
        self.setCentralWidget(self.widgetCentral)

        #Remplissage des sous-dispositions
        self.previousnext = ['Previous', 'Next']
        self.pos = 0
        for pn in self.previousnext:
            btn = QPushButton(pn)
            btn.clicked.connect(self.changerPage)
            self.buttonLayout.addWidget(btn)

    @pyqtSlot()
    def changerPage(self):
        texte = self.sender().text()
        if texte == 'Next':
            if self.pos ==3: self.pos = 0
            else:   self.pos+=1
        else :
            if self.pos == 0: self.pos = 3
            else :  self.pos-=1
        self.stackedLayout.setCurrentIndex(self.pos)


#ces trois lignes c'est pour que ça fonctionne avec spyder
app = QCoreApplication.instance()
if app == None:
    app = QApplication([''])

window = FenetrePrincipale()
window.show()

app.exec()
