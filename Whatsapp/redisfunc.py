import redis

# Connessione a Redis
def cloudConnect() -> redis:
    try:
        r = redis.Redis(host="redis-11521.c135.eu-central-1-1.ec2.redns.redis-cloud.com", port=11521, password="sUaEw4HsesMiuONu3MURRZvuUDLqXeEi", db=0, decode_responses=True)
        print(f"Stato db: {r.ping()}")
        print("Connessione a redis in locale riuscita!")
        return r
    except redis.ConnectionError:
        print("Devi avviare Docker e runnare il container con Redis!")
        exit()