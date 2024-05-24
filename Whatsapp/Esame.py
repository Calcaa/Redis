import redis
import redisfunc 

# connessione a Redis cloud
r = redisfunc.connessioneCloud()


print("Benvenuto su AAAAAAAAAtsapp la nota app di SCONTRI!")
accesso = input("Scrivi ACCEDI se possiedi già un account, altrimenti REGISTRATI.")

# se scegli di accedere
while True:
    if accesso == "ACCEDI":
     redisfunc.ACCESSO()
     break
 
# se scegli di registrarti
    elif accesso == "REGISTRATI":
        redisfunc.registrazione()
        break

while True:
    choose = input(
                f"\n\nCosa vuoi fare?\n"
                f"1 - Aggiungi proposta\n"
                f"2 - Vota Proposta\n"
                f"3 - Visualizza proposte\n"
                f"4 - Visualizza voti\n"
                f"5 - Esci\n\n"
                f"Scelta: ")





    
    
