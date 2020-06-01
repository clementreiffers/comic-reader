from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
class Edition(QWidget):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        posit = QVBoxLayout()
        posit.addWidget(QLineEdit())
        posit.addWidget(QLineEdit())
        posit.addWidget(QPushButton())

        widget.setLayout(posit)


if __name__ == '__main__':

    app = QCoreApplication.instance()
    if app == None:
        app = QApplication([''])

    window = Edition()
    window.show()

    app.exec()
