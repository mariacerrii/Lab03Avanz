from csv import reader
from operator import attrgetter

#Inseriamo una nuova classe strumento
class Strumento:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore

    def __str__(self):
        #qui devi restituire una stringa
        return f"{self.codice} - {self.tipo} - {self.marca} - {self.anno_acquisto} - {self.valore}"

#Inseriamo una nuova classe per prestito
class Prestito:
    def __init__(self, codice, data, id_strumento, cognome_allievo):
        self.codice = codice
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        # qui devi restituire una stringa
        return f"{self.codice} - {self.data} - {self.id_strumento} - {self.cognome_allievo}"

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        #self = riferimento all'oggetto corrente
        # self.nome = attributo appartenente all'oggetto
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        #due liste vuote
        self.strumenti = []
        self.prestiti = []
        #Necessario per inserimento nuovo prestito
        self.contatore_prestiti = 0

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        #Prendiamo spunto dal LAIB02
        #Qui non c'è bisogno di mettere try-except perchè vogliamo scatenare in caso FileNotFoundError
        inFile = open(file_path, "r", encoding="utf-8")
        # Legge il file come CSV
        csvReader = reader(inFile)
        # Legge uno strumento alla volta
        for row in csvReader:
            codice = row[0]
            tipo = row[1]
            marca = row[2]
            anno_acquisto = int(row[3])
            valore = float(row[4]) #usi float dato che è valore decimale
            strumento = Strumento(codice, tipo, marca, anno_acquisto, valore)
            self.strumenti.append(strumento)
        inFile.close()

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        # ultimo.codice→ "S10"
        # ultimo.codice[1:]→ "10"
        # int(...)→ 10
        if len(self.strumenti) == 0:
            numero_codice = 0
        else:
            ultimo = self.strumenti[-1]
            # [1:] toglie la S
            numero_codice = int(ultimo.codice[1:])
        #aggiungere +1 codice
        numero_codice = numero_codice + 1
        #trasformi in una stringa
        numero_codice = str(numero_codice)
        #ci aggiungi s
        nuovo_codice = "S" + numero_codice
        strumento = Strumento(nuovo_codice, tipo, marca, anno_acquisto, valore)
        self.strumenti.append(strumento)
        return strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        strumenti_ordinati = sorted(self.strumenti, key=attrgetter("marca"))
        return strumenti_ordinati

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        #Prestito: codice univoco, data, codice univoco strumento, cognome allievo
        #Codice univoco: P+numero
        #Codice assegnato nel momento in cui prestito viene creato
        # 1) Controllo che lo strumento esista
        strumento_trovato = False
        for strumento in self.strumenti:
            if strumento.codice == id_strumento:
                strumento_trovato = True
        if strumento_trovato == False:
            #Scateno io un'eccezione (richiesto dalla consegna)
            raise Exception("Strumento non presente nel deposito")
        # 2) Controllo che non sia già in prestito
        for prestito in self.prestiti:
            if prestito.id_strumento == id_strumento:
                raise Exception("Questo strumento è già in prestito")
        # 3) Creo codice progressivo prestito
        self.contatore_prestiti = self.contatore_prestiti + 1
        nuovo_codice = "P" + str(self.contatore_prestiti)
        #4) Credo prestito e aggiungo a lista
        prestito = Prestito(nuovo_codice,data, id_strumento, cognome_allievo)
        self.prestiti.append(prestito)
        return prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        prestito_fatto= False
        for prestito in self.prestiti:
            if prestito.codice == id_prestito:
                self.prestiti.remove(prestito)
                prestito_fatto = True
        if prestito_fatto == False:
            raise Exception("Prestito non in atto")


