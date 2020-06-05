from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import comics as c
class Page(QMainWindow):
    def __init__(self, nom):
        super().__init__()
        self.size = self.width()*0.7
        self.livre = c.COMICParser(nom)
        self.pos = 0


        self.app()
    def app(self):
        self.pageLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.stackedLayout = QStackedLayout()
        self.sw = QVBoxLayout()
        self.liste = self.livre.read_book()
        a = 0
        for i in self.liste :
            btn = QPushButton(str(a))
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
        self.previous.setStyleSheet("font-size:50px; color : green;padding-bottom:15px;")
        self.previous.setEnabled(False)



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
        self.next.setStyleSheet("font-size:50px; color : green;padding-bottom:15px;")
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
        scroll = QScrollArea()
        w = QWidget()
        w.setLayout(self.stackedLayout)
        scroll.setWidget(w)
        scroll.setAlignment(Qt.AlignHCenter)
        qh2.addWidget(scroll)
        self.pageLayout.addLayout(self.buttonLayout)




    def changerPageAvecBtn(self):
        self.stackedLayout.setCurrentIndex(int(self.sender().text()))
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

    def zoom(self):
        try :
            texte = self.sender().text()
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
        except :
            ...
