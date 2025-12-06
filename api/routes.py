from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, Union
from datetime import datetime
from database import get_db
from models import ApiRequest
from schemas import ApiRequestCreate, ApiRequestResponse
from tgstat_client import tgstat_client
import json

router = APIRouter(prefix="/api/tgstat", tags=["TGStat"])


@router.get("/request")
async def make_tgstat_request(
    endpoint: str = Query(..., description="Путь эндпоинта TGStat API (например, /channels/get)"),
    params: Optional[str] = Query(None, description="JSON строка с параметрами запроса"),
    save_to_db: bool = Query(True, description="Сохранить результат в БД"),
    db: Session = Depends(get_db)
):
    """
    Выполняет GET запрос к TGStat API и опционально сохраняет результат в PostgreSQL
    
    Args:
        endpoint: Путь эндпоинта (например, /channels/get)
        params: JSON строка с параметрами запроса
        save_to_db: Сохранить ли результат в БД
        db: Сессия БД
    """
    # Парсим параметры, если они переданы
    request_params = None
    if params:
        try:
            request_params = json.loads(params)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Неверный формат JSON в параметрах")
    
    # Выполняем запрос к TGStat API
    response_data = await tgstat_client.get(endpoint, request_params)
    
    # Извлекаем статус код из ответа, если есть
    status_code = response_data.get("status_code", 200)
    if "error" in response_data:
        status_code = response_data.get("status_code", 500)
    
    # Сохраняем в БД, если требуется
    if save_to_db:
        db_request = ApiRequest(
            endpoint=endpoint,
            method="GET",
            status_code=status_code,
            response_data=response_data,
            raw_response=json.dumps(response_data, ensure_ascii=False)
        )
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        
        return ApiRequestResponse(
            id=db_request.id,
            endpoint=db_request.endpoint,
            method=db_request.method,
            status_code=db_request.status_code,
            response_data=db_request.response_data,
            created_at=db_request.created_at
        )
    else:
        # Возвращаем только ответ API без сохранения
        return ApiRequestResponse(
            id=0,
            endpoint=endpoint,
            method="GET",
            status_code=status_code,
            response_data=response_data,
            created_at=datetime.now()
        )


@router.get("/requests", response_model=list[ApiRequestResponse])
async def get_saved_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    endpoint: Optional[str] = Query(None, description="Фильтр по эндпоинту"),
    db: Session = Depends(get_db)
):
    """
    Получает список сохраненных запросов из БД
    
    Args:
        skip: Количество записей для пропуска
        limit: Максимальное количество записей
        endpoint: Фильтр по эндпоинту (опционально)
        db: Сессия БД
    """
    query = db.query(ApiRequest)
    
    if endpoint:
        query = query.filter(ApiRequest.endpoint.contains(endpoint))
    
    requests = query.order_by(ApiRequest.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        ApiRequestResponse(
            id=req.id,
            endpoint=req.endpoint,
            method=req.method,
            status_code=req.status_code,
            response_data=req.response_data,
            created_at=req.created_at
        )
        for req in requests
    ]


@router.get("/requests/{request_id}", response_model=ApiRequestResponse)
async def get_request_by_id(
    request_id: int,
    db: Session = Depends(get_db)
):
    """
    Получает сохраненный запрос по ID
    
    Args:
        request_id: ID запроса
        db: Сессия БД
    """
    request = db.query(ApiRequest).filter(ApiRequest.id == request_id).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    
    return ApiRequestResponse(
        id=request.id,
        endpoint=request.endpoint,
        method=request.method,
        status_code=request.status_code,
        response_data=request.response_data,
        created_at=request.created_at
    )

