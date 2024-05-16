import redis
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

print(f"Stato db: {r.ping()}")
#r.set("stocazzo", "1234")
print(f"Benvenuto, come prima cosa dimmi chi cazzo sei")
nome_utente =input("Nome utente: ")

pw_utente = r.get(nome_utente)
if pw_utente:
    pw = input("Password: ")

    if pw == pw_utente:
        print(f"Benvenuto {nome_utente}\n")

        while True:
            choose = input(f"\n\nCosa vuoi fare?\n1 - Aggiungi proposta\n2 - Vota Proposta\n3 - Visualizza proposte\n\nScelta: ")

            if choose == "1":
                nome_proposta = input("Nome proposta: ")
                descrizione_proposta = input("Descrizione: ")

                r.set(f"Proposte:{nome_proposta}", f"{descrizione_proposta}")

            elif choose == "2":
                nome_proposta = input("Che proposta vuoi votare?\nNome: ")

                if r.get(nome_proposta):
                    if not r.get(f"{nome_utente}:Voti:{nome_proposta}"):
                        r.incr(f"Voti:{nome_proposta}")
                        r.set(f"{nome_utente}:Voti:{nome_proposta}", 1)
                    else:
                        print(f"Abbello, hai gia votato sta proposta... fatte un giro")
                else:
                    print("Nooonnn Iesiìììstie")

            elif choose == "3":
                """proposte = r.get(f"Voti:")
                print(proposte)"""
                #Non funzica

    else:
        print("Coglione non ti ricordi la password")
else:
    choose = input("Vuoi creare un nuovo utente? (y/n)\n")

    if choose == "y":
        pw = input("Inserisci la password")
        r.set(nome_utente, pw)
