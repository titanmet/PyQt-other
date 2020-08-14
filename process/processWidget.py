from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
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

        self.p = QProcess()
        self.p.setProcessChannelMode(QProcess.MergedChannels)
        self.p.finished.connect(self.finish)
        self.p.readyRead.connect(self.readOut)

    def start(self):
        self.p.start(worker)
        self.start_btn.setEnabled(0)

    def readOut(self):
        out = str(self.p.readAll()).strip()
        self.showMessage(str(out.split("\'")[1]).split('\\r')[0].split('\\n')[0])
        proc = int(out.split(':')[-1].strip().split('\\r')[0])
        self.process.setValue(proc)

    def finish(self):
        self.start_btn.setEnabled(1)
        self.showMessage('COMPLETE')
        # self.p.deleteLater()

    def showMessage(self, msg):
        self.out.append(msg)


if __name__ == '__main__':
    app = QApplication([])
    window = worckerClass()
    window.show()
    app.exec_()
