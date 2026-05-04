"""Модели базы данных — User, Channel и доменные таблицы курсов"""
import enum
from datetime import datetime, time

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Time,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""
    pass


class User(Base):
    """Пользователь бота"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255))
    # язык интерфейса: ru / uz / en (дефолт ru!)
    language: Mapped[str] = mapped_column(String(5), default="ru")
    # временная зона юзера (для локальных уведомлений)
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Tashkent")
    # подписан ли на ежедневный дайджест курсов
    subscribed_daily: Mapped[bool] = mapped_column(Boolean, default=False)
    # счётчик запросов (для статистики)
    download_count: Mapped[int] = mapped_column(Integer, default=0)
    # когда первый раз зашёл в бота
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # связи
    conversions: Mapped[list["ConversionHistory"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    daily_sub: Mapped["DailySubscriber | None"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User {self.telegram_id} ({self.username})>"


class Channel(Base):
    """Канал/группа для обязательной подписки"""
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # id канала в Telegram (например -1001234567890)
    channel_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    # название для отображения юзеру
    title: Mapped[str] = mapped_column(String(255))
    # ссылка на канал (для кнопки "Подписаться")
    invite_link: Mapped[str] = mapped_column(String(255))
    # когда добавлен
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<Channel {self.channel_id} ({self.title})>"


# === Доменные модели ===

class RateSourceEnum(str, enum.Enum):
    """Источники курсов валют"""
    cbu = "cbu"           # Центральный банк Узбекистана
    bank_uz = "bank_uz"   # коммерческие банки
    nbu = "nbu"           # Национальный банк Узбекистана
    coingecko = "coingecko"  # криптовалюты


class RatesSnapshot(Base):
    """Снимок курса валюты от конкретного источника в конкретный момент"""
    __tablename__ = "rates_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # источник данных
    source: Mapped[RateSourceEnum] = mapped_column(
        Enum(RateSourceEnum, name="rate_source_enum"), nullable=False
    )
    # код валюты (USD, EUR, RUB, BTC, ...)
    currency: Mapped[str] = mapped_column(String(16), nullable=False)
    # официальный курс ЦБ в сумах
    rate_uzs: Mapped[float] = mapped_column(Numeric(20, 4), nullable=False)
    # курс в USD (для крипты — цена в USD)
    rate_usd: Mapped[float | None] = mapped_column(Numeric(20, 8), nullable=True)
    # курс покупки в банке (в сумах)
    rate_buy: Mapped[float | None] = mapped_column(Numeric(20, 4), nullable=True)
    # курс продажи в банке (в сумах)
    rate_sell: Mapped[float | None] = mapped_column(Numeric(20, 4), nullable=True)
    # название банка (если source = bank_uz)
    bank_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # когда получен курс
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # составной индекс для быстрых выборок по валюте + источнику + времени
    __table_args__ = (
        Index("ix_rates_currency_source_fetched", "currency", "source", "fetched_at"),
    )

    def __repr__(self) -> str:
        return f"<RatesSnapshot {self.source}/{self.currency} = {self.rate_uzs} UZS>"


class ConversionHistory(Base):
    """История конвертаций юзера"""
    __tablename__ = "conversion_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # к какому юзеру привязан
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False, index=True
    )
    # исходная сумма
    amount: Mapped[float] = mapped_column(Numeric(20, 4), nullable=False)
    # из какой валюты
    from_curr: Mapped[str] = mapped_column(String(8), nullable=False)
    # в какую валюту
    to_curr: Mapped[str] = mapped_column(String(8), nullable=False)
    # результат конвертации
    result: Mapped[float] = mapped_column(Numeric(20, 4), nullable=False)
    # курс который использовался
    rate_used: Mapped[float] = mapped_column(Numeric(20, 8), nullable=False)
    # когда сконвертировано
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="conversions")

    def __repr__(self) -> str:
        return f"<ConversionHistory {self.amount} {self.from_curr} → {self.to_curr}>"


class DailySubscriber(Base):
    """Настройки ежедневного дайджеста юзера"""
    __tablename__ = "daily_subscribers"

    # PK = telegram_id юзера
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), primary_key=True
    )
    # список кодов валют для дайджеста (PostgreSQL ARRAY)
    currencies: Mapped[list[str]] = mapped_column(
        ARRAY(String), default=lambda: ["USD", "EUR", "RUB"], nullable=False
    )
    # время отправки дайджеста (локальное время юзера)
    time_local: Mapped[time] = mapped_column(
        Time, default=time(9, 0), nullable=False
    )
    # когда последний раз отправляли дайджест
    last_sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user: Mapped["User"] = relationship(back_populates="daily_sub")

    def __repr__(self) -> str:
        return f"<DailySubscriber user={self.user_id} currencies={self.currencies}>"
