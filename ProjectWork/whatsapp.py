import redis

#sUaEw4HsesMiuONu3MURRZvuUDLqXeEi
#default


redis_host = "redis-11521.c135.eu-central-1-1.ec2.redns.redis-cloud.com"

# Connessione al database Redis
r = redis.Redis(host=redis_host, port=11521, password="sUaEw4HsesMiuONu3MURRZvuUDLqXeEi",db = 0, decode_responses=True)  # Decodifica le risposte in stringhe



def messaggio():
    pass