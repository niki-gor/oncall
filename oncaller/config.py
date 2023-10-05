from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="oncall_")

    host: str = "http://localhost:8080"
    username: str = "root"
    password: str = "root"
