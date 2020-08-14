from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os

worker = 'python ' + os.path.join(os.path.dirname(__file__), 'worker.py')


class worckerClass(QWidget):
    def __init__(self):
        super(worckerClass, self).__init__()
        self.ly = QVBoxLayout(self)

        self.start_btn = QPushButton('Start')
        self.ly.addWidget(self.start_btn)
        self.start_btn.clicked.connect(self.start)

        self.out = QTextBrowser()
        self.ly.addWidget(self.out)

        self.process = QProgressBar()
        self.ly.addWidget(self.process)
        self.process.setValue(0)

    def start(self):
        self.p = QProcess()
        self.p.finished.connect(self.finish)
        self.p.readyRead.connect(self.readOut)
        self.p.start(worker)

    def readOut(self):
        out = str(self.p.readAll()).strip()
        print(out)

    def finish(self):
        print('Finish')


if __name__ == '__main__':
    app = QApplication([])
    window = worckerClass()
    window.show()
    app.exec_()
