import funzioni 
import os
import keyboard
import threading

# os.system('cls') per pulire alla fine
# connessione a Redis cloud
r = funzioni.connessioneCloud()


print("Benvenuto su AAAAAAAAAtsapp la nota app di SCONTRI!\n")

# se scegli di accedere
while True:
    accesso = input("Scrivi ACCEDI per entrare nel nostro sito.\n - ")
    
    if accesso.upper() == "ACCEDI":
     nome_user = input('Inserisci il nome utente del tuo account: ')
     password = input('Inserisci la password del tuo account: ')
     funzioni.ACCESSO(r, nome_user, password)
     os.system('cls')
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
        if funzioni.controllaContatto(r, contatto):
             print("Il contatto che hai cercato esiste")
        else:
            print('Il contatto che hai cercato non esiste!')
    
    # 2 - stampa amici 
    elif choose == "2":
        for amici in r.smembers(f'Amici:{nome_user}'):
            print(amici)
        
    # 3 - scelta Aggiungi amico
    elif choose == "3":
        cerca = input('Scrivi l\'username di chi vuoi aggiungere fra i contatti: ')
        result = r.hget('Utenti', cerca)
        conferma = r.sismember(f'Amici:{nome_user}', cerca)

        if result:
            if conferma:
                print('L\'utente è già parte dei tuoi contatti!')
            else:
                funzioni.aggiungiContatto(r, nome_user, cerca)
                r.sadd(f'Amici:{nome_user}', cerca)
        else:
            print('L\'utente non esiste!')


    # 4 - scelta Do Not Disturb
    elif choose == "4":
        funzioni.DoNotDisturb(r, nome_user)

    #5 - scelta apri chat
    elif choose == "5":
        #print('Chat esistenti:')
        destinatario = input('A chi vuoi scrivere?\nScelta: ')
        try:
            risposta = input("Desideri che la chat sia effimera? y/n\n")
            effimera = risposta.lower() == 'y'
        except ValueError:
            print('err')

        listaNomi = [nome_user, destinatario]
        chiaveNomi = "".join(sorted(listaNomi))
        
        t = threading.Thread(target=funzioni.ascolta_chat, args=(r, chiaveNomi, nome_user))
        t.start()
        #funzioni.ascolta_chat(r, chiaveNomi, nome_user) 
        
        while True:
            messaggio = input("\nMessaggio: ")
            if messaggio.lower() == 'esc':
             break
            funzioni.invia_messaggio(r, chiaveNomi, nome_user, messaggio, effimera, destinatario)  # Invio del messaggio

    
    #6 - elimina amico
    elif choose == "6":
        funzioni.EliminaAmico(r,nome_user)
    
    #7 - mostra tutte le mie chat
    elif choose == "7":
        funzioni.MostraChat(r,nome_user)
    
    #8 - esci, da implementare anche nel 5
    elif choose == "8":
                print('bye bye')
                break
    
    
    #mancano datastamps, la chat non rimane aperta, il clear del terminal, notifiche