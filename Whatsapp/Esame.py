import redis
import redisfunc 

# connessione a Redis cloud
r = redisfunc.connessioneCloud()


print("Benvenuto su AAAAAAAAAtsapp la nota app di SCONTRI!")

# se scegli di accedere
while True:
    accesso = input("Scrivi ACCEDI per entrare nel nostro sito.\n - ")
    
    if accesso == "ACCEDI":
     nome_user = input('Inserisci il nome utente del tuo account: ')
     password = input('Inserisci la password del tuo account: ')
     redisfunc.ACCESSO(r, nome_user, password)
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
#ho creato un set con solo i nomi degli utenti, cerca l'input con ismember, se lo trova stampa l'username (quello cercato)
#se no dice che non esiste

    if choose == "1":
        cerca = input('Chi stai cercando? ')
        result = r.sismember('Utenti:Nomi', cerca)
        
        if result:
            print(f'Utente trovato: {cerca}')
        else:
            print('L\'utente non esiste')
        
        
    # 2 - scelta Aggiungi amico
#ho creato nella f(x) registrazione un secondo set per lo storing degli utenti, all'inizio cerco se l'utente
#cercato esiste, se sì result lo aggiunge al set contatti:nome_utente, se conferma (elif) passa dovrebbe invece
#stampare  che è gia presente, se no non esiste in generale

    elif choose == "2":
        cerca = input('Scrivi l\'username di vuoi aggiungere fra i contatti: ')
        result = r.hget('Utenti', cerca)
        conferma = r.sismember(f'Contatti:{nome_user}', cerca)
        
        if result:
            print('Utente aggiunto ai tuoi amici!\nCerca aggiunto fra i tuoi contatti.')
            r.sadd(f'Contatti:{nome_user}', cerca)
        
        elif conferma:
            print('L\'utente è gia parte dei tuoi contatti!')
        
        else:
            print('L\'utente non esiste!')


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





    
    
