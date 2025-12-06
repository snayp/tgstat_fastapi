"""
Примеры использования API
"""
import httpx
import json

BASE_URL = "http://localhost:8000"


async def example_make_request():
    """Пример выполнения запроса к TGStat API"""
    async with httpx.AsyncClient() as client:
        # Пример 1: Простой запрос
        response = await client.get(
            f"{BASE_URL}/api/tgstat/request",
            params={
                "endpoint": "/channels/get",
                "params": json.dumps({"channel": "@example"}),
                "save_to_db": "true"
            }
        )
        print("Пример 1 - Простой запрос:")
        print(response.json())
        print("\n" + "="*50 + "\n")
        
        # Пример 2: Запрос без сохранения в БД
        response = await client.get(
            f"{BASE_URL}/api/tgstat/request",
            params={
                "endpoint": "/channels/search",
                "params": json.dumps({"q": "python"}),
                "save_to_db": "false"
            }
        )
        print("Пример 2 - Запрос без сохранения:")
        print(response.json())
        print("\n" + "="*50 + "\n")


async def example_get_requests():
    """Пример получения списка сохраненных запросов"""
    async with httpx.AsyncClient() as client:
        # Получить все запросы
        response = await client.get(
            f"{BASE_URL}/api/tgstat/requests",
            params={"skip": 0, "limit": 10}
        )
        print("Список запросов:")
        print(response.json())
        print("\n" + "="*50 + "\n")
        
        # Получить запросы с фильтром по эндпоинту
        response = await client.get(
            f"{BASE_URL}/api/tgstat/requests",
            params={"endpoint": "/channels/get", "limit": 5}
        )
        print("Запросы с фильтром:")
        print(response.json())


async def example_get_request_by_id():
    """Пример получения запроса по ID"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/tgstat/requests/1")
        print("Запрос по ID:")
        print(response.json())


if __name__ == "__main__":
    import asyncio
    
    # Запустите приложение перед выполнением примеров
    # python main.py
    
    # Раскомментируйте нужный пример:
    # asyncio.run(example_make_request())
    # asyncio.run(example_get_requests())
    # asyncio.run(example_get_request_by_id())

