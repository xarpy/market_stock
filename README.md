# Cial StockAPI Challenges

[![Python Version][python-image]][python-url]
[![FastAPI Version][fastapi-image]][fastapi-url]


A API based on fastapi with purpose to scrapping data from MarketWatch

## Installation

### Environment Local

Using your dependency manager, create a python environment, follow a [link](https://ahmed-nafies.medium.com/pip-pipenv-poetry-or-conda-7d2398adbac9) talking about the managers!

Access the project folder and using the **pip** manager, inside the python env, apply the command below:

Upgrade pip version and install requirements and install:

```sh
pip install --upgrade pip && pip install --require-hashes -r requirements/dev.txt
```

And now can run the api, just use the command below:
```sh
python manage.py runserver
```

### Docker Build

You will need to have docker compose, and finally apply the command:

```sh
docker compose up --build
```

**Obs:**

* Don't forget to manually create a folder named logs at the root of the project. Otherwise, it will fail to deploy the application;
* When project run by docker, don't forget to change reference keys, like POSTGRES_HOST and REDIS_HOST for the correctly values;
* If the build is done through the docker and then you try to run the application locally, it will be necessary to grant read and write permission to the file `error.log`;
* To use or test the cache service with Redis, we can use, in docker-compose.yml we build a container using one of the main information monitoring systems in the Redis database, called RedisInsight. We just need to access the `localhost:8000` route and create the database instance, according to the following instructions:

```txt
HOST -> cache
PORT -> 6379
NAME -> Anyone
USERNAME -> It is not necessary
PASSWORD -> The same inserted into env
```


## Dependencies

This project uses hashed dependencies. To update them, edit `requirements/base.in` for project dependencies and `requirements/dev.in` for development dependencies and run:
```sh
pip-compile --generate-hashes --output-file requirements/base.txt requirements/base.in && \
pip-compile --generate-hashes --output-file requirements/dev.txt requirements/dev.in
```
It is always necessary to `pip-compile` both because dev-deps references base-deps.

## Usage

In order to be able to normalize, we add the best practices in this project, aiming to respect the principles with example **Clean Code**, **SOLID** and others. For more details, see the tip links!


### Formatters and Linters

* [Flake8](https://flake8.pycqa.org/en/latest/index.html)
* [Black](https://black.readthedocs.io/en/stable/)
* [Isort](https://isort.readthedocs.io/en/latest/)
* [Bandit](https://bandit.readthedocs.io/en/latest/)
* [MyPy](https://mypy.readthedocs.io/en/stable/)

**Obs:**

* Programming with Python, we use the `snake_case` style for variables, functions and methods, and the `PascalCase` style for classes. Configuration variables should written in `UPPERCASE`.

### Structure

We use the **microservices architecture patterns** with **DDD principle**, to create system resources. To example, see the content:

```sh
./
├── alembic/
│   ├── versions/
│   │   └── 7fd1ecdb54e8_initial_migration.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── logs/
│   └── app.log
├── requirements/
│   ├── base.in*
│   ├── base.txt
│   ├── dev.in*
│   └── dev.txt
├──  server/
│   ├── api/
│   │   ├── v1/
│   │   │   └── stocks.py
│   │   ├── __init__.py*
│   │   └── routes.py*
│   ├── application/
│   │   ├── external_api.py
│   │   ├── __init__.py
│   │   ├── scraper.py
│   │   └── services.py
│   ├── core/
│   │   ├── cache.py
│   │   ├── database.py
│   │   ├── exceptions.py*
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   └── settings.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── repositories.py
│   │   └── schemas.py
│   └── __init__.py
├── tests/
│   └── test_stock.py
├── alembic.ini
├── docker-compose copy.yml*
├── docker-compose.yml*
├── Dockerfile
├── env.example*
├── manage.py*
├── pyproject.toml*
└── README.md
```

### Tests

In this application, we used this dependencies to perform, scan and cover tests in the application:

* [Interrogate](https://interrogate.readthedocs.io/en/latest/)
* [Pytest](https://docs.pytest.org/en/8.3.x/)

In this application, unit tests were created, using **pytest**. Follow the instructions to run the tests. The commands are the same for both settings, just the environment follow belou the steps:

### Environment Local

* To see tests list

```sh
pytest --co
```

* To run all test

```sh
pytest tests/
```

* To run only test module

```sh
pytest tests/<module-you-want-test>.py
```

* To run only function test module

```sh
pytest tests/<module-you-want-test>.py::<function_teste_name>
```

### Container Environment

* To see tests list

```sh
docker compose run backend pytest --co
```

* To run all test

```sh
docker compose run backend pytest tests/
```

* To run only test module

```sh
docker compose run backend pytest tests/<module-you-want-test>.py
```

* To run only function test module

```sh
docker compose run backend tests/<module-you-want-test>.py::<function_teste_name>
```

**Obs:**

* Any doubts about the use or how pytest works, in the resources section we provide a direct link to the tool's documentation.


## Resources and Documentations

* [Pip (Package Installer Python)](https://pip.pypa.io/en/stable/)
* [Pre-commits](https://pre-commit.com/index.html)
* [Editor Config](https://editorconfig.org/)
* [Pip Tools](https://github.com/jazzband/pip-tools)
* [FastAPI](https://docs.djangoproject.com/en/3.2/)
* [Docker](https://docs.docker.com/get-started/)
* [Docker Compose](https://docs.docker.com/compose/)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

[python-url]: https://www.python.org/dev/peps/pep-0596/
[python-image]: https://img.shields.io/badge/python-v3.12-blue
[fastapi-image]: https://img.shields.io/badge/FastAPI-v0.6.8-blue
[fastapi-url]: https://fastapi.tiangolo.com/
