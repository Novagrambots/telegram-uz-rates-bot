"""Сервис курсов криптовалют (CoinGecko)"""
import asyncio
import logging

import httpx

from bot.database import async_session
from bot.database.crud import get_latest_cbu_rates, save_rates_snapshot_batch
from bot.database.models import RateSourceEnum

logger = logging.getLogger(__name__)

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
CRYPTO_MAP = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "tether": "USDT",
    "binancecoin": "BNB",
    "the-open-network": "TON",
}

_sem = asyncio.Semaphore(5)


async def fetch_crypto_rates() -> list[dict]:
    """Получить курсы крипты в USD через CoinGecko и пересчитать в UZS по курсу ЦБ.

    Возвращает список: {currency, rate_usd, rate_uzs}.
    При сбое API — пустой список.
    """
    ids = ",".join(CRYPTO_MAP.keys())
    params = {"ids": ids, "vs_currencies": "usd"}

    try:
        async with _sem:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(COINGECKO_URL, params=params)
                resp.raise_for_status()
                data = resp.json()
    except (httpx.HTTPError, ValueError) as e:
        logger.warning("CoinGecko недоступен: %s", e)
        return []

    # пересчёт USD → UZS через курс ЦБ
    usd_uzs: float | None = None
    try:
        async with async_session() as session:
            cbu = await get_latest_cbu_rates(session)
        for s in cbu:
            if s.currency == "USD":
                usd_uzs = float(s.rate_uzs)
                break
    except Exception as e:
        logger.warning("Не удалось получить USD/UZS из ЦБ: %s", e)

    out: list[dict] = []
    for cg_id, code in CRYPTO_MAP.items():
        prices = data.get(cg_id, {})
        usd = prices.get("usd")
        if usd is None:
            continue
        usd_f = float(usd)
        uzs_f = usd_f * usd_uzs if usd_uzs else None
        out.append(
            {
                "currency": code,
                "rate_usd": usd_f,
                "rate_uzs": uzs_f,
            }
        )

    if out:
        try:
            async with async_session() as session:
                await save_rates_snapshot_batch(
                    session,
                    RateSourceEnum.coingecko,
                    [
                        {
                            "currency": item["currency"],
                            "rate_uzs": item["rate_uzs"] or 0.0,
                            "rate_usd": item["rate_usd"],
                        }
                        for item in out
                    ],
                )
        except Exception as e:
            logger.warning("Не удалось сохранить крипту в БД: %s", e)

    logger.info("Crypto: загружено %d монет", len(out))
    return out
