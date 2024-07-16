from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    Sign_In_Word: str = "gm"


settings = Settings()
