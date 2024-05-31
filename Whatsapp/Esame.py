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
        print('\nDo not disturb: OFF')
    else:
        print('\nDo not disturb: ON')
        #da implementare il blocco messaggi

    choose = input(
                f"\n\nCosa vuoi fare?\n"
                f"1 - Cerca utente\n"
                f"2 - Lista amici\n"
                f"3 - Aggiungi amico\n"
                f"4 - Do Not Disturb\n"
                f"5 - Apri chat\n"
                f"6 - Elimina Amico\n"
                f"7 - Mostra tutte le chat aperte\n"
                f"8 - Esci\n\n"
                f"Scelta: ")
    
    # 1 - scelta Cerca utente
#ho creato un set con solo i nomi degli utenti, cerca l'input con ismember, se lo trova stampa l'username (quello cercato)
#se no dice che non esiste

    if choose == "1":
        contatto = input('Chi vuoi cercare?\nScelta: ')
        if redisfunc.controllaContatto(r, contatto):
             print("Il contatto che hai cercato esiste")
        else:
            print('Il contratto che hai cercato non esiste!')
    
    # 2 - stampa amici 
    elif choose == "2":
        for amici in r.smembers(f'Contatti:{nome_user}'):
            print(amici)
        
    # 3 - scelta Aggiungi amico
    elif choose == "3":
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


    # 4 - scelta Do Not Disturb
    elif choose == "4":
        redisfunc.DoNotDisturb(r, nome_user)

    #5 - scelta apri chat
    elif choose == "5":
        #print('Chat esistenti:')
        destinatario = input('a chi vuoi scrivere?\nScelta: ')
        
        try:
            risposta = input("Desideri che la chat sia effimera? y/n")
            if risposta.lower() == 'y':
                effimera = True     
            else:
                effimera = False    
        except ValueError:
            
            print('err')
        redisfunc.ApriChat(r, nome_user, destinatario, effimera)
    
    #6 - elimina amico
    elif choose == "6":
        redisfunc.EliminaAmico(r,nome_user)
    
    #7 - mostra tutte le mie chat
    elif choose == "7":
        redisfunc.MostraChat(r,nome_user)
    
    #8 - esci, da implementare anche nel 5
    elif choose == "8":
                print('bye bye')
                break

    
    
