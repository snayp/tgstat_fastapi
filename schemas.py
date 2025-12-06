from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ApiRequestCreate(BaseModel):
    endpoint: str
    method: str = "GET"
    params: Optional[Dict[str, Any]] = None


class ApiRequestResponse(BaseModel):
    id: int
    endpoint: str
    method: str
    status_code: Optional[int]
    response_data: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True


class TgStatResponse(BaseModel):
    """Базовая схема для ответов TGStat API"""
    status: Optional[str] = None
    response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

