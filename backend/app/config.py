from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/sindh_police_imei"
    jwt_secret_key: str = "change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    cors_origins: str = "http://localhost:3000"
    max_citizen_registrations_per_year: int = 10
    max_shop_registrations_per_day: int = 50

    class Config:
        env_file = ".env"


settings = Settings()
