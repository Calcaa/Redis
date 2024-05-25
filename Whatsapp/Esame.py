import redis
import redisfunc 

# connessione a Redis cloud
r = redisfunc.connessioneCloud()


print("Benvenuto su AAAAAAAAAtsapp la nota app di SCONTRI!")
accesso = input("Scrivi ACCEDI se possiedi già un account, altrimenti REGISTRATI.")

# se scegli di accedere
while True:
    if accesso == "ACCEDI":
     nome = input('Inserisci il nome utente del tuo account: ')
     password = input('Inserisci la password del tuo account: ')
     redisfunc.ACCESSO(r, nome, password)
     break
 

while True:
    choose = input(
                f"\n\nCosa vuoi fare?\n"
                f"1 - Cerca utente\n"
                f"2 - Aggiungi amico\n"
                f"3 - Do Not Disturb\n"
                f"4 - Apri chat\n"
                f"5 - Esci\n\n"
                f"Scelta: ")
    
    # 1 - scelta Cerca utente
#vorrei prendere in input ciò he vuole cercare, poi hkeys per avere i values (tutti i nomi utenti) e cercare con pandas tutti i valori simili
    if choose == "1":
        cerca = input('Chi stai cercando')
        result = r.hget('Utenti')
        

    # 2 - scelta Aggiungi amico
#una semplice aggiunta del amico con zset(), if else per verificare l'esistenza
    elif choose == "2":
                pass

    # 3 - scelta Do Not Disturb
#semplicemente una variabile in python, quando i = 1 non passano i messaggi (implementiamo un elif i = 1: pass tipo)
    elif choose == "3":
                pass

    #4 - scelta apri chat
#penso un if che controlla l'esistenza, se non la trova crea la chat, all'interno della chat la funzione async? e la possibilità di scrivere messaggi 
    elif choose == "4":
                pass
          
    #5 - esci, da implementare anche nel 4 (lascerei la chat aperta fino a che schiacciano 5)
    elif choose == "5":
                print('bye bye')
                break





    
    
