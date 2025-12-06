# TGStat FastAPI Client

Приложение для выполнения REST GET запросов к [TGStat API](https://api.tgstat.ru/) и сохранения результатов в PostgreSQL.

## Возможности

- Выполнение GET запросов к TGStat API
- Автоматическое сохранение результатов в PostgreSQL
- Просмотр истории запросов
- RESTful API с автоматической документацией

## Требования

- Python 3.8+
- PostgreSQL 12+

## Установка

1. Клонируйте репозиторий или создайте проект

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` в корне проекта со следующим содержимым:
```env
# PostgreSQL настройки
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=tgstat_db

# TGStat API настройки
TGSTAT_API_TOKEN=your_api_token_here
TGSTAT_API_BASE_URL=https://api.tgstat.ru
```

4. Настройте переменные окружения в `.env`:
   - Настройте подключение к PostgreSQL (измените USER, PASSWORD, HOST, PORT, DB при необходимости)
   - Добавьте ваш API токен TGStat вместо `your_api_token_here` (получить можно на [tgstat.ru](https://tgstat.ru/))

5. Создайте базу данных PostgreSQL:
```bash
createdb tgstat_db
```

6. Запустите приложение:
```bash
python main.py
```

Или с помощью uvicorn:
```bash
uvicorn main:app --reload
```

Приложение будет доступно по адресу: http://localhost:8000

## API Документация

После запуска приложения доступна автоматическая документация:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Использование

### Выполнение запроса к TGStat API

```bash
GET /api/tgstat/request?endpoint=/channels/get&params={"channel":"@example"}
```

Параметры:
- `endpoint` (обязательный) - путь эндпоинта TGStat API
- `params` (опциональный) - JSON строка с параметрами запроса
- `save_to_db` (опциональный, по умолчанию `true`) - сохранить ли результат в БД

Пример:
```bash
curl "http://localhost:8000/api/tgstat/request?endpoint=/channels/get&params=%7B%22channel%22%3A%22%40example%22%7D"
```

### Получение списка сохраненных запросов

```bash
GET /api/tgstat/requests?skip=0&limit=100&endpoint=/channels/get
```

Параметры:
- `skip` - количество записей для пропуска (по умолчанию 0)
- `limit` - максимальное количество записей (по умолчанию 100, максимум 1000)
- `endpoint` - фильтр по эндпоинту (опционально)

### Получение запроса по ID

```bash
GET /api/tgstat/requests/{request_id}
```

## Структура проекта

```
tgstat_fastapi/
├── main.py              # Главный файл приложения
├── config.py            # Конфигурация
├── database.py          # Настройка БД
├── models.py            # SQLAlchemy модели
├── schemas.py           # Pydantic схемы
├── tgstat_client.py     # Клиент для TGStat API
├── api/
│   ├── __init__.py
│   └── routes.py        # API роуты
├── requirements.txt     # Зависимости
├── .env.example         # Пример конфигурации
└── README.md            # Документация
```

## Примеры эндпоинтов TGStat API

Согласно документации TGStat API, доступны следующие эндпоинты:
- `/channels/get` - получение информации о канале
- `/channels/search` - поиск каналов
- `/posts/get` - получение постов
- И другие...

Подробная документация: https://api.tgstat.ru/docs/

## Лицензия

MIT

