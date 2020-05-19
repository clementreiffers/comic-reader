#APPLICATION MINIMALE
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import comics as c
class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Première Fenêtre')
        self.filename = ""

        self.pageLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.stackedLayout = QStackedLayout()

        self.toolbar = QToolBar("Bar d'outils")
        self.addToolBar(self.toolbar)

        self.ouvrir = QAction("Ouvrir", self)
        self.ouvrir.triggered.connect(self.charger)
        self.ouvrir.setStatusTip("Pour ouvrir un fichier")
        #self.ouvrir.setIcon(QIcon("editer.png"))

        self.barreDeMenu = self.menuBar()
        self.menuFichier = self.barreDeMenu.addMenu("&Fichier")
        self.menuFichier.addAction(self.ouvrir)
        self.menuFichier.addSeparator()

        self.menuEdition = self.barreDeMenu.addMenu("&Edition")
        self.menuEdition.addSeparator()

        self.menuAffichage = self.barreDeMenu.addMenu("&Affichage")
        self.menuAffichage.addSeparator()

        self.menuLire = self.barreDeMenu.addMenu("&Lire")
        self.menuLire.addSeparator()

        self.menuAide = self.barreDeMenu.addMenu("&Aide")
        self.menuAide.addSeparator()


        self.ouvrir.setShortcut(QKeySequence("ctrl+o"))
        #self.ouvrir.setShortcut(QKeySequence("ctrl+o"))
        self.app()
    def app(self):
        if self.filename != "" :

            self.livre = c.COMICParser(self.filename)
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

    def charger(self):
        dialogue = QFileDialog()
        self.filename = dialogue.getOpenFileName(self,
                                                    'Ouvrir fichier',

                                                    filter='Comic Book Zip (*.cbz);;Comic Book Rar (*.cbr)')[0]
        nom = ""
        for i in self.filename[::-1]:
            if i == "/" : break
            nom += i
        self.filename = nom[::-1]

        self.app()
        """
        if self.filename == ('',''):
            print('Nom de fichier vide.')
            return

        fichier = QFile(self.filename)
        ok = fichier.open(QFile.ReadOnly)

        if ok:
            print('Le fichier de sauvegarde à été chargé.')
            flux = QTextStream(fichier)
            texte = flux.readAll()
            self.textEdit.setText(texte)
            fichier.close()
        else:
            print('Le fichier de sauvegarde n\'a pas pu être chargé.')
        """


#ces trois lignes c'est pour que ça fonctionne avec spyder
app = QCoreApplication.instance()
if app == None:
    app = QApplication([''])

window = FenetrePrincipale()
window.show()

app.exec()
