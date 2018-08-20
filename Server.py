#!/usr/bin/env python3
import threading
import socket

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

                print("gelen mesaj  :  " + str(data))

                for i in range(len(self.baglantilar)):
                    print("Messaj gonder for içi : "+ str(i))
                    self.baglantilar[i].send(data)

                if not data :
                    print(str(self.baglantilar[kulS].getpeername())+" Hata")

                    for i in range(len(self.baglantilar)):
                        print("ilk hali",self.baglantilar[i])

                    self.baglantilar.remove(self.baglantilar[kulS])

                    for i in range(len(self.baglantilar)):
                        print("son hali",self.baglantilar[i])

                    break

        except Exception as problem :

            print(str(problem ))




if __name__ =="__main__":
    server = Server("127.0.0.1",31312,5)