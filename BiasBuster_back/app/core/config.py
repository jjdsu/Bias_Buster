import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "BiasBuster API"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "뉴스 기사 편향성 분석 서비스 백엔드"
    
    MODEL_PATH: str = "data/models/political_bias_model"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()