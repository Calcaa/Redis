import redis as r

'''
Obiettivo:
realizzare un applicazione CLI Python che gestisca il processo di votazione di proposte da parte degli studenti
Utilizzare Redis come database

L app Python deve permettere di caricare le proposte
Ogni proposta ha un proponente
Ogni studente può votare tutte le proposte che vuole, ma al massimo un voto per proposta
In ogni momento l applicazione può mostrare la lista delle proposte ordinate per numero di voti

'''
#aprite docker e create un container chiamato db di redis, con la porta 6379, passo cruciale o ciuccia
#avere python 3.12.1

db = r.Redis(host='localhost', port=6379, db=0, decode_responses=True)

ping_status = db.ping()
print("Ping Status: ", ping_status)