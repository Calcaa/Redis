import redis
from sys import exit
from datetime import date, datetime
try:
    r = redis.Redis(host="redis-11521.c135.eu-central-1-1.ec2.redns.redis-cloud.com", port=11521, password="sUaEw4HsesMiuONu3MURRZvuUDLqXeEi", db=0, decode_responses=True)
    print(f"Stato db: {r.ping()}")
    print("Connessione a redis in locale riuscita!")
except redis.ConnectionError:
    print("Devi avviare Docker e runnare il container con Redis!")
    exit()


ora = datetime.now()
ora = ora.strftime("[%d/%m/%Y - %H:%M:%S]")

print(ora)