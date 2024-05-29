import redis
import redisfunc 

# connessione a Redis cloud
r = redisfunc.connessioneCloud()


print("Benvenuto su AAAAAAAAAtsapp la nota app di SCONTRI!")

# se scegli di accedere
while True:
    accesso = input("Scrivi ACCEDI per entrare nel nostro sito.\n - ")
    
    if accesso.upper() == "ACCEDI":
     nome_user = input('Inserisci il nome utente del tuo account: ')
     password = input('Inserisci la password del tuo account: ')
     redisfunc.ACCESSO(r, nome_user, password)
     break
 

while True:
    if r.hget('DND', nome_user) == '0':
        print('Do not disturb: OFF')
    else:
        print('Do not disturb: ON')
        #da implementare il blocco messaggi

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
        contatto = input('Chi vuoi cercare?\nScelta: ')
        if redisfunc.controllaContatto(r, contatto):
             print("il contatto che hai cercato esiste")
        
        
    # 2 - scelta Aggiungi amico
#ho creato nella f(x) registrazione un secondo set per lo storing degli utenti, all'inizio cerco se l'utente
#cercato esiste, se sì result lo aggiunge al set contatti:nome_utente, se conferma (elif) passa dovrebbe invece
#stampare  che è gia presente, se no non esiste in generale


    elif choose == "2":
        cerca = input('Scrivi l\'username di chi vuoi aggiungere fra i contatti: ')
        result = r.hget('Utenti', cerca)
        conferma = r.sismember(f'Contatti:{nome_user}', cerca)

        if result:
            if conferma:
                print('L\'utente è già parte dei tuoi contatti!')
            else:
                redisfunc.aggiungiContatto(r, nome_user, cerca)
                r.sadd(f'Contatti:{nome_user}', cerca)
        else:
            print('L\'utente non esiste!')


    # 3 - scelta Do Not Disturb
#semplicemente una variabile in python, quando i = 1 non passano i messaggi (implementiamo un elif i = 1: pass tipo)
    elif choose == "3":
        redisfunc.DoNotDisturb(r, nome_user)

    #4 - scelta apri chat
#penso un if che controlla l'esistenza, se non la trova crea la chat, all'interno della chat la funzione async? e la possibilità di scrivere messaggi 
    elif choose == "4":
        print('Chat esistenti:')
        
        destinatario = input('a chi vuoi scrivere?\nScelta: ')
        redisfunc.ApriChat(r, nome_user, destinatario) #da modificare
          
    #5 - esci, da implementare anche nel 4 (lascerei la chat aperta fino a che schiacciano 5)
    elif choose == "5":
                print('bye bye')
                break


#dobbiamo stampare le chat esistenti
#stampare la cronologia della chat
#proviamo a vedere publish e spublish
#5 per chiudere la chat  e riportarlo al menù principale


    
    
