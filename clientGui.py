
from PyQt5 import QtCore, QtGui, QtWidgets

import time
import socket
import json
import sys
import threading


"""
class uiTxtEdtGunclThread(QtCore.QThread):
    def __init__(self,uiwin):
        super().__init__(parent=QtCore.QThread())
        self.uiwin =uiwin

    def run(self):
        while True:
            self.uiwin.textEdit.setText(self.uiwin.mesajlar)
            time.sleep(0.1)
"""




class Ui_MainWindow(object):
    degDeger = QtCore.pyqtSignal(str)

    def __init__(self):
        self.istemci = Istemci()
        self.mesajlar = ""

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(780, 498)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.gridLayout.setObjectName("gridLayout")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.gonderClick)
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 2)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 780, 22))
        self.menubar.setObjectName("menubar")

        self.menuMen = QtWidgets.QMenu(self.menubar)
        self.menuMen.setObjectName("menuMen")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionBa_lan = QtWidgets.QAction(MainWindow)
        self.actionBa_lan.setObjectName("actionBa_lan")

        self.action_k = QtWidgets.QAction(MainWindow)
        self.action_k.setObjectName("action_k")

        self.actionTema = QtWidgets.QAction(MainWindow)
        self.actionTema.setObjectName("actionTema")

        self.menuMen.addAction(self.actionBa_lan)
        self.menuMen.addAction(self.actionTema)
        self.menuMen.addAction(self.action_k)

        self.menubar.addAction(self.menuMen.menuAction())
        self.menubar.triggered.connect(self.menuClick)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    """
    def txtEdtgun_Olay(self,dgr):
        self.textEdit.
    """

    @QtCore.pyqtSlot(str)
    def txtEdtGun(self,degr):
        self.textEdit.setText(degr)

    def gelenMesajKnt(self):


        while True:
            glnmsj = self.istemci.mesajAl()
            if glnmsj == "boss":
                pass
            else:
                if self.mesajlar == (self.mesajlar + glnmsj+"\n"):
                    pass
                else:
                    self.mesajlar += glnmsj+"\n"


            time.sleep(0.1)


    def gonderClick(self):


        if self.lineEdit.text() == "":
            pass
        else:
            self.istemci.mesajGonder(self.lineEdit.text())
            self.mesajlar += self.lineEdit.text()+"\n"
            self.textEdit.setText(self.mesajlar)

            self.lineEdit.clear()

        print("mesajlar"+ self.mesajlar)



    def baglantiClick(self):
        host = self.uiB.lineEdit.text()
        port = self.uiB.lineEdit_2.text()

        print("host : " + host)
        print("port : " + port)

        self.istemci.baslat(host, int(port))

        glnmsjknt = threading.Thread(target=self.gelenMesajKnt,)
        glnmsjknt.start()










    def menuClick(self,action):
        if action.text()=="&Bağlan":
            Form = QtWidgets.QDialog()
            self.uiB = Baglan_Ui()
            self.uiB.setupUi(Form)
            self.uiB.pushButton.clicked.connect(self.baglantiClick)
            Form.exec_()

        elif action.text() == "&Çıkış":
            Dilog = QtWidgets.QDialog()
            uyari = UyariDialog()
            uyari.setupUi(Dilog)
            uyari.label.setText("Bağlantıyı kesmek istediğinize emin misiniz ??")

            if Dilog.exec_():
                self.istemci.durdur()
            else:
                pass





    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Gönder"))
        self.menuMen.setTitle(_translate("MainWindow", "Me&nü"))
        self.actionBa_lan.setText(_translate("MainWindow", "&Bağlan"))
        self.action_k.setText(_translate("MainWindow", "&Çıkış"))
        self.actionTema.setText(_translate("MainWindow", "&Tema"))

class Istemci():

    def __init__(self):
        global mesajj
        mesajj= "boss"



    def baslat(self,h,p):

        self.host = h
        self.port = p
        self.tampon = 1024

        self.sock = socket.socket()
        self.sock.connect((h, p))


        glnmes =  threading.Thread(target=self.gelenMessaj,)
        glnmes.start()


    def durdur(self):
        self.sock.close()


    def gelenMessaj(self):
        global mesajj
        while True:
            data =  self.sock.recv(self.tampon)

            if data =="":
                pass
            elif data == bytes():
                mesajj="Server Baglantı koptu"
                break
            else:
                mesajj=bytes.decode(data,"utf-8") + "  TT"


            time.sleep(0.02)


    def mesajGonder(self,messaj):
        mess = bytes(messaj,"utf-8")
        self.sock.send(mess)
        print("mesaj gonderildi")

    def mesajAl(self):
        return mesajj



class Baglan_Ui(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(630, 138)
        Form.setMinimumSize(QtCore.QSize(630, 138))
        Form.setMaximumSize(QtCore.QSize(1920, 1080))
        Form.setWindowOpacity(1.0)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")

        self.gridLayout.addWidget(self.pushButton, 4, 1, 1, 1)

        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setText("4446")
        self.gridLayout.addWidget(self.lineEdit_2, 2, 1, 1, 1)

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText("127.0.0.1")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "BAĞLAN"))
        self.label_2.setText(_translate("Form", "İP :"))
        self.label.setText(_translate("Form", "PORT :"))
        self.pushButton.setText(_translate("Form", "Bağlan"))
        self.label_3.setText(_translate("Form", "Durum :"))

    def uiclose(self):
        QtWidgets.QDialog.close(self)



class UyariDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 303)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "TextLabel"))




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

