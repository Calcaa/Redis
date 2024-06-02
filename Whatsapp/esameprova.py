import redis
import redisfunc

# terminale ####################################
import pyfiglet as p
from colorama import init, Fore, Back, Style 
from termcolor import colored
init(autoreset=True)
#################################################



# connessione a Redis cloud
r = redisfunc.connessioneCloud()

TITOLO = p.figlet_format("faketsapp", font="slant")
print(Fore.RED + Style.BRIGHT + TITOLO)


# se scegli di accedere
while True:
         
    nome_user = input("Inserisci il" + (Fore.RED + " nome utente  ") + (Style.RESET_ALL + "del tuo account: "))
    password = input("Inserisci la" + (Fore.RED + " password 🔒 ") + (Style.RESET_ALL + "del tuo account: "))
    
    if redisfunc.ACCESSO(r, nome_user, password):
        break

while True:
    
    if r.hget("DND", nome_user) == "0":
        print("\n☀️ Do not disturb: " + (Fore.RED + "OFF"))
    
    else:
        print("\n💤 Do not disturb: " + (Fore.GREEN + "ON"))
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
        contatto = input("Chi vuoi cercare? 🔍 ")
        
        if redisfunc.controllaContatto(r, contatto):
            choose = input("L'utente che hai cercato " + (Fore.GREEN + "esiste ") + (Style.RESET_ALL + "\n\nVuoi aggiungere questo utente ai tuoi contatti? ") + (Fore.GREEN + "y") + (Style.RESET_ALL + "/") + (Fore.RED + "n\nScelta: "))
            
            if choose.lower() == "y":
                redisfunc.aggiungiContatto(r, nome_user, contatto)
        
        else:
            print("L'utente che hai cercato " + (Fore.RED + "non esiste!"))
    
    # 2 - stampa amici 
    elif choose == "2":
        print(Fore.YELLOW + "I tuoi amici: ")
        
        for amici in r.smembers(f"Amici:{nome_user}"):
            print(amici)
        
    # 3 - scelta Aggiungi amico
    elif choose == "3":
        cerca = input("\nScrivi l'username di chi vuoi " + (Fore.GREEN + "aggiungere ") + (Style.RESET_ALL + "ai tuoi contatti: "))
        result = r.hget("Utenti", cerca)
        conferma = r.sismember(f"Amici:{nome_user}", cerca)

        if result:
            
            if conferma:
                print(Fore.YELLOW + "L'utente fa già parte dei tuoi contatti!")
            
            else:
                redisfunc.aggiungiContatto(r, nome_user, cerca)
                r.sadd(f"Amici:{nome_user}", cerca)
        
        else:
            print(Fore.RED + "L'utente non esiste!")


    # 4 - scelta Do Not Disturb
    elif choose == "4":
        redisfunc.DoNotDisturb(r, nome_user)

    #5 - scelta apri chat
    elif choose == "5":
        #print('Chat esistenti:')
        destinatario = input(Fore.YELLOW + "a chi vuoi scrivere? ")
        
        try:
            risposta = input("Desideri aprire una chat " + (Fore.LIGHTCYAN_EX + "effimera? 🕑 ") + (Fore.GREEN + "y") + (Style.RESET_ALL + "/") + (Fore.RED + "n "))
            
            if risposta.lower() == "y":
                effimera = True     
            
            else:
                effimera = False    
        
        except ValueError:
            
            print(Fore.RED + "errore")
        
        # reverse True per visualizzare i mess dal più recente al meno recente, altrimenti False per visualizzazione al contrario
        redisfunc.Chat(r, nome_user, destinatario, effimera, reverse = True)
    
    #6 - elimina amico
    elif choose == "6":
        redisfunc.EliminaAmico(r,nome_user)
    
    #7 - mostra tutte le mie chat
    elif choose == "7":
        redisfunc.MostraChat(r,nome_user)
    
    #8 - esci, da implementare anche nel 5
    elif choose == "8":
        print(Fore.YELLOW + "bye bye")
        break
