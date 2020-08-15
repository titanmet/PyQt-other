from functools import partial

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *
from widget import server_UI as ui
import util


class serverWindow(QWidget, ui.Ui_Server):
    def __init__(self):
        super(serverWindow, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.lineEdit.setText(util.IP)
        self.tcpServer = QTcpServer()
        self.tcpServer.listen(QHostAddress(QHostAddress.Any), util.PORT)
        self.tcpServer.newConnection.connect(self.createConnection)

    def createConnection(self):
        connection = self.tcpServer.nextPendingConnection()
        connection.nextBlockSize = 0
        connection.readyRead.connect(partial(self.receiveMessage, connection))
        connection.error.connect(self.socketError)
        adr = str(connection.peerAddress().toString())
        self.consoleMessage('Connected to: ' + adr)

    def consoleMessage(self, text):
        self.textBrowser.append(text)

    def receiveMessage(self, socket):
        if socket.bytesAvailable() > 0:
            stream = QDataStream(socket)
            stream.setVersion(QDataStream.Qt_4_2)
            if socket.nextBlockSize == 0:
                if socket.bytesAvailable() < util.UINT32:
                    return
                socket.nextBlockSize = stream.readUInt32()
            if socket.bytesAvailable() < socket.nextBlockSize:
                return
            textFromClient = stream.readQString()
            socket.nextBlockSize = 0
            self.consoleMessage(textFromClient)

            if textFromClient.isdigit():
                self.setProgress(textFromClient)
            else:
                self.consoleMessage(textFromClient)

    def setProgress(self, val):
        self.progressBar.setValue(int(val))

    def socketError(self):
        self.consoleMessage('socket ERROR')


if __name__ == '__main__':
    app = QApplication([])
    window = serverWindow()
    window.show()
    app.exec_()
