import sys

class Narudzbina:
    def __init__(self, velicina, vrsta, dodaci, placanje, adresa, tel, napomena):
        self.velicina = velicina
        self.vrsta = vrsta
        self.dodaci = dodaci
        self.placanje = placanje
        self.adresa = adresa
        self.tel = tel
        self.napomena = napomena

    def __str__(self):
        strDodaci=""
        for d in self.dodaci:
            strDodaci+=str(d) + ", "
        return "Velicina: " + str(self.velicina) + " Vrsta: " + self.vrsta + " Dodaci: " + strDodaci + " Placanje: " + str(self.placanje) + " Adresa: " + self.adresa + " Telefon: " + self.tel + " Napomena: " + self.napomena
