from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    db_name: str
    db_host: str
    db_user: str
    db_password: str
    db_port: int
    model_config = SettingsConfigDict(env_file='prod.env')
    # TODO: Shall be this
    # model_config = SettingsConfigDict(env_file='prod.env', secrets_dir='')

@lru_cache()
def get_settings():
    return Settings()