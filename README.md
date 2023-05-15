# Проект "Кошачий благотворительный фонд"

[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
![FastApi](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)

## Описание проекта

Проект позволяет создавать инвестиционные проекты и пожертвования в них.

**Используемые технологии**

- Python
- FastAPI
- GoogleApi

### 1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Filin1985/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

- Если у вас Linux/macOS

  ```
  source venv/bin/activate
  ```

- Если у вас windows

  ```
  source venv/scripts/activate
  ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

### 2. База данных и переменные окружения

В проекте используется база данных SQLite

Пример заполнения файла .env

```
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secretkey
FIRST_SUPERUSER_EMAIL=example@example.com
FIRST_SUPERUSER_PASSWORD=password
DATABASE_URL=
FIRST_SUPERUSER_EMAIL=
FIRST_SUPERUSER_PASSWORD=
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
EMAIL=
```

### 3. Запуск проекта

Создаем базу данных

```
alembic upgrade head
```

Запускаем проект

```
uvicorn app.main:app --reload
```

Открываем Redoc проекта по адресу

http://127.0.0.1:8000/docs

**Автор [Марат Ихсанов](https://github.com/Filin1985)**
