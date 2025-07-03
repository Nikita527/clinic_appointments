from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application."""

    app_name: str = "Clinic Appointments API"
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str
    debug: bool
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


settings = Settings()  # type: ignore
