Per il corretto funzionamento del file è necessario seguire i prossimi step:

1.	Assicurarsi di aver installato python 3.12
2.	Installare in un ambiente virtuale le seguenti librerie:
    -	redis
    -	pandas
    -	colorama
    -	pyfiglet
    -	termcolor
3.	Registrarsi nel database Redis tramite codice mandando in run il main (Esame_finale.py)

Nel repository sono presenti due file:
    - (Esame_finale.py)
    - (redisfunc.py)

Il funzionamento è molto semplice, basterà runnare il codice dal (main) e apparirà il nome dell’app con la richiesta di inserire nome utente e password.
Nel caso in cui l’utente esistesse già:
-	Se la password verrà inserita correttamente si accederà all’app.
-	In caso di password errata apparirà un messaggio di errore (e verranno chiesti nuovamente nome utente e password).
Nel caso in cui l’utente non fosse già registrato:
-	Verrà richiesta la registrazione (in caso di mancata conferma l’applicazione si chiuderà, altrimenti verrà eseguito l’accesso all’app).

Una volta all’interno dell’app verrà stampata una lista con le possibili azioni effettuabili; apparirà inoltre un messaggio in alto per ricordare all’utente lo stato del suo profilo (modalità do not disturb ON/OFF)

LISTA AZIONI

1 – Cerca utente: l’utente può ricercarne altri attraverso l’azione ‘Cerca utente’ selezionabile scrivendo ‘1’ in input.
Questa funzione cercherà nel set degli utenti di Redis (nel quale sono immagazzinati tutti i nomi utente) un match fra l’input e i nomi, creando un dataframe con Pandas e operandoci sopra, fornendo anche match parziali.

Es.
Input: ‘Gianni’		Output: Gianni12, GianniniFabrizio, Gianni, GianniMa57

Nel caso la funzione non trovasse nessun match manderà in output un messaggio di errore.
Attenzione: la funzione è case sensitive

2 – Lista amici: la funzione restituirà come output la lista amici dell’utente 
Se la lista degli amici dell’utente è vuota restituirà “ “

3 – Aggiungi amico: la funzione permetterà di aggiungere un utente alla propria lista amici. (i nomi dei quali saranno salvati all’interno di un apposito set).
Se l’utente non esiste verrà stampato un messaggio di errore.

4 – Do Not Disturb: la funzione permetterà di cambiare il proprio stato e passare dalla modalità DnD OFF a quella ON (e viceversa)
Lo stato verrà indicato a schermo con un on e off, nel caso sia ON l’utente non potrà essere contattato

5 – Apri Chat: la funzione permetterà di aprire una chat (esistente o meno) con un amico. Verrà chiesto all’utente di indicare il nome del contatto col quale messaggiare, in seguito si avrà la possibilità di scegliere se avviare una chat permanente o effimera.

Nel caso in cui l’utente ricercato: 
-	non dovesse esistere 
-	non dovesse essere amico dell’utente
-	dovesse essere in modalità DnD ON
apparirà a schermo un messaggio di errore.
Nel caso in cui non dovessero esserci problemi si aprirà la chat:
-	se l’utente avrà scelto di avviare una chat normale, i messaggi verranno salvati in un sorted set permanente.
-	se l’utente avrà scelto di avviare una chat effimera, i messaggi verranno salvati in un sorted set che si autodistruggerà dopo un minuto dall’ultimo messaggio inviato da uno dei due membri (eliminando la chat)

6 – Elimina amico: la funzione permette di rimuovere un amico dalla lista amici dell’ utente

7 – Mostra chat: la funzione stampa a schermo tutte le chat attive dell’user
Attenzione: le chat effimere non verranno contate come tali, dato che in caso d’inattività verranno cancellate dopo 60 secondi

8 – Esci: permette all’utente di chiudere il programma

