import redis
from sys import exit

# Connessione a Redis
try:
    r = redis.Redis(host="redis-11521.c135.eu-central-1-1.ec2.redns.redis-cloud.com", port=11521, password="sUaEw4HsesMiuONu3MURRZvuUDLqXeEi", db=0, decode_responses=True)
    print(f"Stato db: {r.ping()}")
    print("Connessione a redis in locale riuscita!")
except redis.ConnectionError:
    print("Devi avviare Docker e runnare il container con Redis!")
    exit()



cerca = input('Chi stai cercando')
result = r.hget('Utenti', cerca)
print(result)
if not result:
    print('L\'utente non esiste')
else:
    print('trovato un utente')