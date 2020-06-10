#APPLICATION MINIMALE
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import comics as c
import page as p
import sys
import subprocess
from PyQt5 import QtGui
import os
import shutil

class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Liseuse')
        self.setGeometry(200, 200, 1140, 500)
        self.setWindowIcon(QtGui.QIcon('spidermanicon.png'))
        self.setGeometry(200, 200, 1200, 500)



        actOpen = QAction( QIcon( "icons8-fichier-48.png" ), "&Open", self )
        actOpen.setStatusTip( "Ouvrir un fichier" )
        actOpen.triggered.connect(self.charger)



        actExit = QAction( QIcon( "icons8-porte-ouverte-40.png" ), "E&xit", self )
        actExit.setShortcut( "Ctrl+Q" )
        actExit.setStatusTip( "quitter l'application" )
        actExit.triggered.connect( self.close )


        actbiblio = QAction(QIcon( "biblio.png" ), "&Open", self)
        actbiblio.setStatusTip( "ouvrir la bibliothèque" )
        actbiblio.triggered.connect(self.addBi)

        toolbar = self.addToolBar( "Standard ToolBar" )
        toolbar.addAction( actOpen )
        toolbar.addAction(actbiblio)
        toolbar.addSeparator()
        toolbar.addAction( actExit )


        self.filename = ""
        self.BDtabs = [1]
        self.nomTabs = ["bibliothèque"]

        self.toolbar = QToolBar("Bar d'outils")
        self.addToolBar(self.toolbar)

        self.ouvrir = QAction("Ouvrir", self)
        self.ouvrir.triggered.connect(self.charger)
        self.ouvrir.setStatusTip("Pour ouvrir un fichier")
        self.ouvrir.setIcon(QIcon("icons8-fichier-48.png"))

        self.biblio = QAction("Bibliothèque", self)
        self.biblio.triggered.connect(self.addBi)
        self.biblio.setStatusTip("Pour afficher la bibliothèque")
        self.biblio.setIcon(QIcon("biblio.png"))

        self.quit = QAction("exit", self)
        self.quit.triggered.connect(self.quitter)
        self.quit.setStatusTip("Pour quitter")
        self.quit.setIcon(QIcon("icons8-porte-ouverte-40.png"))

        self.dl = QAction("Télécharger des BD", self)
        self.dl.triggered.connect(self.download)
        self.dl.setStatusTip("Pour télécharger des Ouvrages")
        self.dl.setIcon(QIcon("icons8-bande-dessinée-48.png"))

        self.close = QAction("Fermez l'onglet courant", self)
        self.close.triggered.connect(self.closeTab)
        self.close.setStatusTip("Pour télécharger des Ouvrages")
        self.close.setIcon(QIcon("icons8-annuler-48.png"))

        self.onglet = QAction("Affichez les onglets", self)
        self.onglet.triggered.connect(self.afficher_onglets)
        self.onglet.setStatusTip("Pour afficher les onglets")
        self.onglet.setIcon(QIcon("icons8-faire-défiler-48.png"))



        self.barreDeMenu = self.menuBar()
        self.menuFichier = self.barreDeMenu.addMenu("&Fichier")
        self.menuFichier.addAction(self.ouvrir)
        self.menuFichier.addAction(self.biblio)
        self.menuFichier.addAction(self.dl)
        self.menuFichier.addAction(self.close)
        self.menuFichier.addAction(self.quit)
        self.menuFichier.addSeparator()

        self.menuEdition = self.barreDeMenu.addMenu("&Edition")
        self.menuEdition.addSeparator()

        self.menuAffichage = self.barreDeMenu.addMenu("&Affichage")
        self.menuAffichage.addAction(self.onglet)
        self.menuAffichage.addSeparator()

        self.menuLire = self.barreDeMenu.addMenu("&Lire")
        self.menuLire.addSeparator()


        self.menuAide = self.barreDeMenu.addMenu("&Aide")
        self.menuAide.addSeparator()

        self.menuMusique = self.barreDeMenu.addMenu("&Musique")
        self.menuMusique.addSeparator()


        self.ouvrir.setShortcut(QKeySequence("ctrl+o"))
        self.biblio.setShortcut(QKeySequence("ctrl+b"))
        self.quit.setShortcut(QKeySequence("ctrl+f"))
        self.close.setShortcut(QKeySequence("ctrl+w"))
        self.dl.setShortcut(QKeySequence("ctrl+d"))
        self.onglet.setShortcut(QKeySequence("ctrl+n"))

        self.tabs=QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)
        self.tabs.setMovable(True)

        self.biblio = self.lire_bibliotheque()
        self.nouveaux_onglets()

    def addBi(self):
        self.BDtabs.append(1)
        self.nomTabs.append("bibliothèque")
        self.nouveaux_onglets()

    def download(self):
        try :
            try :
                #commande pour windows
                subprocess.call("explorer " + "http://www.openculture.com/2014/03/download-15000-free-golden-age-comics-from-the-digital-comic-museum.html", shell=True)
            except :
                #commande pour les systèmes debian
                subprocess.call("xdg-open " + "http://www.openculture.com/2014/03/download-15000-free-golden-age-comics-from-the-digital-comic-museum.html", shell=True)
        except :
            print("votre système n'est pas répertorié dans nos commandes")


    def quitter(self):
        exit()

    def closeTab(self):
        if len(self.nomTabs)>1:
            i = self.tabs.currentIndex()
            self.nomTabs.pop(i)
            self.BDtabs.pop(i)
            self.tabs.removeTab(i)
        else :
            self.tabs=QTabWidget()
            self.tabs.setTabPosition(QTabWidget.North)
            self.tabs.setTabsClosable(True)
            self.tabs.tabCloseRequested.connect(self.closeTab)
            self.tabs.setMovable(True)
            self.afficher_biblio()

    def nouveaux_onglets(self):
        self.tabs=QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setTabsClosable(True)
        for i in range(len(self.BDtabs)):
            if self.BDtabs[i-1] != 1 :
                self.tabs.addTab(p.Page(self.BDtabs[i-1]), self.nomTabs[i-1])
                self.setCentralWidget(self.tabs)
            else :
                self.tabs.addTab(self.afficher_biblio(), "Bibliothèque")
                self.setCentralWidget(self.tabs)

    def au_revoir(self):
        partir = QAction('&Exit',self)
        partir.setShortcut('Ctrl+Q')
        partir.setStatusTip('Exit App')
        partir.triggered.connect(self.closeEvent)
        return partir


    def closeEvent(self,event):
        reply = QMessageBox.question(self,'Attention','Êtes vous sûr de vouloir quitter la liseuse.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)

        if reply == QMessageBox.Yes :
            qApp.quit()
        else :
            try:
                event.ignore()
            except AttributeError:
                pass

    def afficher_onglets(self):
        try :
            self.tabs.addTab(p.Page(self.BDtabs[-1]), self.nomTabs[-1])
            self.setCentralWidget(self.tabs)
        except:
            self.nouveaux_onglets()


    def lire_bibliotheque(self):
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
        return T

    def afficher_biblio(self, T=None):
        self.T = self.lire_bibliotheque()
        T = self.T
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setRowCount(len(T))
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("cover"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("source"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("title"))
        self.tableWidget.setItem(0, 3 , QTableWidgetItem("author"))
        self.tableWidget.setItem(0, 4 , QTableWidgetItem("creation_time"))
        self.tableWidget.setItem(0, 5 , QTableWidgetItem("year"))
        self.tableWidget.setItem(0, 6 , QTableWidgetItem("tags"))
        self.tableWidget.setItem(0, 7 , QTableWidgetItem("quality"))
        self.tableWidget.setItem(0, 8 , QTableWidgetItem("ouvrir"))
        self.tableWidget.setItem(0, 9 , QTableWidgetItem("editer"))
        self.tableWidget.setItem(0, 10 , QTableWidgetItem("delete"))
        header = self.tableWidget.verticalHeader()
        for i in range(len(T)-1):
            self.btn = QAction("lire " + T[i][2], self)
            self.btn.triggered.connect(self.lire)
            self.btn.setStatusTip("Lire cette Ouvrage")
            self.menuLire.addAction(self.btn)

            for j in range(len(T[i])+3):
                if j == 0 :

                    info = QVBoxLayout()
                    h = QHBoxLayout()
                    n = 0
                    txt = ''
                    self.label = QLabel()
                    self.pixmap= QPixmap("./"+str(T[i][2])+ "/" + T[i][0])
                    self.scaledPixmap= self.pixmap.scaledToWidth(self.width() * 0.1)
                    self.label.setPixmap(self.scaledPixmap)
                    info = QLabel(txt)
                    h.addWidget(self.label)
                    h.addWidget(info)
                    widget = QWidget()
                    widget.setLayout(h)
                    self.tableWidget.setCellWidget(i+1, j, widget)
                    header.setSectionResizeMode(i+1, QHeaderView.Stretch)

                elif j == len(T[i])-1:
                    self.btn = QPushButton("lire\n" + str(T[i][2]))
                    self.btn.clicked.connect(self.lire)
                    self.tableWidget.setCellWidget(i+1, j, self.btn)

                elif j == len(T[i]):
                    self.btn = QPushButton("editer\n"+ str(T[i][2]))
                    self.btn.clicked.connect(self.editer)
                    self.tableWidget.setCellWidget(i+1, j, self.btn)

                elif j == len(T[i])+1:
                    self.btn = QPushButton("supprimer\n"+ str(T[i][2]))
                    self.btn.clicked.connect(self.delete)
                    self.tableWidget.setCellWidget(i+1, j, self.btn)

                elif j<len(T[i]):
                    self.tableWidget.setItem(i+1, j, QTableWidgetItem(T[i][j]))
            self.vBoxLayout = QVBoxLayout()
            self.vBoxLayout.addWidget(self.tableWidget)
            widget = QWidget()
            widget.setLayout(self.vBoxLayout)
            self.setCentralWidget(widget)
        return widget

    def editer(self):
        texte = self.sender().text()
        self.filename = texte[7:len(texte)]
        T = self.T
        for i in T :
            for j in i :
                if j == self.filename :
                    self.book = T.index(i)
                    break
        book = self.book
        self.source_temp = T[book][1]
        self.title_temp = T[book][2]
        self.author_temp = T[book][3]
        self.creation_time_temp = T[book][4]
        self.year_temp = T[book][5]
        self.tags_temp = []
        self.quality_temp = T[book][7]
        self.bookmark_temp = T[book][8]


        widget = QWidget()
        qv = QVBoxLayout()
        qv.addWidget(QLabel("titre"))
        self.titre = QLineEdit()
        self.titre.setPlaceholderText(T[book][2])
        qv.addWidget(self.titre)
        qv.addWidget(QLabel("auteur"))
        self.author = QLineEdit()
        self.author.setPlaceholderText(T[book][3])
        qv.addWidget(self.author)
        qv.addWidget(QLabel("date de création"))
        self.creation_time = QLineEdit()
        self.creation_time.setPlaceholderText(T[book][4])
        qv.addWidget(self.creation_time)
        qv.addWidget(QLabel("année"))
        self.year = QLineEdit()
        self.year.setPlaceholderText(T[book][5])
        qv.addWidget(self.year)
        qv.addWidget(QLabel("tags"))
        self.tag = QLineEdit()
        self.tag.setText(T[book][6])
        add = QPushButton("ajouter")
        add.clicked.connect(self.add_tags)
        qv.addWidget(self.tag)
        qv.addWidget(add)
        qv.addWidget(QLabel("Quality"))
        self.quality = QLineEdit()
        self.quality.setPlaceholderText(T[book][7])
        qv.addWidget(self.quality)
        qv.addWidget(QLabel("source"))
        self.source = QPushButton("source")
        self.source.clicked.connect(self.changer_source)
        qv.addWidget(self.source)
        annuler = QPushButton("annuler")
        annuler.clicked.connect(self.afficher_biblio)
        valider = QPushButton("valider")
        valider.clicked.connect(self.update)
        qh = QHBoxLayout()
        qh.addWidget(annuler)
        qh.addWidget(valider)
        w = QWidget()
        w.setLayout(qh)
        qv.addWidget(w)
        widget.setLayout(qv)
        self.setCentralWidget(widget)

    def add_tags(self):
        tag = self.tag.text()
        if ',' in tag : tag.split(",")
        self.tags_temp = tag
        self.tag.setPlaceholderText(str(self.tags_temp))

    def update(self):
        if self.titre.text() != "":
            self.title_temp = self.titre.text()
            os.rename(self.T[self.book][2], self.title_temp)

        if self.author.text() != "":self.author_temp = self.author.text()
        if self.creation_time.text() != "":self.creation_time_temp = self.creation_time.text()
        if self.year.text() != "":self.year_temp = self.year.text()
        if self.quality.text() != "":self.quality_temp = self.quality.text()

        print(str(self.T[self.book][2])+"/"+self.T[self.book][0])
        T_book = [self.T[self.book][0], self.source_temp, self.title_temp, self.author_temp, self.creation_time_temp, self.year_temp, str(self.tags_temp), self.quality_temp, self.bookmark_temp]
        self.T[self.book] = T_book

        file = open("biblio.txt", "w")
        for i in range(len(self.T)-1):

            biblio = file.write(str(self.T[i][0]) + "$" + str(self.T[i][1]) + "$" + str(self.T[i][2]) + "$" + str(self.T[i][3]) + "$" + str(self.T[i][4]) + "$" + str(self.T[i][5]) + "$" + str(self.T[i][6]) + "$" + str(self.T[i][7]) + "$" + str(self.T[i][8]) + "\n")
        file.close()
        self.afficher_biblio()

    def changer_source(self):
        dialogue = QFileDialog()
        self.source_temp = dialogue.getOpenFileName(self,'Ouvrir fichier',filter='Comic Book Zip (*.cbz);;Comic Book Rar (*.cbr)')[0]

    def delete(self):
        texte = self.sender().text()
        self.filename = texte[10:len(texte)]
        T = self.T
        for i in T :
            for j in i :
                if j == self.filename :
                    self.book = T.index(i)
                    break
        self.tableWidget.removeRow(self.book)
        self.T.pop(self.book)
        file = open("biblio.txt", "w")
        for i in range(len(self.T)-1):
            biblio = file.write(str(self.T[i][0]) + "$" + str(self.T[i][1]) + "$" + str(self.T[i][2]) + "$" + str(self.T[i][3]) + "$" + str(self.T[i][4]) + "$" + str(self.T[i][5]) + "$" + str(self.T[i][6]) + "$" + str(self.T[i][7]) + "\n")
        file.close()
        shutil.rmtree(self.filename)
        self.afficher_biblio()


    def charger(self):
        try :
            dialogue = QFileDialog()
            self.filename = dialogue.getOpenFileName(self,'Ouvrir fichier',filter='Comic Book Zip (*.cbz);;Comic Book Rar (*.cbr)')[0]
            livre = c.COMICParser(self.filename)
            livre.read_book()
            livre.generate_metadata(author='<Unknown>', isbn = None, tags=[], quality=0, src=self.filename)
            self.BDtabs.append(self.filename)
            nom = ""
            for i in self.filename[::-1]:
                if i == "/" : break
                nom += i
            nom = nom[::-1]
            self.nomTabs.append(nom)
            self.afficher_onglets()
        except:
            pass

    def lire(self):

        texte = self.sender().text()
        self.filename = texte[5:len(texte)]
        T = self.lire_bibliotheque()
        for i in T :
            for j in i :
                if j == self.filename :
                    emplacement = T[T.index(i)][1]
                    break
        livre = c.COMICParser(emplacement)
        livre.read_book()
        self.BDtabs.append(emplacement)
        nom = ""
        for i in self.filename[::-1]:
            if i == "/" : break
            nom += i
        nom = nom[::-1]
        self.nomTabs.append(nom)
        self.afficher_onglets()

def printArray(T):
    for i in T :
        print(i)


app = QCoreApplication.instance()
if app == None:
    app = QApplication([''])

window = FenetrePrincipale()
window.show()

app.exec()
