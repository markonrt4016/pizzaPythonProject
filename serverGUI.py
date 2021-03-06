import time, tkinter, random, re, threading, socket, datetime
import Narudzbina
from Narudzbina import *
from tkinter import *
from tkinter import messagebox

lstNeisporucene = ""
lstIsporucene = ""

piceNeisporucene = {}
piceIsporucene = {}
brIsporucenih = 0

nitiVreme = []

def hvatajPoruku():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()

    s.bind((host, port))
    s.listen(1)

    conn, addr = s.accept()

    print("povezan sa: ", addr)
    i=0

    global upaljeno
    while upaljeno:
        primljeno = conn.recv(1024).decode()
        print(str(primljeno))

        vreme = datetime.time(0, random.randint(0, 1), random.randint(0, 30))
        # print(str(test))

        conn.send(("Vaša naruddžbina će biti isporučena za: " + str(vreme)).encode())
        global piceNeisporucene

        piceNeisporucene[i] = [primljeno, vreme]
        if threading.activeCount() < 4:
            t3.start()
        print("Trenutno: ", threading.activeCount())

        global nitiVreme
        brava.acquire()
        nitiVreme.append(threading.Thread(target=racunajVreme, args=(vreme,i)))
        brava.release()
        brava.acquire()
        for nit in nitiVreme:
            if not nit.isAlive():
                nit.start()
                nitiVreme.remove(nit)
        brava.release()
        i+=1


    conn.close()
    print("Gotovoo")

def ispisujNeisporucene():
    global lstNeisporucene
    global piceNeisporucene
    while True:
        lstNeisporucene.delete(0, END)
        for key in piceNeisporucene.keys():
            lstNeisporucene.insert(key, piceNeisporucene[key][0] + " vreme isporuke: " + str(piceNeisporucene[key][1]))

            print("imamo: ",piceNeisporucene[key][1])

        time.sleep(0.2)

def racunajVreme(vreme, i):
    while vreme.minute > 0 or vreme.second > 0:
        vreme = datetime.time(0, vreme.minute, vreme.second - 1)
        global brIsporucenih
        global piceIsporucene
        if vreme.minute == 0 and vreme.second == 0:
            lstIsporucene.insert(brIsporucenih, piceNeisporucene[i][0])
            piceNeisporucene.pop(i,None)
            break
        else:
            piceNeisporucene[i][1]=vreme
        #print("usao test")
        if vreme.second == 0:
            vreme = datetime.time(0, vreme.minute - 1, 59)
            #print(vreme)
        print(str(vreme))
        time.sleep(0.2)


upaljeno = True
def crtajGui():
    prozor = Tk()
    prozor.geometry("1200x650")
    lblDobrodosli = Label(prozor, text="Dobro došli na server deo!", font=("Helvetica", 24, "bold"))
    lblDobrodosli.pack()
    lblUputstvo = Label(prozor, text="Pogledajte isporučene i neisporučene pice...", font=("Arial", 16, "italic"))
    lblUputstvo.pack(pady=20)

    framePolja = Frame()
    framePolja.pack(pady=30)

    lblIsporucene = Label(framePolja, text="Isporučene pice", font=("Arial", 16, "italic"))
    lblIsporucene.grid(row=0, column=0)

    frameScrollNeisporucene = Frame()
    frameScrollNeisporucene.place(x=610, y=320, width=575)
    frameScrollIsporucene = Frame()
    frameScrollIsporucene.place(x=25, y=328, width=575, anchor=W)

    global lstIsporucene
    lstIsporucene = Listbox(framePolja, selectmode=SINGLE, width=95)
    lstIsporucene.grid(row=1, column=0, padx=10)

    scrollIsporucene = Scrollbar(frameScrollIsporucene, orient=HORIZONTAL)
    scrollIsporucene.config(command=lstIsporucene.xview)
    scrollIsporucene.pack(side=BOTTOM, fill=X)

    lblNeisporucene = Label(framePolja, text="Neisporučene pice", font=("Arial", 16, "italic"))
    lblNeisporucene.grid(row=0, column=1)
    global lstNeisporucene

    lstNeisporucene = Listbox(framePolja, selectmode=SINGLE, width=95)
    scrollNeisporucene = Scrollbar(frameScrollNeisporucene, orient=HORIZONTAL)
    scrollNeisporucene.config(command=lstNeisporucene.xview)
    lstNeisporucene.grid(row=1, column=1)
    scrollNeisporucene.pack(side=BOTTOM, fill=X)
    t2.start()
    prozor.mainloop()
    global upaljeno
    upaljeno = False



t1 = threading.Thread(target=crtajGui, args=())
t2 = threading.Thread(target=hvatajPoruku, args=())
brava = threading.Lock()

t3 = threading.Thread(target=ispisujNeisporucene, args=())

t1.start()

