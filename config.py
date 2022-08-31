from pydantic import BaseSettings


class Settings(BaseSettings):
    TOKEN: str
    APPID: int
    APIKEY: str
    CHANNELID: int

    class Config:
        env_file = ".env"


settings = Settings()
