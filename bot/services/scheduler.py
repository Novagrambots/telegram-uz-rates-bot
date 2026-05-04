"""Фоновый планировщик: обновление курсов и ежедневный дайджест"""
import asyncio
import logging
from datetime import datetime, time as dtime, timedelta

import pytz
from aiogram import Bot

from bot.config import settings
from bot.database import async_session
from bot.database.crud import (
    cleanup_old_records,
    get_daily_subscribers,
    get_latest_cbu_rates,
    get_user_language,
)
from bot.services.banks import fetch_all_bank_rates
from bot.services.cbu import fetch_cbu_rates
from bot.services.crypto import fetch_crypto_rates
from bot.services.formatter import format_digest

logger = logging.getLogger(__name__)

# синглтоны-локи на уровне модуля
_cbu_lock = asyncio.Lock()
_banks_lock = asyncio.Lock()
_crypto_lock = asyncio.Lock()


async def run_cbu_updater() -> None:
    """Цикл обновления курсов ЦБ"""
    while True:
        async with _cbu_lock:
            try:
                await fetch_cbu_rates()
            except Exception as e:
                logger.exception("CBU updater error: %s", e)
        await asyncio.sleep(settings.cbu_refresh_min * 60)


async def run_banks_updater() -> None:
    """Цикл обновления курсов банков. Один проход парсит все валюты сразу."""
    while True:
        async with _banks_lock:
            try:
                await fetch_all_bank_rates(["USD", "EUR", "RUB"])
            except Exception as e:
                logger.exception("Banks updater error: %s", e)
        await asyncio.sleep(settings.banks_refresh_min * 60)


async def run_crypto_updater() -> None:
    """Цикл обновления крипты"""
    while True:
        async with _crypto_lock:
            try:
                await fetch_crypto_rates()
            except Exception as e:
                logger.exception("Crypto updater error: %s", e)
        await asyncio.sleep(settings.crypto_refresh_min * 60)


async def run_daily_digest(bot: Bot) -> None:
    """Ежедневный дайджест: проверяет каждые 5 минут, у кого пора отправить.

    Для каждого подписчика смотрим его time_local в TZ бота. Если текущее время
    >= time_local и last_sent_at сегодня ещё не было — отправляем.
    """
    tz = pytz.timezone(settings.timezone)
    # дефолтное время из настроек (если у sub time_local пустое — fallback)
    try:
        hh_def, mm_def = (int(x) for x in settings.daily_digest_time.split(":"))
    except (ValueError, AttributeError):
        hh_def, mm_def = 9, 0

    while True:
        try:
            now_local = datetime.now(tz)
            today = now_local.date()
            today_start = tz.localize(datetime.combine(today, dtime(0, 0)))

            async with async_session() as session:
                subs = await get_daily_subscribers(session)
                if not subs:
                    await asyncio.sleep(300)
                    continue

                # курсы загружаем один раз на цикл
                cbu = await get_latest_cbu_rates(session)

                for sub in subs:
                    try:
                        # время отправки конкретного подписчика
                        t_local = sub.time_local or dtime(hh_def, mm_def)
                        target = tz.localize(datetime.combine(today, t_local))

                        # ещё не пора
                        if now_local < target:
                            continue

                        # уже отправляли сегодня
                        if sub.last_sent_at is not None:
                            last = sub.last_sent_at
                            # приводим к tz-aware для корректного сравнения
                            if last.tzinfo is None:
                                last = pytz.UTC.localize(last)
                            if last >= today_start:
                                continue

                        lang = await get_user_language(session, sub.user_id)
                        filtered = [r for r in cbu if r.currency in (sub.currencies or [])]
                        if not filtered:
                            filtered = cbu
                        text = format_digest(
                            filtered,
                            sub.currencies or ["USD", "EUR", "RUB"],
                            lang,
                        )
                        await bot.send_message(sub.user_id, text, parse_mode="HTML")
                        sub.last_sent_at = datetime.now(tz)
                    except Exception as e:
                        logger.warning("Дайджест юзеру %s не отправлен: %s", sub.user_id, e)
                await session.commit()
        except Exception as e:
            logger.exception("Daily digest error: %s", e)
        await asyncio.sleep(300)


async def run_db_cleanup() -> None:
    """Раз в сутки удаляет старые снимки курсов и историю конвертаций.

    Хранение:
    - rates_snapshots старше 30 дней (cbu/coingecko — нужны только свежие)
    - conversion_history старше 90 дней
    """
    # ждём минуту после старта, чтобы не упереться в инициализацию БД
    await asyncio.sleep(60)
    while True:
        try:
            async with async_session() as session:
                deleted = await cleanup_old_records(
                    session,
                    rates_keep_days=30,
                    conversions_keep_days=90,
                )
            logger.info("Cleanup: удалено %d записей из БД", deleted)
        except Exception as e:
            logger.exception("DB cleanup error: %s", e)
        # раз в сутки
        await asyncio.sleep(24 * 60 * 60)


async def start_scheduler(bot: Bot) -> None:
    """Запустить все фоновые задачи"""
    asyncio.create_task(run_cbu_updater())
    asyncio.create_task(run_banks_updater())
    asyncio.create_task(run_crypto_updater())
    asyncio.create_task(run_daily_digest(bot))
    asyncio.create_task(run_db_cleanup())
    logger.info("Scheduler: 5 фоновых задач запущено")
