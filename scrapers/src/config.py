from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = "trajectoire"
    postgres_password: str = "changeme"
    postgres_db: str = "trajectoire"
    postgres_host: str = "db"
    postgres_port: int = 5432

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = Settings()
