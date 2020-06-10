from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import comics as c
class Page(QMainWindow):
    def __init__(self, nom):
        super().__init__()
        self.filename = nom
        self.size = self.width()*0.7
        self.livre = c.COMICParser(nom)
        self.T = self.lire_bibliotheque()
        T = self.T
        for i in T :
            for j in i :
                if j == self.filename :
                    self.book = T.index(i)
                    break
        self.pos = int(T[self.book][8])
        self.pos_dep = self.pos

        self.app()
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
    def app(self):
        self.pageLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.stackedLayout = QStackedLayout()
        self.sw = QVBoxLayout()
        self.liste = self.livre.read_book()
        a = 0
        self.btn = []
        for i in self.liste :
            btn = QPushButton(str(a))
            self.btn.append(btn)
            if a == int(self.T[self.book][8]):
                self.btn[a].setStyleSheet("background-color : black;color:white")
            btn.setMaximumWidth(40)
            btn.clicked.connect(self.changerPageAvecBtn)
            self.sw.addWidget(btn)
            a+=1
            self.label = QLabel()
            self.pixmap= QPixmap(self.livre.name + "/" + i)
            self.scaledPixmap= self.pixmap.scaledToWidth(self.size)
            self.label.setPixmap(self.scaledPixmap)
            self.stackedLayout.addWidget(self.label)


        self.widget = QWidget()
        self.widget.setLayout(self.pageLayout)
        self.setCentralWidget(self.widget)


        self.previous = QPushButton('←')
        self.previous.clicked.connect(self.changerPage)
        self.buttonLayout.addWidget(self.previous)
        self.previous.setMaximumWidth(50)
        self.previous.setMinimumWidth(50)
        self.previous.setMaximumHeight(50)
        self.previous.setMinimumHeight(50)



        self.spin = QSpinBox()
        self.spin.setMaximum(len(self.liste)-1)
        self.spin.setMinimum(0)
        self.spin.valueChanged.connect(self.changerPage)
        self.buttonLayout.addWidget(self.spin)

        self.next = QPushButton('→')
        self.next.clicked.connect(self.changerPage)
        self.buttonLayout.addWidget(self.next)
        self.next.setMaximumWidth(50)
        self.next.setMinimumWidth(50)
        self.next.setMaximumHeight(50)
        self.next.setMinimumHeight(50)
        self.next.setEnabled(True)

        self.qh = QHBoxLayout()
        self.plus = QPushButton('+')
        self.plus.clicked.connect(self.zoom)
        self.plus.setMaximumHeight(20)
        self.plus.setMinimumHeight(20)

        self.plus.setStyleSheet("color:blue;font-size:15px;")

        self.plus.setEnabled(True)

        self.moins = QPushButton('-')
        self.moins.clicked.connect(self.zoom)
        self.moins.setStyleSheet("color:red;font-size:15px;")
        self.moins.setMaximumHeight(20)
        self.moins.setMinimumHeight(20)
        self.qh.addWidget(self.moins)
        self.qh.addWidget(self.plus)

        self.moins.setEnabled(True)

        self.signet = QPushButton('ajouter un signet')
        self.signet.clicked.connect(self.addBookmark)
        self.buttonLayout.addWidget(self.previous)
        self.qh.addWidget(self.signet)

        self.pageLayout.addLayout(self.qh)
        scsw = QScrollArea()
        w = QWidget()
        w.setLayout(self.sw)
        scsw.setWidget(w)
        scsw.setMaximumWidth(80)
        qh2 = QHBoxLayout()
        qh2.addWidget(scsw)
        wid = QWidget()
        wid.setLayout(qh2)
        self.pageLayout.addWidget(wid)
        self.scroll = QScrollArea()
        self.scroll.setBackgroundRole(QPalette.Dark)
        w = QWidget()
        w.setLayout(self.stackedLayout)
        self.scroll.setWidget(w)
        self.scroll.setAlignment(Qt.AlignHCenter)
        qh2.addWidget(self.scroll)
        self.pageLayout.addLayout(self.buttonLayout)
        self.stackedLayout.setCurrentIndex(self.pos)
        self.spin.setValue(self.pos)



    def addBookmark(self):
        T = self.T
        book = self.book
        self.source_temp = T[book][1]
        self.title_temp = T[book][2]
        self.author_temp = T[book][3]
        self.creation_time_temp = T[book][4]
        self.year_temp = T[book][5]
        self.tags_temp = []
        self.quality_temp = T[book][7]
        self.bookmark_temp = T[book][8]
        self.bookmark_temp = self.pos
        T_book = [self.T[self.book][0], self.source_temp, self.title_temp, self.author_temp, self.creation_time_temp, self.year_temp, str(self.tags_temp), self.quality_temp, self.bookmark_temp]
        self.T[self.book] = T_book
        file = open("biblio.txt", "w")
        for i in range(len(self.T)-1):
            self.btn[self.pos_dep].setStyleSheet("background-color:white;color:black")
            self.btn[self.bookmark_temp].setStyleSheet("background-color:black;color:white")
            biblio = file.write(str(self.T[i][0]) + "$" + str(self.T[i][1]) + "$" + str(self.T[i][2]) + "$" + str(self.T[i][3]) + "$" + str(self.T[i][4]) + "$" + str(self.T[i][5]) + "$" + str(self.T[i][6]) + "$" + str(self.T[i][7]) + "$" + str(self.T[i][8]) + "\n")
        file.close()


    def changerPageAvecBtn(self):
        self.stackedLayout.setCurrentIndex(int(self.sender().text()))
        self.pos = int(self.sender().text())

    @pyqtSlot()
    def changerPage(self):
        texte = self.sender().text()
        if texte == '→':
            if self.pos == len(self.liste)-1:
                self.previous.setEnabled(True)
                self.previous.setStyleSheet("color:white; background-color:green;")
                self.next.setStyleSheet("color:white; background-color:white;")
                self.next.setEnabled(False)
                pass

            else:
                self.previous.setEnabled(True)
                self.next.setEnabled(True)
                self.previous.setStyleSheet("color:white; background-color:green;")
                self.next.setStyleSheet("color:white; background-color:green;")

                self.pos+=1
            self.spin.setValue(self.spin.value()+1)
        elif texte == '←' :
            if self.pos ==0:
                self.next.setEnabled(True)
                self.next.setStyleSheet("color:white; background-color:green;")
                self.previous.setStyleSheet("color:white; background-color:white;")
                self.previous.setEnabled(False)
                pass
            else :
                self.previous.setEnabled(True)
                self.next.setEnabled(True)
                self.previous.setStyleSheet("color:white; background-color:green;")
                self.next.setStyleSheet("color:white; background-color:green;")
                self.pos-=1
            self.spin.setValue(self.spin.value()-1)
        self.pos = self.spin.value()
        self.stackedLayout.setCurrentIndex(self.pos)

    def zoom(self):

        try :
            texte = self.sender().text()
            a = self.pos
            if texte == '+':
                if self.size == 0.9:
                    self.moins.setEnabled(True)
                    self.plus.setEnabled(False)
                else:
                    self.moins.setEnabled(False)
                    self.plus.setEnabled(True)
                    self.size+=10
            else :
                if self.size ==0:
                    self.plus.setEnabled(True)
                    self.moins.setEnabled(False)
                else :
                    self.moins.setEnabled(True)
                    self.size-=10
            self.app()
            self.stackedLayout.setCurrentIndex(a)
            self.pos = a
        except :
            ...
if __name__ == '__main__':
    book = Page('spidersurf.cbz')
