import redis
from sys import exit

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
                
        except ValueError:
            print('err')
            

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
    p_c = r.hexists("Utenti",contatto_da_aggiungere)

    if p_c:
        # INSERIRE FUNZIONE CHE AGGIUNGE ALLA LISTA PERSONALE UTENTE
        print(f"Contatto {contatto_da_aggiungere} aggiunto alla tua rubrica!")
        r.sadd(f"Amici:{nome_utente}",contatto_da_aggiungere)
    
    # se il contatto non esiste
    else:
        print("Non esiste alcun utente con questo nome!")

# FUNZIONE crea lista utenti in modalità DND, se stato è True diventa False e viceversa.
def DND_MODE(r : redis, nome_utente : str, dnd : bool) -> None:
    r.hset("Utenti:DND",nome_utente,int(not dnd)) 
