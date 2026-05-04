"""Конфигурация бота — все настройки из .env"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # токен бота
    bot_token: str

    # PostgreSQL
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "bot_4_rates_uz"
    db_user: str = "bot_4_rates_uz"
    db_password: str = ""

    # юзернейм бота
    bot_username: str = ""

    # админы бота (через запятую в .env)
    admin_ids: str = ""
    admin_username: str = "admin"

    # временная зона для дайджеста и отображения времени
    timezone: str = "Asia/Tashkent"

    # интервалы обновления курсов (в минутах)
    cbu_refresh_min: int = 60
    banks_refresh_min: int = 30
    crypto_refresh_min: int = 5

    # время ежедневного дайджеста (HH:MM, локальное время)
    daily_digest_time: str = "09:00"

    @property
    def admin_id_list(self) -> list[int]:
        """Парсит admin_ids из строки в список int"""
        if not self.admin_ids:
            return []
        return [int(x.strip()) for x in self.admin_ids.split(",") if x.strip()]

    @property
    def db_url(self) -> str:
        """URL для подключения к PostgreSQL через asyncpg"""
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def db_url_sync(self) -> str:
        """Синхронный URL для Alembic (psycopg2)"""
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # игнорируем лишние переменные в .env
    )


# глобальный экземпляр настроек
settings = Settings()
