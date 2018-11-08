# Run tests and application

## With docker

- run tests
```bash
docker-compose --file docker-compose_tests.yml up --build 
```
- run application
```bash
docker-compose up --build
```

## Without docker

- create virtualenv
```bash
virtualenv -p python3.6 ven
```
- launch virtualenv
```bash
source venv/bin/activate
```
- install requirements
```bash
pip install -r requirements.txt
```
- export environment variables
```bash
export APP_ENV=DEV
export APP_PORT=8080
```
- up database (test database in example, but you can up any postgres db on port 5432 and with name, login and pass from conf.py file)
```bash
docker-compose --file docker-compose_tests.yml up postgres_test
```
- run tests (with coverage)
```bash
bash test_coverage.sh
```
- run application
```bash
python run.py
```

# How it works

There are 3 api endpoints:
- **/user** for user creation
- **/login** for login
- **/config** endpoint from the task

Endpoint methods and parameters you can get from the postman file 'twyla.postman_collection.json'

I made this service with aiohttp and postgres. As driver for postgres I use aiopg. 
No one non-blocking driver for Postgres doesnt support ORM (and ORM layer of SQLAlchemy too). 
That's why I used core layer of SQLAlchemy and my own model classes for work with database. 
It is enough abstract too and sometimes it is more flexible.

I completed bonus task about security. I implemented authorization for it and access to endpoints by token. 
It appends else one requirement parameter *'token'* to API. 

For load testing I can use any load tools for web services (Apache JMeter, for example) or write simple load tester with aiohttp clienside (just api shooter). Anyway I have to add logs for start and end of I/O operations and put it somewhere, where I can analise it later (cache; database, where I can write with queue; Elastic; etc.)

Alternative solution. Of course Python is not the fastest language ever, but in the current solution we don't have any CPU-bound problem. We can use Go or something else for it, but performance will not increase.
All our tasks are I/O-bound. It is read and write to database. To make it faster we can use cache or in-memory database. 
I guess key-value cache is enough, and as keys we will use composite of "tenant" and "integration_type", after every read we can put in to cache for N minutes, and after every update, if entity is in cache we will update it there too.
