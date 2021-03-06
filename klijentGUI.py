import time, tkinter, random, re, threading, socket, datetime
import Narudzbina
from Narudzbina import *
from tkinter import *
from tkinter import messagebox


podaci = {}

class Izuzetak(Exception):
    def __init__(self, poruka):
        self.poruka = poruka
    def __str__(self):
        return self.poruka

def crtajGui():
    global podaci

    prozor = Tk()
    prozor.geometry("800x650")

    lblDobrodosli = Label(prozor, text="Dobro došli u aplikaciju za naručivanje pice!", font=("Helvetica",24,"bold"))
    lblDobrodosli.pack()
    lblUputstvo = Label(prozor, text="Popunite sledeća polja...", font=("Arial",16,"italic"))
    lblUputstvo.pack(pady=20)
    framePolja = Frame()
    framePolja.pack(pady=40)

    fontGlavnihLabela = ("Arial",16,"bold")
    fontKontrola = ("Arial",12)
    #VELICINAA
    lblVelicina = Label(framePolja, text="Odaberite velicinu:",font=fontGlavnihLabela).grid(row=0,column=0, padx=20)
    lstVelicina = Listbox(framePolja, selectmode=SINGLE, height=3, font=fontKontrola)
    lstVelicina.insert(0,25)
    lstVelicina.insert(1,32)
    lstVelicina.insert(2,50)
    lstVelicina.activate(0)
    lstVelicina.select_set(0,0)
    lstVelicina.grid(row=1,column=0, padx=20, pady=10)
    podaci["velicina"] = lstVelicina

    #VRSTAA
    lblVrsta = Label(framePolja, text="Odaberite vrstu:", font=fontGlavnihLabela).grid(row=0, column=1, padx=350)

    varVrsta = StringVar()
    varVrsta.set("--odabrana vrsta--")
    optVrsta = OptionMenu(framePolja,varVrsta, 'Margarita', 'Funghi', 'Quatro  Stagione', 'Vegeteriana', 'Plavi Jadran')
    optVrsta.grid(row=1,column=1, padx=20)
    optVrsta.config(font=fontKontrola)
    podaci["vrsta"] = varVrsta

    #DODACIII
    frameDodaci = Frame(framePolja)
    frameDodaci.grid(row=3, column=0)
    lblDodaci = Label(framePolja, text="Odaberite dodatke:", font=fontGlavnihLabela).grid(row=2, column=0, padx=20)
    listaChkDodataka = []
    varKecap = IntVar()
    varMajonez = IntVar()
    varOrigano = IntVar()
    kecap = Checkbutton(frameDodaci, text="Kecap", variable=varKecap)
    majonez = Checkbutton(frameDodaci, text="Majonez", variable=varMajonez)
    origano = Checkbutton(frameDodaci, text="Origano", variable=varOrigano)
    listaChkDodataka.append(kecap)
    listaChkDodataka.append(majonez)
    listaChkDodataka.append(origano)
    for i in range(0, len(listaChkDodataka)):
        listaChkDodataka[i].grid(row=i, column=0, sticky='w')
    podaci["dodaci"] = [varKecap, varMajonez, varOrigano]

    #NACIN PLACANJA
    framePlacanje = Frame(framePolja)
    framePlacanje.grid(row=3, column=1)
    lblPlacanje = Label(framePolja, text="Nacin placanja:", font=fontGlavnihLabela).grid(row=2, column=1, padx=20)
    varPlacanje = IntVar()
    radioKes = Radiobutton(framePlacanje, text="Keš", variable=varPlacanje, value=0).grid(row=0,column=0, sticky='w')
    radioKartica = Radiobutton(framePlacanje, text="Kartica", variable=varPlacanje, value=1).grid(row=1,column=0, sticky='w')
    podaci["placanje"] = varPlacanje

    #ADRESA
    lblAdresa = Label(framePolja, text="Adresa:", font=fontGlavnihLabela).grid(row=4, column=0, padx=20)
    varAdresa = StringVar()
    entAdresa = Entry(framePolja, textvariable=varAdresa, width=30).grid(row=5, column=0, sticky='n', rowspan=2)
    podaci["adresa"] = varAdresa

    #Broj telefona
    lblTelefon = Label(framePolja, text="Telefon:", font=fontGlavnihLabela)

    global varTelefon
    varTelefon = StringVar()
    entTelefon = Entry(framePolja, textvariable=varTelefon)
    lblTelefon.grid(row=5, column=0, sticky='n', pady=30, rowspan=1)
    entTelefon.grid(row=5,column=0, sticky='n', pady=70)
    #regex unos
    lblObavestenje = Label(framePolja, text="U formatu: xxx/xxx-xxx", font=("Arial", 12, "italic"))
    lblObavestenje.grid(row=5,column=0, sticky='n', pady=110)
    podaci["telefon"] = varTelefon

    #Napomena
    lblNapomena = Label(framePolja, text="Napomena:", font=fontGlavnihLabela).grid(row=4, column=1, padx=20)
    text = Text(framePolja, width=30, height=10)
    text.grid(row=5, column=1, padx=20, sticky='n')
    podaci["napomena"] = text

    #OpcionalnostNapomene
    lblOpciono = Label(framePolja, text="*Opciono...", font=("Arial", 12, "italic"))
    lblOpciono.grid(row=5, column=1, pady=170)


    #posalji
    btnPosalji = Button(framePolja,text="Pošalji narudžbinu!", font=fontGlavnihLabela, command=prikazi)
    btnPosalji.grid(row=5,column=0,sticky='n', pady=150)
    prozor.mainloop()

def prikazi():
    # messagebox.showwarning("Greska!", "Odaberite vrstu!")
    velicina = str(podaci["velicina"].get(ACTIVE)) + " "
    porukaIzuzetka=""
    try:
        vrsta = str(podaci["vrsta"].get())
        if vrsta == "--odabrana vrsta--":
            porukaIzuzetka +="Odaberite vrstu!\n"
        adresa = podaci["adresa"].get()
        if adresa == "":
            porukaIzuzetka += "Morate popuniti adresu!\n"
        telefon = podaci["telefon"].get()

        if not re.match(r"\d{3}/\d{3}-\d{3}", telefon):
            porukaIzuzetka += "Neispravno popunjen telefon!"

        if porukaIzuzetka != "":
            raise Izuzetak(porukaIzuzetka)

        dodaci = []
        if podaci["dodaci"][0].get() != 0:
            dodaci.append("Kecap")
        if podaci["dodaci"][1].get() != 0:
            dodaci.append("Majonez")
        if podaci["dodaci"][2].get() != 0:
            dodaci.append("Origano")

        if podaci["placanje"].get() == 0:
            placanje = "Keš"
        else:
            placanje = "Kartica"

        napomena = podaci["napomena"].get("1.0", END)
    except Izuzetak as izuzetak:
        messagebox.showwarning("Greska!", izuzetak.poruka)
    else:

        narudzbina = Narudzbina(velicina,vrsta,dodaci,placanje,adresa,telefon,napomena)

        s.send(str(narudzbina).encode())

        #print(s.recv(1024).decode())

        # vreme = []
        # test = datetime.time(0,random.randint(0,1),random.randint(0,60))
        # print(str(test))
        # while test.minute>0 or test.second>0:
        #     test = datetime.time(0,test.minute, test.second-1)
        #
        #     if test.second == 0:
        #         test = datetime.time(0, test.minute-1, 59)
        #         print(datetime.time(0,test.minute-1,0))
        #     print(str(test))
        #     time.sleep(0.3)
        # vreme.append(random.randint(10,50))

        messagebox.showinfo("Odgovor", str(s.recv(1024).decode()))




s = socket.socket()
s.connect(('127.0.0.1', 5000))

crtajGui()

s.close()


# test = datetime.time(0,random.randint(0,1),random.randint(0,59))
# print(str(test))
# while test.minute>0 or test.second>0:
#     test = datetime.time(0,test.minute, test.second-1)
#
#     if test.minute == 0 and test.second ==0:
#         break
#
#     if test.second == 0:
#         test = datetime.time(0, test.minute-1, 59)
#         print(datetime.time(0,test.minute-1,0))
#     print(str(test))
#     time.sleep(0.3)