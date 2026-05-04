"""CRUD операции с базой данных"""
from datetime import datetime, timedelta, time as dtime

from sqlalchemy import and_, delete, desc, func as sa_func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import (
    Channel,
    ConversionHistory,
    DailySubscriber,
    RateSourceEnum,
    RatesSnapshot,
    User,
)


# === User ===

async def get_or_create_user(
    session: AsyncSession,
    telegram_id: int,
    username: str | None,
    full_name: str,
    language: str | None = None,
) -> User:
    """Получить юзера или создать нового"""
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            telegram_id=telegram_id,
            username=username,
            full_name=full_name,
            language=language or "ru",
        )
        session.add(user)
        try:
            await session.commit()
            await session.refresh(user)
        except IntegrityError:
            # параллельный запрос мог вставить юзера — откатываем и читаем заново
            await session.rollback()
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalar_one()

    return user


async def get_user_language(session: AsyncSession, telegram_id: int) -> str:
    """Получить язык юзера (по умолчанию ru)"""
    result = await session.execute(
        select(User.language).where(User.telegram_id == telegram_id)
    )
    lang = result.scalar_one_or_none()
    return lang or "ru"


async def update_user_language(
    session: AsyncSession, telegram_id: int, language: str
) -> None:
    """Обновить язык юзера"""
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    if user:
        user.language = language
        await session.commit()


# === Channel ===

async def get_active_channels(session: AsyncSession) -> list[Channel]:
    """Получить все каналы для обязательной подписки"""
    result = await session.execute(select(Channel))
    return list(result.scalars().all())


async def add_channel(
    session: AsyncSession,
    channel_id: int,
    title: str,
    invite_link: str,
) -> Channel:
    """Добавить канал для обязательной подписки"""
    result = await session.execute(
        select(Channel).where(Channel.channel_id == channel_id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise ValueError(f"Канал {channel_id} уже добавлен")

    channel = Channel(
        channel_id=channel_id,
        title=title,
        invite_link=invite_link,
    )
    session.add(channel)
    await session.commit()
    await session.refresh(channel)
    return channel


async def remove_channel(session: AsyncSession, channel_id: int) -> bool:
    """Удалить канал. Возвращает True если удалён"""
    result = await session.execute(
        select(Channel).where(Channel.channel_id == channel_id)
    )
    channel = result.scalar_one_or_none()
    if not channel:
        return False

    await session.delete(channel)
    await session.commit()
    return True


# === Статистика ===

async def get_user_stats(session: AsyncSession) -> dict:
    """Статистика: всего юзеров, за сегодня, подписаны на дайджест, каналов"""
    total = await session.execute(select(sa_func.count(User.id)))
    total_users = total.scalar() or 0

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_result = await session.execute(
        select(sa_func.count(User.id)).where(User.created_at >= today)
    )
    today_users = today_result.scalar() or 0

    digest_result = await session.execute(
        select(sa_func.count(User.id)).where(User.subscribed_daily == True)  # noqa: E712
    )
    total_downloads = digest_result.scalar() or 0

    channels = await session.execute(select(sa_func.count(Channel.id)))
    total_channels = channels.scalar() or 0

    return {
        "total_users": total_users,
        "today_users": today_users,
        "total_downloads": total_downloads,
        "total_channels": total_channels,
    }


async def get_all_user_ids(session: AsyncSession) -> list[int]:
    """Получить все telegram_id юзеров для рассылки"""
    result = await session.execute(select(User.telegram_id))
    return [row[0] for row in result.all()]


# === RatesSnapshot ===

async def save_rates_snapshot(
    session: AsyncSession,
    source: RateSourceEnum,
    currency: str,
    rate_uzs: float,
    rate_usd: float | None = None,
    rate_buy: float | None = None,
    rate_sell: float | None = None,
    bank_name: str | None = None,
) -> RatesSnapshot:
    """Сохранить снимок курса"""
    snap = RatesSnapshot(
        source=source,
        currency=currency,
        rate_uzs=rate_uzs,
        rate_usd=rate_usd,
        rate_buy=rate_buy,
        rate_sell=rate_sell,
        bank_name=bank_name,
    )
    session.add(snap)
    await session.commit()
    await session.refresh(snap)
    return snap


async def save_rates_snapshot_batch(
    session: AsyncSession,
    source: RateSourceEnum,
    items: list[dict],
) -> int:
    """Батчевая вставка снимков курсов. Для bank_uz сначала удаляет
    предыдущие записи по затронутым валютам — каждая ротация полностью
    замещает предыдущий снимок (старые записи нужны только для истории
    cbu/coingecko, для банков актуален только последний срез).
    """
    if not items:
        return 0
    if source == RateSourceEnum.bank_uz:
        currencies = {it["currency"] for it in items if "currency" in it}
        if currencies:
            await session.execute(
                delete(RatesSnapshot).where(
                    and_(
                        RatesSnapshot.source == RateSourceEnum.bank_uz,
                        RatesSnapshot.currency.in_(currencies),
                    )
                )
            )
    snapshots = [RatesSnapshot(source=source, **item) for item in items]
    session.add_all(snapshots)
    await session.commit()
    return len(snapshots)


async def get_latest_cbu_rates(session: AsyncSession) -> list[RatesSnapshot]:
    """Получить последние курсы ЦБ по каждой валюте"""
    # subquery: max fetched_at per currency
    sub = (
        select(
            RatesSnapshot.currency,
            sa_func.max(RatesSnapshot.fetched_at).label("max_at"),
        )
        .where(RatesSnapshot.source == RateSourceEnum.cbu)
        .group_by(RatesSnapshot.currency)
        .subquery()
    )
    result = await session.execute(
        select(RatesSnapshot)
        .join(
            sub,
            and_(
                RatesSnapshot.currency == sub.c.currency,
                RatesSnapshot.fetched_at == sub.c.max_at,
            ),
        )
        .where(RatesSnapshot.source == RateSourceEnum.cbu)
    )
    return list(result.scalars().all())


async def get_previous_day_cbu_rates(
    session: AsyncSession,
) -> dict[str, float]:
    """Курсы ЦБ за предыдущий торговый день для расчёта дельты"""
    # берём последнюю запись по каждой валюте, у которой fetched_at < сегодня (start of day)
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    sub = (
        select(
            RatesSnapshot.currency,
            sa_func.max(RatesSnapshot.fetched_at).label("max_at"),
        )
        .where(
            and_(
                RatesSnapshot.source == RateSourceEnum.cbu,
                RatesSnapshot.fetched_at < today_start,
            )
        )
        .group_by(RatesSnapshot.currency)
        .subquery()
    )
    result = await session.execute(
        select(RatesSnapshot)
        .join(
            sub,
            and_(
                RatesSnapshot.currency == sub.c.currency,
                RatesSnapshot.fetched_at == sub.c.max_at,
            ),
        )
        .where(RatesSnapshot.source == RateSourceEnum.cbu)
    )
    return {s.currency: float(s.rate_uzs) for s in result.scalars().all()}


async def get_cbu_rate_history(
    session: AsyncSession, currency: str, days: int
) -> list[RatesSnapshot]:
    """История курса ЦБ за N дней — по одному снимку в день (последний за день)"""
    since = datetime.now() - timedelta(days=days)
    # выбираем все снимки за период, потом группируем по дате на уровне Python
    result = await session.execute(
        select(RatesSnapshot)
        .where(
            and_(
                RatesSnapshot.source == RateSourceEnum.cbu,
                RatesSnapshot.currency == currency,
                RatesSnapshot.fetched_at >= since,
            )
        )
        .order_by(RatesSnapshot.fetched_at.asc())
    )
    snaps = list(result.scalars().all())
    # схлопываем до одного на дату — берём последний за день
    by_date: dict[str, RatesSnapshot] = {}
    for s in snaps:
        key = s.fetched_at.strftime("%Y-%m-%d")
        by_date[key] = s
    return list(by_date.values())


async def get_bank_rates(
    session: AsyncSession, currency: str
) -> list[RatesSnapshot]:
    """Последние курсы банков по валюте (за последние 2 часа)"""
    since = datetime.now() - timedelta(hours=6)
    result = await session.execute(
        select(RatesSnapshot)
        .where(
            and_(
                RatesSnapshot.source == RateSourceEnum.bank_uz,
                RatesSnapshot.currency == currency,
                RatesSnapshot.bank_name.is_not(None),
                RatesSnapshot.fetched_at >= since,
            )
        )
        .order_by(desc(RatesSnapshot.rate_buy))
    )
    rows = list(result.scalars().all())
    # дедуп по bank_name — берём последнюю по времени (запись со свежим fetched_at)
    seen: dict[str, RatesSnapshot] = {}
    # сначала отсортируем по fetched_at desc, чтобы оставить последний
    rows_sorted = sorted(rows, key=lambda r: r.fetched_at, reverse=True)
    for r in rows_sorted:
        if r.bank_name not in seen:
            seen[r.bank_name] = r
    # вернём отсортированные по rate_buy DESC
    return sorted(seen.values(), key=lambda r: float(r.rate_buy or 0), reverse=True)


async def get_latest_crypto_rates(session: AsyncSession) -> list[RatesSnapshot]:
    """Последние курсы крипты по каждой монете"""
    sub = (
        select(
            RatesSnapshot.currency,
            sa_func.max(RatesSnapshot.fetched_at).label("max_at"),
        )
        .where(RatesSnapshot.source == RateSourceEnum.coingecko)
        .group_by(RatesSnapshot.currency)
        .subquery()
    )
    result = await session.execute(
        select(RatesSnapshot)
        .join(
            sub,
            and_(
                RatesSnapshot.currency == sub.c.currency,
                RatesSnapshot.fetched_at == sub.c.max_at,
            ),
        )
        .where(RatesSnapshot.source == RateSourceEnum.coingecko)
    )
    return list(result.scalars().all())


# === Cleanup ===

async def cleanup_old_records(
    session: AsyncSession,
    rates_keep_days: int = 30,
    conversions_keep_days: int = 90,
) -> int:
    """Удалить старые снимки курсов и устаревшую историю конвертаций.

    Возвращает суммарное количество удалённых строк.
    """
    now = datetime.utcnow()
    rates_cutoff = now - timedelta(days=rates_keep_days)
    conv_cutoff = now - timedelta(days=conversions_keep_days)

    rates_res = await session.execute(
        delete(RatesSnapshot).where(RatesSnapshot.fetched_at < rates_cutoff)
    )
    conv_res = await session.execute(
        delete(ConversionHistory).where(ConversionHistory.created_at < conv_cutoff)
    )
    await session.commit()
    return (rates_res.rowcount or 0) + (conv_res.rowcount or 0)


# === ConversionHistory ===

async def save_conversion(
    session: AsyncSession,
    user_id: int,
    amount: float,
    from_curr: str,
    to_curr: str,
    result: float,
    rate_used: float,
) -> ConversionHistory:
    """Сохранить конвертацию в историю"""
    conv = ConversionHistory(
        user_id=user_id,
        amount=amount,
        from_curr=from_curr,
        to_curr=to_curr,
        result=result,
        rate_used=rate_used,
    )
    session.add(conv)
    await session.commit()
    await session.refresh(conv)
    return conv


async def get_conversion_history(
    session: AsyncSession, user_id: int, limit: int = 10
) -> list[ConversionHistory]:
    """История конвертаций юзера"""
    result = await session.execute(
        select(ConversionHistory)
        .where(ConversionHistory.user_id == user_id)
        .order_by(desc(ConversionHistory.created_at))
        .limit(limit)
    )
    return list(result.scalars().all())


# === DailySubscriber ===

async def get_daily_subscribers(
    session: AsyncSession,
) -> list[DailySubscriber]:
    """Все подписчики ежедневного дайджеста"""
    result = await session.execute(select(DailySubscriber))
    return list(result.scalars().all())


async def upsert_daily_subscriber(
    session: AsyncSession,
    user_id: int,
    currencies: list[str] | None = None,
    time_local: dtime | None = None,
) -> DailySubscriber:
    """Создать/обновить подписку"""
    result = await session.execute(
        select(DailySubscriber).where(DailySubscriber.user_id == user_id)
    )
    sub = result.scalar_one_or_none()
    if sub is None:
        sub = DailySubscriber(
            user_id=user_id,
            currencies=currencies or ["USD", "EUR", "RUB"],
            time_local=time_local or dtime(9, 0),
        )
        session.add(sub)
    else:
        if currencies is not None:
            sub.currencies = currencies
        if time_local is not None:
            sub.time_local = time_local

    # обновляем флаг у юзера
    user_res = await session.execute(
        select(User).where(User.telegram_id == user_id)
    )
    user = user_res.scalar_one_or_none()
    if user:
        user.subscribed_daily = True

    await session.commit()
    await session.refresh(sub)
    return sub


async def remove_daily_subscriber(
    session: AsyncSession, user_id: int
) -> bool:
    """Удалить подписку"""
    result = await session.execute(
        delete(DailySubscriber).where(DailySubscriber.user_id == user_id)
    )
    user_res = await session.execute(
        select(User).where(User.telegram_id == user_id)
    )
    user = user_res.scalar_one_or_none()
    if user:
        user.subscribed_daily = False
    await session.commit()
    return result.rowcount > 0
