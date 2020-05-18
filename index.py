
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QPainter, QPen, QImage
from PyQt5.QtCore import Qt,QPoint

class Dessin(QWidget):
    #evenement QPaintEvent
    def paintEvent(self, event): # event de type QPaintEvent
        painter = QPainter(self) # recupere le QPainter du widget
        point = QPoint(10,10)
        image = QImage("inductance.gif");
        painter.drawImage(point, image);

        return

def main(args):
    app = QApplication(args)
    win = QMainWindow()
    win.setCentralWidget(Dessin())
    win.resize(300,200)
    win.show()
    app.exec_()
    return

if __name__ == "__main__":
    main(sys.argv)

