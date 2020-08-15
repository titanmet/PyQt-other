from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from widget import client_UI as ui
import util


class clientWindow(QWidget, ui.Ui_client):
    def __init__(self):
        super(clientWindow, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.lineEdit.setText(util.IP)


if __name__ == '__main__':
    app = QApplication([])
    window = clientWindow()
    window.show()
    app.exec_()
