import redis
from sys import exit

'''
Obiettivo:
realizzare un applicazione CLI Python che gestisca il processo di votazione di proposte da parte degli studenti
Utilizzare Redis come database

L app Python deve permettere di caricare le proposte
Ogni proposta ha un proponente
Ogni studente può votare tutte le proposte che vuole, ma al massimo un voto per proposta
In ogni momento l applicazione può mostrare la lista delle proposte ordinate per numero di voti

'''
#aprite docker e create un container chiamato '' di redis, con la porta 6379, passo cruciale o ciuccia
#avere python 3.12.1

# connessione a redis
while True:
    try:
        r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        print(f"Stato db: {r.ping()}")
        print("Connessione a redis in locale riuscita!")
    except redis.ConnectionError: 
        print("Devi avviare Docker e runnare il container con Redis!")
        exit()
    
    # richiesta nome utente 
    print(f"Benvenuto, inserisci il tuo nome utente.")
    nome_utente = input("Nome utente: ")

    pw_utente = r.get(nome_utente)
    if pw_utente:

        # richiesta psw
        pw = input("Password: ")

        # se psw inserita corrisponde ad esistente
        if pw == pw_utente:
            print(f"Benvenuto {nome_utente}\n")

            while True:
                # selezione azione
                choose = input(f"\n\nCosa vuoi fare?\n1 - Aggiungi proposta\n2 - Vota Proposta\n3 - Visualizza proposte\n4 - Visualizza voti\n5 - Esci\n\nScelta: ")

                # 1 - scelta aggiunta proposta
                if choose == "1":
                    nome_proposta = input("Nome proposta: ")
                    descrizione_proposta = input("Descrizione: ")

                    r.set(f"Proposte:{nome_proposta}", f"{descrizione_proposta}")
                
                # 2 - scelta voto proposta
                elif choose == "2":
                    nome_proposta = input("Che proposta vuoi votare?\nNome: ")

                    if r.get(nome_proposta):
                        if not r.get(f"{nome_utente}:Voti:{nome_proposta}"):
                            r.incr(f"Voti:{nome_proposta}")
                            r.set(f"{nome_utente}:Voti:{nome_proposta}", 1)
                        else:
                            print(f"Abbello, hai gia votato sta proposta... fatte un giro")
                    else:
                        print("Nooonnn Iesiìììstie\n-NON ESISTE (in italiano)")

                # 3 - scelta lettura proposte
                elif choose == "3":
                    proposte = r.keys('Proposte:*')
                    for proposta in proposte:
                        print(f'Nome: {proposta.split(':')[1]}')
                        print(f'Descrizione: {r.get(proposta)}\n')
                 
                elif choose == '4':
                    proposte = r.keys('Proposte:*')
                    for proposta in proposte:
                        print(f'Nome: {proposta.split(':')[1]}')
                        print(f'Voti: {r.get(f'voti:{proposta}')}\n')
                     
                   
                elif choose == '5':
                    print('bye bye')
                    break
                
                    

        else:

            # se la psw inserita non corrisponde a quella esistente
            print("Ciglione non ti ricordi la password")

    # se l'utente non esiste
    else:
        choose = input("L'utente non esiste, vuoi crearne uno nuovo? (y/n)\n")

        # se scegli di creare un nuovo profilo utente
        if choose == "y":
            pw = input("Inserisci la password: ")
            r.set(nome_utente, pw)
        else:
            print('https://www.youtube.com/watch?v=TGgcC5xg9YI&ab_channel=Tyler%2CTheCreator\nSEE YOU AGAIN!')
