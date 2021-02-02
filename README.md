## Django Rest Scraper:

Endpoint per lo scraping delle prime n pagine fornite all'endpoint in ingresso e che salva tutto in Database in modo asincrono.
http://127.0.0.1:8000/scraper/ method=POST data={"pages": integer}

CRUD completo sui singoli articoli.

Endpoint che listi tutti gli articoli salvati in 3 diversi modi in base ad un parametro in ingresso: per autore, per categoria, lista completa.
http://127.0.0.1:8000/articles/
http://127.0.0.1:8000/articles/?category=adventure&author=pippo


Testing basilare delle API tramite Unit Testing.
Django Rest Framework APITestCase


Un logger che logghi tutte le richieste in entrata sul server.
access.log

Celery Log per monitorare i progressi dello scraping:
celery.log

Containerizzazione del server tramite Docker:
Realizzata con Docker e docker-compose (vedi docker_guide.txt)

Documentazione dei singoli endpoint.
http://127.0.0.1:8000/swagger/

## Tecnologie utilizzate:

Django 3 

Django ORM

Django rest framework

django rest framework pagination (vedi settings.py)

django filters (filtri) /articles/?category=adventure&author=pippo

requests-html (scraping con supporto js)

celery (job asincroni)

MongoDB (with djongo Object DB Mapper)

Django Rest Framework APITestCase

Logger django

Docker, docker-compose

Swagger (documentazione e test) http://127.0.0.1:8000/swagger/
