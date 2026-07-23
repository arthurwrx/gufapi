from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    """
    Configurações gerais usadas na aplicação
    """

    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://arthurwrx:ramones12@127.0.0.1:54673/faculdade"
    DBBaseModel = declarative_base()

    JWT_SECRET: str = "n8tyKfKytMrnTRpclrO60QyYc9HVCAtzpSAvObGQnRE"

    """
    import secrets
    
    token: str = secrets.token_urlsafe(32)
    """

    ALGORITHM: str = "HS256"

    # 60 Minutos x 24h x 7 dias = 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings = Settings()
