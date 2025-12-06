from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from api.routes import router
import uvicorn

app = FastAPI(
    title="TGStat API Client",
    description="Приложение для выполнения REST GET запросов к TGStat API и сохранения результатов в PostgreSQL",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Инициализация БД при запуске приложения"""
    init_db()
    print("База данных инициализирована")


@app.on_event("shutdown")
async def shutdown_event():
    """Закрытие соединений при остановке приложения"""
    from tgstat_client import tgstat_client
    await tgstat_client.close()


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "TGStat API Client",
        "docs": "/docs",
        "endpoints": {
            "make_request": "/api/tgstat/request?endpoint=/channels/get",
            "get_requests": "/api/tgstat/requests",
            "get_request_by_id": "/api/tgstat/requests/{id}"
        }
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

