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
        self.book = 0
        for i in T :
            for j in i :
            	if j == self.filename :
                    self.book = T.index(i)
        n = 0
        for i in T[self.book]:
        	if n==8:
        		self.pos = int(i)
        	n+=1
        #self.pos = int(T[self.book][7])
        self.pos_dep = self.pos
        self.pos_av = self.pos

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
        self.btn_page_no_visit_and_no_bookmark = "color:black; background-color:white; border-radius:5px; padding:10px;border:0.5px solid grey"
        self.btn_bookmark = "background-color : black;color:white;border-radius:5px; padding:10px;border:1px solid black"
        self.btn_visit = "background-color:red;color:white; padding:10px;border-radius:5px;"
        self.btn_bookmark_visit = "background-color : black;color:white;border-radius:5px; padding:10px;border:1px solid red"
        for i in self.liste :
            btn = QPushButton(str(a))
            btn.setStyleSheet(self.btn_page_no_visit_and_no_bookmark)
            self.btn.append(btn)
            if a == self.pos:
                self.btn[a].setStyleSheet(self.btn_bookmark)
            btn.setMaximumWidth(40)
            btn.clicked.connect(self.changerPageAvecBtn)
            self.sw.addWidget(btn)
            a+=1
            self.label = QLabel()
            self.pixmap= QPixmap(self.livre.name + "/" + i)
            self.scaledPixmap= self.pixmap.scaledToWidth(self.size)
            self.label.setPixmap(self.scaledPixmap)
            self.stackedLayout.addWidget(self.label)


        self.widget = QWidget(objectName="page")
        self.widget.setLayout(self.pageLayout)
        self.setCentralWidget(self.widget)


        self.previous = QPushButton('←', objectName='previous')
        self.previous.clicked.connect(self.changerPage)
        self.buttonLayout.addWidget(self.previous)
        self.previous.setMaximumWidth(50)
        self.previous.setMinimumWidth(50)
        self.previous.setMaximumHeight(50)
        self.previous.setMinimumHeight(50)
        self.previous.setShortcut(QKeySequence("Left"))



        self.spin = QSpinBox()
        self.spin.setMaximum(len(self.liste)-1)
        self.spin.setMinimum(0)
        self.spin.setMinimumWidth(1000)
        self.spin.valueChanged.connect(self.changerPage)
        self.buttonLayout.addWidget(self.spin)

        self.next = QPushButton('→', objectName='next')
        self.next.clicked.connect(self.changerPage)
        self.buttonLayout.addWidget(self.next)
        self.next.setMaximumWidth(50)
        self.next.setMinimumWidth(50)
        self.next.setMaximumHeight(50)
        self.next.setMinimumHeight(50)
        self.next.setEnabled(True)
        self.next.setShortcut(QKeySequence("Right"))

        self.buttonLayout.setAlignment(Qt.AlignCenter)
        self.qh = QHBoxLayout()
        self.plus = QPushButton('+', objectName='plus')
        self.plus.clicked.connect(self.zoom)
        self.plus.setMaximumHeight(30)
        self.plus.setMinimumHeight(30)
        self.plus.setMaximumWidth(420)
        self.plus.setMinimumWidth(420)


        self.plus.setEnabled(True)

        self.moins = QPushButton('-', objectName='moins')
        self.moins.clicked.connect(self.zoom)
        self.moins.setMaximumHeight(30)
        self.moins.setMinimumHeight(30)
        self.moins.setMaximumWidth(420)
        self.moins.setMinimumWidth(420)
        self.qh.addWidget(self.moins)
        self.qh.addWidget(self.plus)

        self.moins.setEnabled(True)

        self.signet = QPushButton('', objectName="signet")
        self.signet.clicked.connect(self.addBookmark)
        self.buttonLayout.addWidget(self.previous)
        self.qh.addWidget(self.signet)
        self.icon = QPixmap("signet.png")
        self.icon_hover = QPixmap("signet_hover.png")
        self.signet.setIcon(QIcon(self.icon))

        self.signet.setIconSize(self.icon.size()*0.03)
        self.signet.setMaximumHeight(30)
        self.signet.setMinimumHeight(30)
        self.signet.setMaximumWidth(420)
        self.signet.setMinimumWidth(420)

        self.plus.setShortcut(QKeySequence("ctrl++"))
        self.moins.setShortcut(QKeySequence("ctrl+-"))


        self.pageLayout.addLayout(self.qh)
        self.pageLayout.addWidget(QLabel("<center><font style='background-color:white;font-weight:bold;font-size:15px;'>Utilisez les flêches directionnelles pour contrôler la liseuse !</font></center>"))
        scsw = QScrollArea(objectName="scsw")
        w = QWidget()
        w.setLayout(self.sw)
        w.setStyleSheet('background-color:transparent;')
        scsw.setWidget(w)
        scsw.setMaximumWidth(80)
        qh2 = QHBoxLayout()
        qh2.addWidget(scsw)
        wid = QWidget()
        wid.setLayout(qh2)
        self.pageLayout.addWidget(wid)
        self.scroll = QScrollArea(objectName='scroll')
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
            self.btn[self.pos_dep].setStyleSheet(self.btn_page_no_visit_and_no_bookmark)
            self.btn[self.bookmark_temp].setStyleSheet(self.btn_bookmark)
            biblio = file.write(str(self.T[i][0]) + "$" + str(self.T[i][1]) + "$" + str(self.T[i][2]) + "$" + str(self.T[i][3]) + "$" + str(self.T[i][4]) + "$" + str(self.T[i][5]) + "$" + str(self.T[i][6]) + "$" + str(self.T[i][7]) + "$" + str(self.T[i][8]) + "\n")
        file.close()
        self.pos_dep = self.bookmark_temp


    def changerPageAvecBtn(self):
        self.pos = int(self.sender().text())
        self.stackedLayout.setCurrentIndex(self.pos)
        self.chang()
    def chang(self):
        for i in self.btn :
            i.setStyleSheet(self.btn_page_no_visit_and_no_bookmark)
            self.btn[self.pos].setStyleSheet(self.btn_visit)
        if self.pos_dep != self.pos :
            self.btn[self.pos_dep].setStyleSheet(self.btn_bookmark)
        else :
            self.btn[self.pos_dep].setStyleSheet(self.btn_bookmark_visit)

    @pyqtSlot()
    def changerPage(self):
        texte = self.sender().text()
        if texte == '→':
            if self.pos == len(self.liste)-1:
                self.previous.setEnabled(True)
                self.next.setEnabled(False)
            else:
                self.previous.setEnabled(True)
                self.next.setEnabled(True)
                self.pos+=1
            self.spin.setValue(self.spin.value()+1)
        elif texte == '←' :
            if self.pos ==0:
                self.next.setEnabled(True)
                self.previous.setEnabled(False)
            else :
                self.previous.setEnabled(True)
                self.next.setEnabled(True)
                self.pos-=1
            self.spin.setValue(self.spin.value()-1)
        self.pos = self.spin.value()
        self.stackedLayout.setCurrentIndex(self.pos)

        self.chang()


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
