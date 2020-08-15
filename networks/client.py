from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *
from widget import client_UI as ui
import util


class clientWindow(QWidget, ui.Ui_client):
    def __init__(self):
        super(clientWindow, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.lineEdit.setText(util.IP)
        self.pushButton.clicked.connect(self.connectToServer)
        self.horizontalSlider.sliderReleased.connect(self.messageToServer)

    def connectToServer(self):
        ip = self.lineEdit.text()
        self.server = QTcpSocket()
        self.server.connectToHost(ip, util.PORT)

    def messageToServer(self):
        msg = str(self.horizontalSlider.value())
        if not self.server:
            return
        self.request = QByteArray()
        stream = QDataStream(self.request, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_2)
        stream.writeUInt32(0)
        stream << msg
        stream.device().seek(0)
        stream.writeUInt32(self.request.size() - util.UINT32)
        self.server.write(self.request)
        self.nextBlockSize = 0

    def serverError(self):
        self.server.close()
        self.pushButton.setEnabled(1)
        self.lineEdit.setEnabled(1)


if __name__ == '__main__':
    app = QApplication([])
    window = clientWindow()
    window.show()
    app.exec_()
