# Route resolver
## Simple LPM API

I hope you enjoy this test project.
I modified a bit your docker file, and docker compose file, and slightly your tests(just changed port and endpoint to make work it through nginx)

The orignial file shall include .env file in infra directory bu anyway, make sure that .env file persists and properly populated

## Install
Clone github repository
```bash
git clone https://github.com/gapa64/route_resolver
cd route_resolver/infra/
```
Create .env file
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
To start a project with compose please navigate run this command from route_resolver/infra/ directory
```bash
docker compose up 
```

Hope you enjoy this project!