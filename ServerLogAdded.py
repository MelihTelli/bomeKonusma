#!/usr/bin/env python3
import threading
import socket
import os
import datetime
class Server():
    def __init__(self,h,p,u):
        self.host = h
        self.port = p
        self.user = u
        self.tampon = 1024
        self.baglantilar=[]

        self.sock = socket.socket()

        self.sock.bind((self.host,self.port))
        self.sock.listen(self.user)

        bagkbl = threading.Thread(target=self.bagKabul,)
        bagkbl.start()
        with open("log.txt", "a")as logTxt:
            logTxt.write(str(datetime.datetime.now().year)+"/"+str(datetime.datetime.now().month)+"/" +str(datetime.datetime.now().day)+" : "+str(datetime.datetime.now().hour) +"/"+str(datetime.datetime.now().minute)+"/"+  str(datetime.datetime.now().second) +" >>> " + " Program Baslası __ init  "+"\n")
            logTxt.close()


    def bagKabul(self):
        for i in range(self.user):
            self.baglnt,self.adrr = self.sock.accept()
            self.baglantilar.append(self.baglnt)
            for i in range(len(self.baglantilar)):
                msjgndthrd = threading.Thread(target=self.messajGonder,args=(i,))
                msjgndthrd.start()

            bagkbl = threading.Thread(target=self.bagKabul, )
            bagkbl.start()



    def messajGonder(self,kulS):
        try:
            while True:
                data = self.baglantilar[kulS].recv(self.tampon)

                if not data :

                    with open("log.txt", "a")as logTxt:
                        logTxt.write(str(datetime.datetime.now().year)+"/"+str(datetime.datetime.now().month)+"/" +str(datetime.datetime.now().day)+" : "+str(datetime.datetime.now().hour) +"/"+str(datetime.datetime.now().minute)+"/"+  str(datetime.datetime.now().second) +" >>> "   + str(self.baglantilar[kulS])+" Çıkış yaptı "+"\n")
                        logTxt.close()

                    self.baglantilar.remove(self.baglantilar[kulS])


                    break

                else :
                    for i in range(len(self.baglantilar)):
                       # print("Messaj gonder for içi : " + str(i))
                        self.baglantilar[i].send(data)


        except Exception as problem :
            self.baglantilar.remove(self.baglantilar[kulS])
            #print(str(problem ))
            with open("log.txt","a")as logTxt:
                logTxt.write(str(datetime.datetime.now().year) + "/" + str(datetime.datetime.now().month) + "/" + str(
                    datetime.datetime.now().day) + " : " + str(datetime.datetime.now().hour) + "/" + str(
                    datetime.datetime.now().minute) + "/" + str(datetime.datetime.now().second) + " >>> " + str(
                    problem)+"\n")
                logTxt.write("PROGRAM KAPATILDI\n")
                logTxt.close()

            os._exit(0)




if __name__ =="__main__":
    server = Server("192.168.1.45",31312,5)
    with open("log.txt", "a")as logTxt:
        logTxt.write(str(datetime.datetime.now().year)+"/"+str(datetime.datetime.now().month)+"/" +str(datetime.datetime.now().day)+" : "+str(datetime.datetime.now().hour) +"/"+str(datetime.datetime.now().minute)+"/"+  str(datetime.datetime.now().second) +" >>> " + " Program Basladı __ name "+"\n")
        logTxt.close()