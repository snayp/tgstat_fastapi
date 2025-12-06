import httpx
from typing import Dict, Any, Optional
from config import settings


class TgStatClient:
    """Клиент для работы с TGStat API"""
    
    def __init__(self):
        self.base_url = settings.TGSTAT_API_BASE_URL
        self.token = settings.TGSTAT_API_TOKEN
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Выполняет GET запрос к TGStat API
        
        Args:
            endpoint: Путь эндпоинта (например, '/channels/get')
            params: Параметры запроса
            
        Returns:
            Словарь с ответом API
        """
        url = f"{self.base_url}{endpoint}"
        
        # Добавляем токен в параметры, если он есть
        request_params = params or {}
        if self.token:
            request_params['token'] = self.token
        
        try:
            response = await self.client.get(url, params=request_params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"HTTP {e.response.status_code}: {e.response.text}",
                "status_code": e.response.status_code
            }
        except Exception as e:
            return {
                "error": str(e),
                "status_code": None
            }
    
    async def close(self):
        """Закрывает HTTP клиент"""
        await self.client.aclose()


# Глобальный экземпляр клиента
tgstat_client = TgStatClient()

