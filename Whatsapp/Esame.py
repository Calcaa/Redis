import redis
import redisfunc
from sys import exit

# connessione a Redis cloud
r = redisfunc.cloudConnect()

#FUNZIONE PER ACCEDERE, chiede nome, se esiste chiede psw, se corretta dà il bentornato.
def ACCESSO ():
    global utente_on
    # richiesta nome utente
    nome_utente = input("Inserisci il tuo nome utente: ")
    pw_utente = r.hget("Utenti", nome_utente)
    if pw_utente:
        # richiesta psw
        pw = input("Inserisci la password")
        # se psw inserita corrisponde ad esistente
        if pw == pw_utente:
            print(f"Bentornato {nome_utente}!")
            utente_on=nome_utente
        else:
            # se la psw inserita non corrisponde a quella esistente
            print("Password errata")
    else:
        print("Non esiste un utente con questo nome")
    return nome_utente

#---------------------------------------
# Aggiungere parte per conttrollo accesso o registrazione
#   
#   es
#   nomeutente = input...
#   pw = input...
#   ...
# 
#--------------------------------------


def SCEGLI_AZIONE():
    Scelta = input("0 - Esci\n1 - Cerca utenti\n2 - Aggiungi contatto")
    return Scelta

print("Benvenuto su AAAAAAAAAtsapp la nota app di SCONTRI!")
accesso = input("Scrivi ACCEDI se possiedi già un account, altrimenti REGISTRATI.")

# se scegli di accedere
if accesso == "ACCEDI":
    ACCESSO()
# se scegli di registrarti
elif accesso == "REGISTRATI":
    REGISTRAZIONE()
    # obbligo ad aggiungere il primo contatto
    AGGIUNTA_CONTATTO()

#SCEGLI_AZIONE()





    
    
