from pydantic import BaseSettings


class Settings(BaseSettings):
    TOKEN: str
    APPID: int
    APIKEY: str

    class Config:
        env_file = ".env"


settings = Settings()
