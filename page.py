from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import comics as c
class Page(QMainWindow):
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
            self.pixmap= QPixmap(self.livre.name + "/" + i)
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


        self.spin = QSpinBox()
        self.spin.setMaximum(len(self.liste)-1)
        self.spin.setMinimum(0)
        self.spin.valueChanged.connect(self.changerPage)
        self.buttonLayout.addWidget(self.spin)

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
            self.spin.setValue(self.spin.value()+1)
        elif texte == 'Previous' :
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
