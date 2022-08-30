from pydantic import BaseSettings


class Settings(BaseSettings):
    TOKEN: str
    APPID: int

    class Config:
        env_file = ".env"


settings = Settings()