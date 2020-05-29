#APPLICATION MINIMALE
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import comics as c
class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Liseuse')
        self.filename = ""
        self.BDtabs = []

        self.toolbar = QToolBar("Bar d'outils")
        self.addToolBar(self.toolbar)

        self.ouvrir = QAction("Ouvrir", self)
        self.ouvrir.triggered.connect(self.charger)
        self.ouvrir.setStatusTip("Pour ouvrir un fichier")

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

        self.bibliotheque()

    def afficher_onglets(self):
        self.tabs=QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setTabsClosable(True)

        for i in self.BDtabs:
            self.tabs.addTab(page(i),i)
            self.setCentralWidget(self.tabs)

    def bibliotheque(self):
        file = open("biblio.txt", 'r')
        biblio = file.read()
        T = [[]]
        a = ''
        lv = 0
        for i in biblio :
            a+= i
            if i =='$':
                a = a[0:-1]
                T[lv].append(a)
                a = ''
            if i == "\n":
                a = a[0:-1]
                T[lv].append(a)
                a = ''
                T.append([])
                lv+=1
        info = QVBoxLayout()
        h = QHBoxLayout()
        i = 0
        txt = ''
        while i< 3:
            i+=1
            txt = txt + '\n' + T[0][i]


        self.label = QLabel()
        self.pixmap= QPixmap("./"+str(T[0][1])+ "/" + T[0][0])
        self.scaledPixmap= self.pixmap.scaledToWidth(self.width() * 0.1)
        self.label.setPixmap(self.scaledPixmap)
        info = QLabel(txt)
        h.addWidget(self.label)
        h.addWidget(info)
        widget = QWidget()
        widget.setLayout(h)
        self.setCentralWidget(widget)




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
        self.size = 0.7
        self.livre = c.COMICParser(nom)
        self.pos = 0


        self.app()
    def app(self):
        self.pageLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.stackedLayout = QStackedLayout()
        self.pageLayout.addLayout(self.stackedLayout)
        self.pageLayout.addLayout(self.buttonLayout) #ajout d'une première sous disposition à pageLayout
        self.liste = self.livre.read_book()
        for i in self.liste :
            self.label = QLabel()
            self.pixmap= QPixmap("./"+self.livre.name + "/" + i)
            self.scaledPixmap= self.pixmap.scaledToWidth(self.width() * self.size)
            self.label.setPixmap(self.scaledPixmap)

            self.stackedLayout.addWidget(self.label)

        self.widget = QWidget()
        self.widget.setLayout(self.pageLayout)
        self.setCentralWidget(self.widget)

        self.previous = QPushButton('Previous')
        self.previous.clicked.connect(self.changerPage)
        self.buttonLayout.addWidget(self.previous)
        self.previous.setEnabled(False)


        self.next = QPushButton('Next')
        self.next.clicked.connect(self.changerPage)
        self.buttonLayout.addWidget(self.next)
        self.next.setEnabled(True)

        self.plus = QPushButton('+')
        self.plus.clicked.connect(self.zoom)
        self.buttonLayout.addWidget(self.plus)
        self.plus.setEnabled(True)

        self.moins = QPushButton('-')
        self.moins.clicked.connect(self.zoom)
        self.buttonLayout.addWidget(self.moins)
        self.moins.setEnabled(True)


    @pyqtSlot()
    def changerPage(self):
        texte = self.sender().text()
        if texte == 'Next':
            if self.pos == len(self.liste)-1:
                self.previous.setEnabled(True)
                self.next.setEnabled(False)
            else:
                self.previous.setEnabled(True)
                self.next.setEnabled(True)
                self.pos+=1
        else :
            if self.pos ==0:
                self.next.setEnabled(True)
                self.previous.setEnabled(False)
            else :
                self.previous.setEnabled(True)
                self.next.setEnabled(True)

                self.pos-=1
        self.stackedLayout.setCurrentIndex(self.pos)
    def zoom(self):
        texte = self.sender().text()
        if texte == '+':
            if self.size == 0.9:
                self.moins.setEnabled(True)
                self.plus.setEnabled(False)
            else:
                self.moins.setEnabled(False)
                self.plus.setEnabled(True)
                self.size+=0.125
        else :
            if self.size ==0:
                self.plus.setEnabled(True)
                self.moins.setEnabled(False)
            else :
                self.moins.setEnabled(True)
                self.size-=0.125
        self.app()


app = QCoreApplication.instance()
if app == None:
    app = QApplication([''])

window = FenetrePrincipale()
window.show()

app.exec()
