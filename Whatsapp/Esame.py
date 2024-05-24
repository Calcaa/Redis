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
    
    # 1 - scelta aggiunta proposta
    if choose == "1":
        cerca = input('Chi stai cercando')
        result = r.hget('Utenti')

            # 2 - scelta voto proposta
    elif choose == "2":
                pass

            # 3 - scelta lettura proposte
    elif choose == "3":
                pass

    elif choose == "4":
                pass
                    
    elif choose == "5":
                print('bye bye')
                break





    
    
