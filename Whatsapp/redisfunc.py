import redis
from sys import exit
import time

# Connessione a Redis
def connessioneCloud() -> redis:

    try:
        r = redis.Redis(host="redis-11521.c135.eu-central-1-1.ec2.redns.redis-cloud.com", port=11521, password="sUaEw4HsesMiuONu3MURRZvuUDLqXeEi", db=0, decode_responses=True)
        print(f"Stato db: {r.ping()}")
        print("Connessione a redis in locale riuscita!")
        return r
    except redis.ConnectionError:
        print("Devi avviare Docker e runnare il container con Redis!")
        exit()

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
        try:
            scelta = input('Vuoi registrare questo nuovo utente? y/n\nScelta: ')
            if scelta.lower() == 'y':
                registrazione(r, nome, password)
            else:
                print('Il nuovo utente non verrà registrato')
                exit()
                
        except ValueError:
            print('err')

def controllaContatto(r : redis, nome_contatto):

    if r.sismember('Utenti:Nomi', nome_contatto):
        return True
    return False


# FUNZIONE PER REGISTRARSI, chiede nome utente, se non è gia presente chiede di inserire una psw
# poi salva nome utente e psw e dà il benvenuto. infine chiede di aggiungere il primo contatto.

def registrazione (r : redis, nome_utente : str, pw : str) -> None:
         # salva utente e psw
        r.hset("Utenti",nome_utente, pw)
        r.sadd('Utenti:Nomi',nome_utente)

        # Benvenuto
        print(f"Benvenuto su AAAAAAAAAtsapp, {nome_utente}!\n")


def aggiungiContatto(r : redis, nome_utente : str, contatto_da_aggiungere : str):

    # se il contatto esiste
    p_c = r.hexists("Utenti", contatto_da_aggiungere)

    if p_c:
        # INSERIRE FUNZIONE CHE AGGIUNGE ALLA LISTA PERSONALE UTENTE
        print(f"Contatto {contatto_da_aggiungere} aggiunto alla tua rubrica!")
        r.sadd(f"Amici:{nome_utente}",contatto_da_aggiungere)
    
    # se il contatto non esiste
    else:
        print("Non esiste alcun utente con questo nome!")


def ApriChat(r : redis, nome_utente : str, destinatario : str):

    if controllaContatto(r, destinatario):
            
        if r.sismember(f"Amici:{nome_utente}", destinatario):
            
            listaNomi = [nome_utente, destinatario]
            chiaveNomi = "".join(sorted(listaNomi))
            if r.hexists(chiaveNomi, chiaveNomi + ":*"):
                #mettere la funzione asincrona per refreshare messaggi
                pass
            
            messaggio = input("Messaggio: ")
            r.hset(chiaveNomi, f"{chiaveNomi}:{nome_utente}:{str(time.time())}", messaggio)
            print(f"Messaggio inviato nella chat {chiaveNomi} con chiave {chiaveNomi}:{nome_utente}:{str(time.time())}")
        else:
            print("Il contatto non e' tuo amico")
    else:
        print("Questa persona non esiste")