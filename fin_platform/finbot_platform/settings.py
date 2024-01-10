import os
from pathlib import Path
from tempfile import gettempdir
from typing import List, Literal, Optional, Union
from pydantic_settings import BaseSettings
TEMP_DIR = Path(gettempdir())
LOG_LEVEL = Literal[
    "NOTSET",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "FATAL",
]

SASL_MECHANISM = Literal[
    "PLAIN",
    "SCRAM-SHA-256",
]

ENVIRONMENT = Literal[
    "development",
    "production",
]



class Settings(BaseSettings):
    '''
    Application settings.

    These parameters can be configured
    with environment variables.
    '''
    JWT_SECRET_KEY:str = "ggijgaglkhwoi3o53h5k3hk35bjk3m5hoicd23413"
    host: str = '127.0.0.1'
    port: int = 8000
    workers_count: int = 1
    reload: bool = True
    environment: ENVIRONMENT = 'development'
    log_level: LOG_LEVEL = 'INFO'
    secret_signing_key: str = 'JF52S66x6WMoifP5gZreiguYs9LYMn0lkXqgPYoNMD0='
    openai_api_base: str = 'https://api.openai.com/v1'
    openai_api_key: str = "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"
    openai_api_version: str = '2023-08-01-preview'
    azure_openai_deployment_name: str = '<Should be updated via env if using azure>'
    frontend_url: str = 'http://localhost:3000'
    allowed_origins_regex: Optional[str] = None
    db_config:dict = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'port': 3306,
        'database': 'mybank'
    }
    db_echo: bool = False

    db_ca_path: Optional[str] = None
    pinecone_api_key: Optional[str] = None
    pinecone_index_name: Optional[str] = None
    pinecone_environment: Optional[str] = None
    pusher_app_id: Optional[str] = None
    pusher_key: Optional[str] = None
    pusher_secret: Optional[str] = None
    pusher_cluster: Optional[str] = None
    @property
    def db_url(self) -> str:
        return f"mysql+mysqlconnector://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
    class Config:
        __qualname__ = 'Settings.Config'
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
