#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import time
import socket
import json
import sys
import threading
import datetime
import random
from Crypto.Cipher import AES
import os


class Ui_MainWindow(object):
    def __init__(self):
        self.isim = "Melih"
        self.id_kull = datetime.datetime.now().microsecond + random.randint(100000, 999999)
        self.istemci = Istemci()
        self.mesajlar = ""
        self.msjsayisi = 0
        self.key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'
        self.cipher = AES.new(self.key)
        self.kullanicilar = []
        self.glnmsjsayisi = []
        self.kullanicilar.append(self.id_kull)
        self.glnmsjsayisi.append(self.msjsayisi)

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

    def gelenMesajKntTimer(self):
        if self.istemci.mesajAl() == "boss":
            pass
        else:
            print(self.kullanicilar)
            print(self.glnmsjsayisi)
            gelenmsj = json.loads(self.decrypt(self.istemci.mesajAl()))

            if gelenmsj[2] in self.kullanicilar:
                if self.glnmsjsayisi[self.kullanicilar.index(gelenmsj[2])] == gelenmsj[3]:

                    pass
                elif gelenmsj[3] > self.glnmsjsayisi[self.kullanicilar.index(gelenmsj[2])]:

                    self.glnmsjsayisi[self.kullanicilar.index(gelenmsj[2])] = gelenmsj[3]
                    self.mesajlar += gelenmsj[0] + " : " + gelenmsj[1] + "\n"
                    self.textEdit.setText(self.mesajlar)


            else:  # gelenmsj[2] in self.kullanicilar:
                self.kullanicilar.append(gelenmsj[2])
                self.glnmsjsayisi.append(gelenmsj[3])
                self.mesajlar += gelenmsj[0] + " : " + gelenmsj[1] + "\n"
                self.textEdit.setText(self.mesajlar)

    def gonderClick(self):

        if self.lineEdit.text() == "":
            pass
        else:
            self.msjsayisi += 1
            gondmess = [self.isim, self.lineEdit.text(), self.id_kull, self.msjsayisi]
            gondmess = self.encrypt(json.dumps(gondmess))

            self.istemci.mesajGonder(gondmess)

            self.lineEdit.clear()

    def baglantiClick(self):
        if self.istemci.durum():
            pass
        else:
            host = self.uiB.lineEdit.text()
            port = self.uiB.lineEdit_2.text()
            self.isim = self.uiB.lineEdit_3.text()

            print("host : " + host)
            print("port : " + port)

            self.istemci.baslat(host, int(port))

            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.gelenMesajKntTimer)
            self.timer.start(10)

            self.FormDailog.close()

    def menuClick(self, action):
        if action.text() == "&Bağlan":
            self.FormDailog = QtWidgets.QDialog()
            self.uiB = Baglan_Ui()
            self.uiB.setupUi(self.FormDailog)
            self.uiB.pushButton.clicked.connect(self.baglantiClick)
            self.FormDailog.exec_()


        elif action.text() == "&Çıkış":
            Dilog = QtWidgets.QDialog()
            uyari = UyariDialog()
            uyari.setupUi(Dilog)
            uyari.label.setText("Bağlantıyı kesmek istediğinize emin misiniz ??")

            if Dilog.exec_():
                self.timer.stop()
                self.istemci.durdur()
            else:
                pass

    # Şifreleme Fonksiyonları
    def pad(self, s):
        return s + ((16 - len(s) % 16) * '{')

    def encrypt(self, plaintext):
        return self.cipher.encrypt(self.pad(plaintext))

    def decrypt(self, ciphertext):
        dec = str(self.cipher.decrypt(ciphertext).decode('utf-8'))
        l = dec.count('{')
        return dec[:len(dec) - l]

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
        mesajj = "boss"
        global onoffknt
        onoffknt = False

    def baslat(self, h, p):
        global onoffknt
        self.host = h
        self.port = p
        self.tampon = 1024

        try:
            self.sock = socket.socket()
            self.sock.connect((h, p))
            glnmes = threading.Thread(target=self.gelenMessaj, )
            glnmes.start()

            onoffknt = True
        except:
            Dilog = QtWidgets.QDialog()
            uyari = UyariDialog()
            uyari.setupUi(Dilog)
            uyari.label.setText("Bağlantı Kurulamadı")
            Dilog.exec()
            onoffknt = False

    def durdur(self):
        self.sock.close()
        global onoffknt
        onoffknt = False

    def gelenMessaj(self):
        global mesajj
        global onoffknt
        try:
            while True:
                data = self.sock.recv(self.tampon)

                if data == "":
                    pass
                elif data == bytes():
                    mesajj = "Server Baglantı koptu"
                    break
                else:
                    mesajj = data

                time.sleep(0.02)
        except Exception as problem:
            print(problem)
            onoffknt = False

    def mesajGonder(self, messaj):
        self.sock.send(messaj)

    def mesajAl(self):
        return mesajj

    def durum(self):
        return onoffknt


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

        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setText("Melih")
        self.gridLayout.addWidget(self.lineEdit_3, 3, 1, 1, 1)

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

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
        self.label_3.setText(_translate("Form", "İsim :"))


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
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
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
    def myExitHandler():
        ui.istemci.durdur()
        ui.timer.stop()
        os._exit(0)


    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.aboutToQuit.connect(myExitHandler)

    sys.exit(app.exec_())


