from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    Sign_In_Word: str = "gm"
    TOKEN: str = "MTI1OTgzNjkzMDY1MzQyNTcxNQ.GUl1mG.mQngRPyczxcq6F40d2PGqzPwDDOqJF6o5OlCY"


settings = Settings()
