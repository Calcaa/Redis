import redis
from sys import exit
from datetime import date, datetime
import pandas as pd
try:
    r = redis.Redis(host="redis-11521.c135.eu-central-1-1.ec2.redns.redis-cloud.com", port=11521, password="sUaEw4HsesMiuONu3MURRZvuUDLqXeEi", db=0, decode_responses=True)
    print(f"Stato db: {r.ping()}")
    print("Connessione a redis in locale riuscita!")
except redis.ConnectionError:
    print("Devi avviare Docker e runnare il container con Redis!")
    exit()


membri = r.smembers('Utenti:Nomi')
membri = list(membri)

df = pd.DataFrame(membri, columns=['Utenti'])
i = input('cosa cerchi?')

df = df[df['Utenti'].apply(lambda x: x.startswith(i))]

for element in df['Utenti']:
    print(element)
