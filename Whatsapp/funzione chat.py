import redis
from sys import exit
import time

def Chat(r : redis, nome_utente : str, destinatario : str, effimera : bool):
    destinatario = input("A chi vuoi scrivere?")
    if r.sismember(f"Amici:{nome_utente}", destinatario):
        if r.hget("DND", destinatario) == '0':
                listaNomi = [nome_utente, destinatario]
                chiaveNomi = "".join(sorted(listaNomi))
        else: 
            print("Errore: L'utente ha la modalita' non disturbare attiva")
    else: 
        print("Il contatto non e' tuo amico")

