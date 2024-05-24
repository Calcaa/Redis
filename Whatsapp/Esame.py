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
#--------------------------------------


# FUNZIONE PER REGISTRARSI, chiede nome utente, se non è gia presente chiede di inserire una psw
# poi salva nome utente e psw e dà il benvenuto. infine chiede di aggiungere il primo contatto.

def registrazione (nome_utente : str, pw : str):

    # se il nome utente non esiste
    if not r.exists(nome_utente):
        
        # salva utente e psw
        r.hset("Utenti",nome_utente, pw)

        # Benvenuto
        print(f"Benvenuto su AAAAAAAAAtsapp, {nome_utente}!\n") 

        # richiama funzione aggiungi contatto
        print("Cerca subito un utente con cui chattare!")
        AGGIUNTA_CONTATTO()

    # se il nome utente esiste già
    else: 
        print("esiste già un utente con questo nome!")

def AGGIUNTA_CONTATTO():
    global utente_on
    # chiede nome del primo contatto
    contatto = input("Chi vuoi aggiungere alla tua rubrica?")
    # se il contatto esiste
    p_c = r.hexists("Utenti",contatto)
    if p_c:
        # INSERIRE FUNZIONE CHE AGGIUNGE ALLA LISTA PERSONALE UTENTE
        print(f"Contatto {contatto} aggiunto alla tua rubrica!")
        r.sadd(f"Amici:{utente_on}",contatto)
    
    # se il contatto non esiste
    else:
        print("Non esiste alcun utente con questo nome!")

def SCEGLI_AZIONE():
    SCELTA = input("1 - CERCA UTENTI\n2 - ")
    return SCELTA

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





    
    
