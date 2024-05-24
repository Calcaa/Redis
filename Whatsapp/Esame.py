import redis
import redisfunc


# connessione a Redis cloud
r = redisfunc.cloudConnect()

#FUNZIONE PER ACCEDERE, chiede nome, se esiste chiede psw, se corretta dà il bentornato.
def ACCESSO(r, nome, password):
        
    # richiesta nome utente
    pw_utente = r.hget("Utenti", nome)
    
    if pw_utente:
        # se psw inserita corrisponde ad esistente
        if password == pw_utente:
            print(f"Bentornato {nome}!") 
        else:
            # se la psw inserita non corrisponde a quella esistente
            print("Password errata")
    else:
        print("Non esiste un utente con questo nome")
        REGISTRAZIONE(nome, password)

# FUNZIONE PER REGISTRARSI, chiede nome utente, se non è gia presente chiede di inserire una psw
# poi salva nome utente e psw e dà il benvenuto. infine chiede di aggiungere il primo contatto.
utente_on = ""

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





    
    
