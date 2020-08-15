from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from widget import server_UI as ui
import util

class serverWindow(QWidget, ui.Ui_Server):
    def __init__(self):
        super(serverWindow, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.lineEdit.setText(util.IP)

    def consoleMessage(self, text):
        self.textBrowser.append(text)


if __name__ == '__main__':
    app = QApplication([])
    window = serverWindow()
    window.show()
    app.exec_()
