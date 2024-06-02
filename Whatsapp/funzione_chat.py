import redis
from sys import exit
from time import sleep
import redisfunc

r = redisfunc.connessioneCloud()

def Chat(r : redis, nome_utente : str, destinatario : str, effimera : bool):
    if r.sismember(f"Amici:{nome_utente}", destinatario):
        if r.hget("DND", destinatario) == '0':
                listaNomi = [nome_utente, destinatario]
                chiaveNomi = "".join(sorted(listaNomi))

        else: 
            print("Errore: L'utente ha la modalita' non disturbare attiva")
    else: 
        print("Il contatto non e' tuo amico")







"""
notifica = "mado"
pubsub = r.pubsub()
pubsub.psubscribe(**{"utenti:registrazioni": notifica})
r.publish("utenti:registrazioni", "marco")
pubsub.run_in_thread(sleep_time=0.01)
"""
"""
r.publish("utenti:registrazioni", "marco")
"""



