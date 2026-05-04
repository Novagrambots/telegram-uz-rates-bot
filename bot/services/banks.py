"""Сервис курсов коммерческих банков Узбекистана.

bank.uz публичного JSON-API не имеет — парсим HTML страниц банков
вида https://bank.uz/uz/currency/bank/{slug}. Список slug-ов получаем
из общей таблицы валют bank.uz и кэшируем.
"""
import asyncio
import logging
import re

import httpx

from bot.database import async_session
from bot.database.crud import save_rates_snapshot_batch
from bot.database.models import RateSourceEnum

logger = logging.getLogger(__name__)

BANK_LIST_URL = "https://bank.uz/uz/currency"
BANK_PAGE_URL = "https://bank.uz/uz/currency/bank/{slug}"

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

_sem = asyncio.Semaphore(5)
_slug_cache: list[str] = []
_slug_lock = asyncio.Lock()

# Запасной список slug на случай, если общая страница не отдаст ссылки.
FALLBACK_SLUGS = [
    "nbu", "kapitalbank", "asaka-bank", "hamkorbank", "agrobank",
    "ipoteka-bank", "asia-alliance-bank", "anor-bank", "infinbank",
    "ipakyulibank", "sanoat-qurilish-bank", "qishloq-qurilish-bank",
    "mikrokreditbank", "savdogar-bank", "trastbank", "turonbank",
    "universalbank", "uzkdb-bank", "xalq-bank", "aloqabank",
    "hayot-bank", "invest-finance-bank", "orient-finans-bank",
    "poytaxtbank", "ravnaq-bank", "saderat-bank-tashkent",
    "smartbank", "tenge-bank",
]

# Slug → человекочитаемое имя (для отображения, если в HTML не нашли заголовок)
_SLUG_NAME_HINT = {
    "nbu": "NBU",
    "kapitalbank": "Kapitalbank",
    "asaka-bank": "Asakabank",
    "hamkorbank": "Hamkorbank",
    "agrobank": "Agrobank",
    "ipoteka-bank": "Ipoteka Bank",
    "asia-alliance-bank": "Asia Alliance Bank",
    "anor-bank": "Anorbank",
    "infinbank": "Infinbank",
    "ipakyulibank": "Ipak Yuli Bank",
    "sanoat-qurilish-bank": "SQB",
    "qishloq-qurilish-bank": "QQB",
    "mikrokreditbank": "Mikrokreditbank",
    "savdogar-bank": "Savdogar Bank",
    "trastbank": "Trastbank",
    "turonbank": "Turonbank",
    "universalbank": "Universal Bank",
    "uzkdb-bank": "UzKDB Bank",
    "xalq-bank": "Xalq Bank",
    "aloqabank": "Aloqabank",
    "hayot-bank": "Hayot Bank",
    "invest-finance-bank": "Invest Finance Bank",
    "orient-finans-bank": "Orient Finans Bank",
    "poytaxtbank": "Poytaxt Bank",
    "ravnaq-bank": "Ravnaq Bank",
    "saderat-bank-tashkent": "Saderat Bank",
    "smartbank": "Smart Bank",
    "tenge-bank": "Tenge Bank",
}

# Парсер таблицы валют на странице банка bank.uz/uz/currency/bank/{slug}.
# Каждый блок начинается с подписи "Kod"; внутри по очереди: код валюты,
# номинал ("Birlik"), buy ("Sotib olish") и sell ("Sotish").
_RE_CCY = re.compile(r"([A-Z]{3})", re.S)
_RE_BIRLIK = re.compile(
    r">\s*Birlik\s*</span>\s*<[^>]+>\s*(\d+)\s*</span>", re.I
)
_RE_BUY = re.compile(
    r">\s*Sotib olish\s*</span>\s*<[^>]+>\s*([\d\s.,\xa0]+?)\s*</span>", re.I
)
_RE_SELL = re.compile(
    r">\s*Sotish\s*</span>\s*<[^>]+>\s*([\d\s.,\xa0]+?)\s*</span>", re.I
)


def _parse_number(s: str) -> float:
    s = s.replace("\xa0", " ").replace(" ", "").replace(",", ".")
    if not s:
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0


async def _fetch_html(client: httpx.AsyncClient, url: str) -> str | None:
    try:
        async with _sem:
            resp = await client.get(url, headers={"User-Agent": USER_AGENT})
            resp.raise_for_status()
            return resp.text
    except httpx.HTTPError as e:
        logger.warning("bank.uz GET %s: %s", url, e)
        return None


async def _refresh_slug_cache(client: httpx.AsyncClient) -> list[str]:
    """Берём slug-и банков с общей страницы bank.uz/uz/currency."""
    html = await _fetch_html(client, BANK_LIST_URL)
    if not html:
        return list(FALLBACK_SLUGS)
    slugs = sorted(set(re.findall(r"/uz/currency/bank/([a-z0-9-]+)", html)))
    if not slugs:
        return list(FALLBACK_SLUGS)
    return slugs


async def _get_slugs(client: httpx.AsyncClient) -> list[str]:
    global _slug_cache
    if _slug_cache:
        return _slug_cache
    async with _slug_lock:
        if _slug_cache:
            return _slug_cache
        _slug_cache = await _refresh_slug_cache(client)
    return _slug_cache


def _extract_bank_name(html: str, slug: str) -> str:
    """Имя банка по slug. h1 на bank.uz содержит мусор вида
    "Bank valyutalar kursi bugun sana uchun" — не используем его."""
    return _SLUG_NAME_HINT.get(slug, slug.replace("-", " ").title())


def _parse_bank_page(html: str, slug: str) -> list[dict]:
    """Извлекает список {currency, buy, sell, bank_name} из HTML банка."""
    bank_name = _extract_bank_name(html, slug)
    # каждый блок валюты разделён подписью "Kod"
    parts = re.split(r">\s*Kod\s*</span>", html, flags=re.I)[1:]
    rows: list[dict] = []
    for part in parts:
        head = part[:400]
        m_ccy = _RE_CCY.search(head)
        if not m_ccy:
            continue
        ccy = m_ccy.group(1).upper()
        m_bir = _RE_BIRLIK.search(part[:3000])
        m_buy = _RE_BUY.search(part[:5000])
        m_sell = _RE_SELL.search(part[:5000])
        nominal = int(m_bir.group(1)) if m_bir and m_bir.group(1).isdigit() else 1
        if nominal == 0:
            nominal = 1
        buy = _parse_number(m_buy.group(1)) / nominal if m_buy else 0.0
        sell = _parse_number(m_sell.group(1)) / nominal if m_sell else 0.0
        if buy <= 0 and sell <= 0:
            continue
        rows.append({
            "bank_name": bank_name,
            "currency": ccy,
            "buy": buy,
            "sell": sell,
        })
    return rows


async def fetch_all_bank_rates(currencies: list[str]) -> dict[str, list[dict]]:
    """Один проход по всем страницам банков, возвращает данные сразу
    по всем запрошенным валютам. Один и тот же HTML парсится один раз.
    """
    wanted = {c.upper() for c in currencies}
    timeout = httpx.Timeout(20.0, connect=10.0)
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        slugs = await _get_slugs(client)
        pages = await asyncio.gather(
            *(_fetch_html(client, BANK_PAGE_URL.format(slug=s)) for s in slugs)
        )

    by_ccy: dict[str, list[dict]] = {c: [] for c in wanted}
    for slug, html in zip(slugs, pages):
        if not html:
            continue
        for r in _parse_bank_page(html, slug):
            if r["currency"] in wanted:
                by_ccy[r["currency"]].append(r)

    for ccy, rows in by_ccy.items():
        rows.sort(key=lambda r: r["buy"], reverse=True)

    # сохраняем единым батчем — replace last snapshot для каждой валюты
    flat = [
        {
            "currency": r["currency"],
            "rate_uzs": r["buy"] or r["sell"],
            "rate_buy": r["buy"] or None,
            "rate_sell": r["sell"] or None,
            "bank_name": r["bank_name"],
        }
        for rows in by_ccy.values() for r in rows
    ]
    if flat:
        try:
            async with async_session() as session:
                await save_rates_snapshot_batch(session, RateSourceEnum.bank_uz, flat)
        except Exception as e:
            logger.warning("Не удалось сохранить курсы банков: %s", e)

    logger.info(
        "Banks: %d страниц, валюты: %s",
        len(slugs),
        ", ".join(f"{c}={len(by_ccy[c])}" for c in sorted(wanted)),
    )
    return by_ccy


async def fetch_bank_rates(currency: str = "USD") -> list[dict]:
    """Курсы заданной валюты по всем банкам Узбекистана.

    Возвращает список {bank_name, currency, buy, sell}, отсортированный
    по покупке (DESC). При сбое отдельных банков пропускаем их без ошибки.
    """
    currency = currency.upper()
    timeout = httpx.Timeout(20.0, connect=10.0)
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        slugs = await _get_slugs(client)
        pages = await asyncio.gather(
            *(_fetch_html(client, BANK_PAGE_URL.format(slug=s)) for s in slugs)
        )

    rows: list[dict] = []
    for slug, html in zip(slugs, pages):
        if not html:
            continue
        for r in _parse_bank_page(html, slug):
            if r["currency"] == currency:
                rows.append(r)

    rows.sort(key=lambda r: r["buy"], reverse=True)

    if rows:
        try:
            async with async_session() as session:
                await save_rates_snapshot_batch(
                    session,
                    RateSourceEnum.bank_uz,
                    [
                        {
                            "currency": r["currency"],
                            "rate_uzs": r["buy"] or r["sell"],
                            "rate_buy": r["buy"] or None,
                            "rate_sell": r["sell"] or None,
                            "bank_name": r["bank_name"],
                        }
                        for r in rows
                    ],
                )
        except Exception as e:
            logger.warning("Не удалось сохранить курсы банков (%s): %s", currency, e)

    logger.info("Banks (%s): %d записей с %d страниц", currency, len(rows), len(slugs))
    return rows
