import redis
from sys import exit
from datetime import datetime
import os

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
        r.hset('DND', nome_utente, 0) #crea un hash assieme al nome utente per il dnd
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



def invia_messaggio(r, chiaveNomi, nome_utente, messaggio, effimera, destinatario):
    ora = datetime.now()
    oraStr = ora.strftime("[%d/%m/%Y-%H:%M:%S]")
    if effimera:
        r.hset(f"Chat:{chiaveNomi}", f"{chiaveNomi}:{nome_utente}:{ora}", f'{oraStr}\t {nome_utente}:{messaggio}')
        r.expire(f"Chat:{chiaveNomi}", 60)
    else:
        r.hset(f"Chat:{chiaveNomi}", f"{chiaveNomi}:{nome_utente}:{ora}", f'{oraStr}\t {nome_utente}:{messaggio}')
        r.sadd(f"Chat:{nome_utente}", f"Chat-Con-{destinatario}")
    
    r.publish(chiaveNomi, f"{nome_utente}:{messaggio}")
    ascolta_chat(r, chiaveNomi, nome_utente) #test
    
'''def ascolta_chat(r, chiaveNomi, nome_user):
    pubsub = r.pubsub()
    pubsub.subscribe(chiaveNomi)

    for message in pubsub.listen():
        if message['type'] == 'message':
            
            os.system('cls')
            chat = r.hgetall(f'Chat:{chiaveNomi}')
            for key, messaggio in sorted(chat.items()):
                timestamp, user_msg = messaggio.split(' ', 1)
                user, msg = user_msg.split(':', 1)
                if user == nome_user:
                    print(f"{timestamp} > {msg}")
                else:
                    print(f"{timestamp} < {msg}")  '''  
    
def ascolta_chat(r, chiaveNomi, nome_user):
    pubsub = r.pubsub()
    pubsub.subscribe(chiaveNomi)
    message = pubsub.listen()
    
    os.system('cls')
        
    '''chat = r.hgetall(f'Chat:{chiaveNomi}')
    for key, messaggio in chat.items():
            timestamp, user_msg = messaggio.split(' ', 1)
            user, msg = user_msg.split(':', 1)
            if user == nome_user:
                print(f"{timestamp} > {msg}")
            else:
                print(f"{timestamp} < {msg}")'''
     
    if not message is None:
        chat = r.hgetall(f'Chat:{chiaveNomi}')
        for key, messaggio in chat.items():
            timestamp, user_msg = messaggio.split(' ', 1)
            user, msg = user_msg.split(':', 1)
            if user == nome_user:
                print(f"{timestamp} > {msg}")
            else:
                print(f"{timestamp} < {msg}")
        

        

def DoNotDisturb(r, nome_user):
    
    if r.hget('DND', nome_user) == '0':
        r.hincrby('DND', nome_user, 1)
        print('Do not disturb attivato')
    else:
        r.hincrby('DND', nome_user, -1)
        print('Do not disturb disattivato')

# Funzione per eliminare amico, restituisce la lista amici e chiede chi vuoi eliminare.
def EliminaAmico (r,nome_utente):
    amici = r.smembers(f"Amici:{nome_utente}")
    amico = input(f"Chi intendi eliminare?\n{amici}\n")
    
    if r.sismember(f"Amici:{nome_utente}",amico):
        print(f"Amico {amico} rimosso!")
        r.srem(f"Amici:{nome_utente}",amico)
    else:
        print(f"Non hai alcun amico con questo nome!")

# Funzione mostra chat
def MostraChat (r,nome_utente):
    lista_chat = r.smembers(f"Chat{nome_utente}")
    print(f"Ecco le tue chat:  {lista_chat}")