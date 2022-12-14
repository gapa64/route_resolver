## Route resolver
### simple LPM API

I hope you enjoy this test project.
I modified a bit your docker file, and docker compose file, and slightly your tests(just changed port and endpoint to make work it through nginx)

The orignial file shall include .env file in infra directory bu anyway, make sure that .env file persists and properly populated
Env
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
To start a project with compose please navigate to infra directory and start.
```bash

cd infra
docker compose up 
```

Hope you enjoy this project!