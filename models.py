from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from database import Base


class ApiRequest(Base):
    """Модель для хранения результатов запросов к TGStat API"""
    __tablename__ = "api_requests"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String, nullable=False, index=True)  # Путь эндпоинта API
    method = Column(String, default="GET")
    status_code = Column(Integer)
    response_data = Column(JSON)  # JSON ответ от API
    raw_response = Column(Text)  # Сырой ответ для отладки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<ApiRequest(id={self.id}, endpoint='{self.endpoint}', status_code={self.status_code})>"


class Category(Base):
    """Справочник категорий TGStat"""
    __tablename__ = "tgstat_categories"

    code = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)

    def __repr__(self):
        return f"<Category(code='{self.code}', name='{self.name}')>"

