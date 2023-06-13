# FastAPI Example


## You'll must have installed:
- [Python 3.9+](https://www.python.org/downloads/)
- [Virtual Environments with Python3.9+](https://docs.python.org/3/tutorial/venv.html)
- [Docker](https://docs.docker.com/engine/install/)
- [Docker-compose](https://docs.docker.com/compose/install/)

___

## Setup Project

Create virtual environment
```bash
python3 -m venv env
```

Activating created virtual environment
```bash
source env/bin/activate 
```
Install app dependencies
```bash
pip install -r requirements.txt 
```

___


## Running Application

Starting database (mysql8 redis6)
```bash
docker-compose up
```

Starting application, run:
```bash
python server.py
```

---

## Acessing on local

The application will get started in http://127.0.0.1:8000  

Swagger Documentation: http://127.0.0.1:8000/docs

Redoc Documentation: http://127.0.0.1:8000/redoc

If required authentication on routes add headers:
- token = my-jwt-token
- x_token = fake-super-secret-token

---

## Testing

__For run tests__  
```bash
pytest
```

___

### Source Documentation
- [FastAPI](https://fastapi.tiangolo.com/)

- [Bigger Application](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

- [SQL](https://fastapi.tiangolo.com/tutorial/sql-databases/)

- [Testing](https://fastapi.tiangolo.com/tutorial/testing/)  

- [Pydantic](https://pydantic-docs.helpmanual.io/)  

- [SQL Relational Database SQLAlchemy by FastAPI](https://fastapi.tiangolo.com/tutorial/sql-databases/?h=databa#sql-relational-databases)

- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/index.htmll)
