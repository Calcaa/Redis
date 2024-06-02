import redis
from sys import exit
import time
import os
from datetime import datetime
import pandas as pd
from colorama import init, Fore, Back, Style 

# Connessione a Redis
def connessioneCloud() -> redis:

    try:
        r = redis.Redis(host="redis-11521.c135.eu-central-1-1.ec2.redns.redis-cloud.com", port=11521, password="sUaEw4HsesMiuONu3MURRZvuUDLqXeEi", db=0, decode_responses=True)
        print(f"Stato db: {r.ping()}")
        print("Connessione a redis riuscita!")
        return r
    except redis.ConnectionError:
        print("Connessione a redis fallita!")
        exit()

#FUNZIONE PER ACCEDERE, chiede nome, se esiste chiede psw, se corretta dà il bentornato.
def ACCESSO(r, nome, password):
        
    # richiesta nome utente
    pw_utente = r.hget("Utenti", nome)
    
    if pw_utente:
        
        # se psw inserita corrisponde ad esistente
        if password == pw_utente:
            print(f"Bentornato \u001b[96m{nome}\u001b[37m!") 
            return True
        else:
            # se la psw inserita non corrisponde a quella esistente
            print("Password errata")
            return False
            
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

def ricercaContatto(r, nome_contatto):
    membri = r.smembers('Utenti:Nomi')
    membri = list(membri)
    df = pd.DataFrame(membri, columns=['Utenti'])
    df = df[df['Utenti'].apply(lambda x: x.startswith(nome_contatto))]
    for element in df['Utenti']:
        print(element)
    
    if len(df) == 0:
        print("Nessun utente corrispone a ciò che hai cercato " + (Fore.RED + "non esiste!"))



# FUNZIONE PER REGISTRARSI, chiede nome utente, se non è gia presente chiede di inserire una psw
# poi salva nome utente e psw e dà il benvenuto. infine chiede di aggiungere il primo contatto.

def registrazione (r : redis, nome_utente : str, pw : str) -> None:
         # salva utente e psw
        r.hset("Utenti",nome_utente, pw)
        r.hset('DND', nome_utente, 0) #crea un hash assieme al nome utente per il dnd
        r.sadd('Utenti:Nomi',nome_utente)

        # Benvenuto
        print(f"Benvenuto su Faketsapp, {nome_utente}!\n")


def aggiungiContatto(r : redis, nome_utente : str, contatto_da_aggiungere : str):

    # se il contatto esiste
    p_c = r.hexists("Utenti", contatto_da_aggiungere)

    if p_c:
        # INSERIRE FUNZIONE CHE AGGIUNGE ALLA LISTA PERSONALE UTENTE
        r.sadd(f"Amici:{nome_utente}",contatto_da_aggiungere)
        print(f"Contatto {contatto_da_aggiungere} aggiunto alla tua rubrica!")
        
    
    # se il contatto non esiste
    else:
        print("Non esiste alcun utente con questo nome!")

# Funzione pulisci terminale
def PulisciTerminale():
    pulisci = "clear"
    if os.name in ("nt", "dos"):
        pulisci = "cls"
    os.system(pulisci)


# Funzione di chat
def Chat(r : redis, nome_utente : str, destinatario : str, effimera : bool, reverse : bool):

    

        # Funzione che stampa i mess con > e <
        def leggiChat(r : redis, chiaveNomi, nome_utente, destinatario, reverse):

            # visualizzazione dal mess meno recente al più recente
            if reverse == False:
                messaggi = r.zrange(chiaveNomi,0,-1)

            # visualizzazione dal mess più recente al meno recente
            else:
                messaggi = r.zrevrange(chiaveNomi,0,-1)

            print(f"\u001b[96m>> Chat con {destinatario} <<\n\u001b[37m(scrivi \u001b[93msys exit\u001b[37m se intendi tornare al menù)\n")
            
            # per ogni messaggio scrive > se il messaggio appartiene al mittente, altrimenti <
            for messaggio in messaggi:
                parti = messaggio.split(":")
                mittente = parti[0].strip()
                if mittente == nome_utente:
                    print(f"> {messaggio}")
                else:
                    print(f"< {messaggio}")
            
        
        # cerca se l'utente è tra gli amici
        if r.sismember(f"Amici:{nome_utente}", destinatario):
            if r.hget("DND", destinatario) == '0':
                    
                    # crea la chiave del sorted set unendo i nomi dei due utenti in chat
                    listaNomi = [nome_utente, destinatario]
                    chiaveNomi = "".join(sorted(listaNomi))
                    
                    # riporta i messaggi della tipologia di chat (effimera e non)
                    if effimera == False:
                        leggiChat(r, chiaveNomi, nome_utente, destinatario, reverse)
                    else: 
                        leggiChat(r, f"Effimera:{chiaveNomi}", nome_utente, destinatario, reverse)
                    
                    # inizio ciclo di scrittura mess
                    while True:

                        # richiesta input mess
                        messaggio = input("\u001b[1mMessaggio: ")

                        # pulisce il terminale ad ogni invio
                        PulisciTerminale()

                        # se l'utente scrive sys exit esce dal ciclo
                        if messaggio.lower() == "sys exit":
                            break
                        
                        # se l'utente scrive qualcosa
                        elif messaggio != "":
                            
                            # se la chat è effimera viene creato il sorted set per chat effimera in cui vengono salvati i mess
                            if effimera == True:
                                r.zadd(f"Effimera:{chiaveNomi}", {f"{nome_utente}: {messaggio}\t\t\t\t[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]":time.time()})
                                r.expire(f"Effimera:{chiaveNomi}",60)

                                # vengono ristampati i messaggi
                                leggiChat(r, f"Effimera:{chiaveNomi}", nome_utente, destinatario, reverse)
                            
                            # se la chat non è effimera viene creato il sorted set per chat normale in cui vengono salvati i mess
                            else:
                                r.zadd(chiaveNomi, {f"{nome_utente}: {messaggio}\t\t\t\t[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]":time.time()})
                                r.sadd(f"Chat{nome_utente}",f"Chat con {destinatario}")

                                # vengono ristampati i messaggi
                                leggiChat(r, chiaveNomi, nome_utente, destinatario, reverse)

            # se il destinatario ha la modalità DnD attiva                   
            else: 
                print("Errore: L'utente ha la modalita' non disturbare attiva")
        
        # se il destinatario non è amico
        else: 
            print("Il contatto non e' tuo amico")

# Funzione do not disturb
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
    print(f"\n\n\u001b[93mChi intendi eliminare?\n")
    for amico in amici:
        print(f"\u001b[37m{amico}")
    amico = input("\nNome: ")
    
    if r.sismember(f"Amici:{nome_utente}",amico):
        print(f"\u001b[93mAmico {amico} rimosso!\u001b[37m")
        r.srem(f"Amici:{nome_utente}",amico)
    else:
        print(f"\n\u001b[93mNon hai alcun amico con questo nome!\u001b[37m")

# Funzione mostra chat
def MostraChat (r,nome_utente):
    lista_chat = r.smembers(f"Chat{nome_utente}")
    print(f"\n\u001b[93mEcco le tue chat:\u001b[37m \n")
    for chat in lista_chat:
        print(chat)






