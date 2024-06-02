import redis
import redisfunc 
import funzione_chat

# connessione a Redis cloud
r = redisfunc.connessioneCloud()


print("\n\u001b[37mBenvenuto su AAAAAAAAAtsapp la nota app di SCONTRI!\n")

# se scegli di accedere
while True:
    accesso = input("\u001b[37mScrivi \u001b[92mACCEDI \u001b[37mper entrare nel nostro sito.\n - ")
    
    if accesso.upper() == "ACCEDI":
         
        nome_user = input('Inserisci il \u001b[92mnome utente \u001b[37mdel tuo account: ')
        password = input('Inserisci la \u001b[92mpassword \u001b[37mdel tuo account: ')
        redisfunc.ACCESSO(r, nome_user, password)
        # CORREGGERE QUESTA PARTE, SE SI SBAGLIA LA PSW NON SI DEVE AVERE ACCESSO
        break

while True:
    if r.hget('DND', nome_user) == '0':
        print('\n\u001b[92mDo not disturb: OFF')
    else:
        print('\n\u001b[91mDo not disturb: ON')
        #da implementare il blocco messaggi

    choose = input(
                f"\n\n\u001b[93mCosa vuoi fare?\u001b[37m\n\n"
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
            print('Il contatto che hai cercato non esiste!')
    
    # 2 - stampa amici 
    elif choose == "2":
        print("\n\u001b[93mI tuoi amici:\u001b[37m\n")
        for amici in r.smembers(f'Amici:{nome_user}'):
            print(amici)
        
    # 3 - scelta Aggiungi amico
    elif choose == "3":
        cerca = input('\nScrivi l\'username di chi vuoi \u001b[93maggiungere\u001b[37m ai tuoi contatti: ')
        result = r.hget('Utenti', cerca)
        conferma = r.sismember(f'Amici:{nome_user}', cerca)

        if result:
            if conferma:
                print('\n\u001b[91mL\'utente fa già parte dei tuoi contatti!\u001b[37m')
            else:
                redisfunc.aggiungiContatto(r, nome_user, cerca)
                r.sadd(f'Amici:{nome_user}', cerca)
        else:
            print('\n\u001b[93mL\'utente non esiste!\u001b[37m')


    # 4 - scelta Do Not Disturb
    elif choose == "4":
        redisfunc.DoNotDisturb(r, nome_user)

    #5 - scelta apri chat
    elif choose == "5":
        #print('Chat esistenti:')
        destinatario = input('\n\u001b[93ma chi vuoi scrivere?\n\u001b[37mScelta: ')
        
        try:
            risposta = input("Desideri aprire una chat \u001b[93meffimera\u001b[37m? y/n\n")
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
                print('\u001b[93mbye bye')
                break
    
    

    
    
