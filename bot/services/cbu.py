"""Сервис курсов Центрального банка Узбекистана"""
import asyncio
import logging

import httpx

from bot.database import async_session
from bot.database.crud import save_rates_snapshot_batch
from bot.database.models import RateSourceEnum

logger = logging.getLogger(__name__)

CBU_URL = "https://cbu.uz/oz/arkhiv-kursov-valyut/json/"
MAIN_CURRENCIES = {"USD", "EUR", "RUB", "KZT", "GBP", "CNY", "JPY", "TRY"}

# семафор на параллельные запросы к API
_sem = asyncio.Semaphore(5)


async def fetch_cbu_rates() -> list[dict]:
    """GET курсы ЦБ Узбекистана. Возвращает список основных валют.

    Каждый элемент: {currency, rate_uzs (float), nominal (int), date (str)}
    Также сохраняет снимки в БД (RatesSnapshot, source=cbu).
    При ошибке сети — возвращает пустой список и логирует warning.
    """
    try:
        async with _sem:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(CBU_URL)
                resp.raise_for_status()
                data = resp.json()
    except (httpx.HTTPError, ValueError) as e:
        logger.warning("CBU API недоступен: %s", e)
        return []

    out: list[dict] = []
    for row in data:
        ccy = row.get("Ccy")
        if not ccy or ccy not in MAIN_CURRENCIES:
            continue
        try:
            rate = float(row.get("Rate", 0))
            nominal = int(row.get("Nominal", 1) or 1)
        except (TypeError, ValueError):
            continue

        # нормализуем к единице (если nominal > 1)
        rate_per_unit = rate / nominal if nominal else rate

        out.append(
            {
                "currency": ccy,
                "rate_uzs": rate_per_unit,
                "nominal": nominal,
                "date": row.get("Date", ""),
            }
        )

    # сохраняем в БД одним батчем
    if out:
        try:
            async with async_session() as session:
                await save_rates_snapshot_batch(
                    session,
                    RateSourceEnum.cbu,
                    [
                        {"currency": item["currency"], "rate_uzs": item["rate_uzs"]}
                        for item in out
                    ],
                )
        except Exception as e:
            logger.warning("Не удалось сохранить снимки CBU в БД: %s", e)

    logger.info("CBU: загружено %d валют", len(out))
    return out
