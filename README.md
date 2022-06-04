# test_fastapi

link to doc
http://fastapi.localhost:8008/docs or
http://fastapi.localhost:8008/redoc

link to traefik
http://fastapi.localhost:8081/dashboard/#/


see func
curl -s fastapi.localhost:8008/ping | jq
```json
{
  "ping": "pong!"
}
```

run tests

docker-compose exec web pytest .

## content of .env in root_dir
```json
COMPOSE_FILE=base.yml
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_DB=...
```


for development
on local machine - *pip install pre-commit* and *pre-commit install* in root dir
