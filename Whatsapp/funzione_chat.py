import redis
from sys import exit
import time
import redisfunc
from datetime import datetime

r = redisfunc.connessioneCloud()

# Funzione di chat
def Chat(r : redis, nome_utente : str, destinatario : str, effimera : bool, reverse : bool):

    

        # Funzione che stampa i mess con > e <
        def leggiChat(r : redis, chiaveNomi, nome_utente, destinatario, reverse):

            # visualizzazione dal mess meno recente al più recente
            if reverse == False:
                messaggi = r.zrange(chiaveNomi,0,-1)

            # visualizzazione dal mess più recente al meno recente
            else:
                messaggi = r.zrevrange(chiaveNomi,0,-1)

            print(f"\u001b[96m>> Chat con {destinatario} <<\n\u001b[37m(scrivi \u001b[93msys exit\u001b[37m se intendi tornare al menù)\n")
            
            # per ogni messaggio scrive > se il messaggio appartiene al mittente, altrimenti <
            for messaggio in messaggi:
                parti = messaggio.split(":")
                mittente = parti[0].strip()
                if mittente == nome_utente:
                    print(f"> {messaggio}")
                else:
                    print(f"< {messaggio}")
            
        
        # cerca se l'utente è tra gli amici
        if r.sismember(f"Amici:{nome_utente}", destinatario):
            if r.hget("DND", destinatario) == '0':
                    
                    # crea la chiave del sorted set unendo i nomi dei due utenti in chat
                    listaNomi = [nome_utente, destinatario]
                    chiaveNomi = "".join(sorted(listaNomi))
                    
                    # riporta i messaggi della tipologia di chat (effimera e non)
                    if effimera == False:
                        leggiChat(r, chiaveNomi, nome_utente, destinatario, reverse)
                    else: 
                        leggiChat(r, f"Effimera:{chiaveNomi}", nome_utente, destinatario, reverse)
                    
                    # inizio ciclo di scrittura mess
                    while True:

                        # richiesta input mess
                        messaggio = input("\u001b[1mMessaggio: ")

                        # pulisce il terminale ad ogni invio
                        redisfunc.PulisciTerminale()

                        # se l'utente scrive sys exit esce dal ciclo
                        if messaggio.lower() == "sys exit":
                            break
                        
                        # se l'utente scrive qualcosa
                        elif messaggio != "":
                            
                            # se la chat è effimera viene creato il sorted set per chat effimera in cui vengono salvati i mess
                            if effimera == True:
                                r.zadd(f"Effimera:{chiaveNomi}", {f"{nome_utente}: {messaggio}           [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]":time.time()})
                                r.expire(f"Effimera:{chiaveNomi}",60)

                                # vengono ristampati i messaggi
                                leggiChat(r, f"Effimera:{chiaveNomi}", nome_utente, destinatario, reverse)
                            
                            # se la chat non è effimera viene creato il sorted set per chat normale in cui vengono salvati i mess
                            else:
                                r.zadd(chiaveNomi, {f"{nome_utente}: {messaggio}           [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]":time.time()})
                                r.sadd(f"Chat{nome_utente}",f"Chat Con {destinatario}")

                                # vengono ristampati i messaggi
                                leggiChat(r, chiaveNomi, nome_utente, destinatario, reverse)

            # se il destinatario ha la modalità DnD attiva                   
            else: 
                print("Errore: L'utente ha la modalita' non disturbare attiva")
        
        # se il destinatario non è amico
        else: 
            print("Il contatto non e' tuo amico")

   

Chat(r,"Manu","gianni",True,True)




