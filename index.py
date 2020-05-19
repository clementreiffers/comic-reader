#APPLICATION MINIMALE
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import comics as c
class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Première Fenêtre')
        self.setMinimumSize(500,500)
        self.setMaximumSize(1700,1000)
        self.filename = ""
        self.BDtabs = []
        self.tabs=QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(True)


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

    def afficher_onglets(self):
        self.tabs=QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabPosition(QTabWidget.East)
        self.tabs.setMovable(True)
        #self.colors=['red','green','blue','yellow']
        print(self.BDtabs)
        for i in self.BDtabs:
            # On ajoute le widget directement
            # AVEC son élément de tableau
            self.tabs.addTab(page(i),i)
            self.setCentralWidget(self.tabs)
            app =QCoreApplication.instance()
            if app is None:
                app =QApplication(sys.argv)
                window=Fenetre()
                window.show()
                app.exec_()

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
        self.BDtabs.append(self.filename)
        self.afficher_onglets()

class page(QMainWindow):
    def __init__(self, nom):
        super().__init__()
        self.pageLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.stackedLayout = QStackedLayout()
        self.pageLayout.addLayout(self.stackedLayout)
        self.pageLayout.addLayout(self.buttonLayout) #ajout d'une première sous disposition à pageLayout
        self.livre = c.COMICParser(nom)
        print(nom)
        self.liste = self.livre.read_book()
        for i in self.liste :
            self.label = QLabel()
            self.pixmap= QPixmap("./"+self.livre.name + "/" + i)

            self.scaledPixmap= self.pixmap.scaledToWidth(self.width() * 0.5)  # Pour prendre 80 % de la largeur
            self.label.setPixmap(self.scaledPixmap)

            self.stackedLayout.addWidget(self.label)

        self.widget = QWidget()
        self.widget.setLayout(self.pageLayout)
        self.setCentralWidget(self.widget)
        #Remplissage des sous-dispositions
        self.pos = 0

        self.previous = QPushButton('Previous')
        self.previous.clicked.connect(self.changerPage)
        self.buttonLayout.addWidget(self.previous)

        self.next = QPushButton('Next')
        self.next.clicked.connect(self.changerPage)
        self.buttonLayout.addWidget(self.next)

    @pyqtSlot()
    def changerPage(self):
        texte = self.sender().text()
        if texte == 'Next':
            if self.pos == len(self.liste):
                self.next.setEnabled(False)
            else:
                self.next.setEnabled(True)

                self.pos+=1
        else :
            if self.pos ==0:
                self.previous.setEnabled(False)
            else :
                self.previous.setEnabled(True)

                self.pos-=1

        self.stackedLayout.setCurrentIndex(self.pos)


#ces trois lignes c'est pour que ça fonctionne avec spyder
app = QCoreApplication.instance()
if app == None:
    app = QApplication([''])

window = FenetrePrincipale()
window.show()

app.exec()
