"""Форматирование сообщений о курсах валют"""
from datetime import datetime

import pytz

from bot.config import settings
from bot.emojis import E
from bot.i18n import t

# флаги/иконки для основных валют

# порядок отображения для ЦБ
CBU_ORDER = ["USD", "EUR", "RUB", "GBP", "CNY", "KZT", "JPY", "TRY"]


def fmt_rate(amount: float, lang: str = "ru") -> str:
    """12 450.50 (ru/uz) или 12,450.50 (en) — два знака после точки"""
    if amount is None:
        return "—"
    s = f"{float(amount):,.2f}"
    if lang == "en":
        return s  # 12,450.50
    # ru/uz: пробел вместо запятой
    return s.replace(",", " ")


def fmt_int(amount: float, lang: str = "ru") -> str:
    """12 450 (ru/uz) или 12,450 (en) — без знаков после точки"""
    if amount is None:
        return "—"
    s = f"{float(amount):,.0f}"
    if lang == "en":
        return s
    return s.replace(",", " ")


def fmt_delta(delta: float) -> str:
    """▲ +5.20 / ▼ -2.10 / — 0.00"""
    if delta is None:
        return ""
    if abs(delta) < 0.01:
        return "— 0.00"
    sign = "+" if delta > 0 else ""
    arrow = "▲" if delta > 0 else "▼"
    return f"{arrow} {sign}{delta:.2f}"


CCY_ICON = {
    "USD": "🇺🇸",
    "EUR": "🇪🇺",
    "RUB": "🇷🇺",
    "KZT": "🇰🇿",
    "GBP": "🇬🇧",
    "CNY": "🇨🇳",
    "JPY": "🇯🇵",
    "TRY": "🇹🇷",
    "BTC": "₿",
    "ETH": "⟠",
    "USDT": "💲",
    "BNB": "🟡",
    "TON": "💎",
    "UZS": "🇺🇿",
}


def _icon(curr: str) -> str:
    """Флаг страны для валюты (unicode — премиум-аналогов в паке нет)."""
    return CCY_ICON.get(curr, E["star"])


def format_cbu_rates(
    rates: list,
    prev_map: dict[str, float],
    lang: str = "ru",
) -> str:
    """Форматирует курсы ЦБ в HTML-таблицу с дельтой к вчера.

    rates — список RatesSnapshot или dict с keys currency/rate_uzs.
    """
    title = t("rates.title", lang)
    lines = [title, ""]

    # сортируем
    def _curr(r) -> str:
        return r.currency if hasattr(r, "currency") else r["currency"]

    def _rate(r) -> float:
        return float(r.rate_uzs if hasattr(r, "rate_uzs") else r["rate_uzs"])

    rates_sorted = sorted(
        rates,
        key=lambda r: CBU_ORDER.index(_curr(r)) if _curr(r) in CBU_ORDER else 99,
    )

    for r in rates_sorted:
        ccy = _curr(r)
        rate = _rate(r)
        prev = prev_map.get(ccy)
        delta = rate - prev if prev else None
        delta_str = f"  {fmt_delta(delta)}" if delta is not None else ""
        lines.append(
            f"{_icon(ccy)} <b>{ccy}</b>  {fmt_rate(rate, lang)} UZS{delta_str}"
        )

    # дата обновления
    fetched = None
    for r in rates_sorted:
        fa = r.fetched_at if hasattr(r, "fetched_at") else None
        if fa:
            fetched = fa
            break
    if fetched:
        lines.append("")
        lines.append(f"{E['clock']} {fetched.strftime('%d.%m.%Y %H:%M')}")

    # пометка о выходных (по UZ-таймзоне)
    tz = pytz.timezone(settings.timezone)
    today = datetime.now(tz)
    if today.weekday() >= 5:
        lines.append("")
        lines.append(t("rates.weekend_note", lang))

    return "\n".join(lines)


def format_bank_rates(
    rates: list,
    currency: str,
    lang: str = "ru",
    top_n: int = 5,
) -> str:
    """Топ-N банков с лучшими курсами покупки и продажи"""
    if not rates:
        return t("banks.empty", lang)

    title = t("banks.title", lang).format(currency=currency)
    lines = [title, ""]

    def _buy(r):
        return float(r.rate_buy if hasattr(r, "rate_buy") and r.rate_buy else (r.get("buy", 0) if isinstance(r, dict) else 0) or 0)

    def _sell(r):
        return float(r.rate_sell if hasattr(r, "rate_sell") and r.rate_sell else (r.get("sell", 0) if isinstance(r, dict) else 0) or 0)

    def _name(r):
        return r.bank_name if hasattr(r, "bank_name") else r.get("bank_name", "")

    by_buy = sorted(rates, key=_buy, reverse=True)[:top_n]
    by_sell = sorted([r for r in rates if _sell(r) > 0], key=_sell)[:top_n]

    lines.append(f"<b>{t('banks.buy', lang)}</b>")
    for i, r in enumerate(by_buy, start=1):
        lines.append(f"{i}. {_name(r)} — <b>{fmt_int(_buy(r), lang)}</b> UZS")

    lines.append("")
    lines.append(f"<b>{t('banks.sell', lang)}</b>")
    for i, r in enumerate(by_sell, start=1):
        lines.append(f"{i}. {_name(r)} — <b>{fmt_int(_sell(r), lang)}</b> UZS")

    return "\n".join(lines)


def format_crypto_rates(rates: list, lang: str = "ru") -> str:
    """Форматирует курсы крипты"""
    if not rates:
        return t("crypto.no_data", lang)

    title = t("crypto.title", lang)
    lines = [title, ""]

    def _curr(r):
        return r.currency if hasattr(r, "currency") else r["currency"]

    def _usd(r):
        return float(r.rate_usd) if hasattr(r, "rate_usd") and r.rate_usd else (r.get("rate_usd") if isinstance(r, dict) else None)

    def _uzs(r):
        return float(r.rate_uzs) if hasattr(r, "rate_uzs") else float(r.get("rate_uzs") or 0)

    for r in rates:
        ccy = _curr(r)
        usd = _usd(r)
        uzs = _uzs(r)
        usd_str = f"${fmt_rate(usd, lang)}" if usd else "—"
        uzs_str = f"{fmt_int(uzs, lang)} UZS" if uzs else "—"
        lines.append(f"{_icon(ccy)} <b>{ccy}</b>  {usd_str}  ~  {uzs_str}")

    fetched = None
    for r in rates:
        fa = r.fetched_at if hasattr(r, "fetched_at") else None
        if fa:
            fetched = fa
            break
    if fetched:
        lines.append("")
        lines.append(f"{E['clock']} {fetched.strftime('%d.%m.%Y %H:%M')}")

    return "\n".join(lines)


def format_digest(
    rates: list,
    currencies: list[str],
    lang: str = "ru",
    date: datetime | None = None,
) -> str:
    """Ежедневный дайджест по выбранным валютам"""
    title = t("subscribe.digest_title", lang)
    tz = pytz.timezone(settings.timezone)
    date_str = (date or datetime.now(tz)).strftime("%d.%m.%Y")
    lines = [f"{title} — {date_str}", ""]

    by_ccy = {}
    for r in rates:
        ccy = r.currency if hasattr(r, "currency") else r["currency"]
        by_ccy[ccy] = r

    for ccy in currencies:
        if ccy in by_ccy:
            r = by_ccy[ccy]
            rate = float(r.rate_uzs) if hasattr(r, "rate_uzs") else float(r["rate_uzs"])
            lines.append(f"{_icon(ccy)} <b>{ccy}</b>  {fmt_rate(rate, lang)} UZS")

    return "\n".join(lines)


def format_conversion_result(
    amount: float,
    from_curr: str,
    to_curr: str,
    result: float,
    rate: float,
    lang: str = "ru",
) -> str:
    """100 USD = 1 274 300.00 UZS (курс: 12 743.00)"""
    return t(
        "convert.result",
        lang,
        amount=fmt_rate(amount, lang),
        from_curr=from_curr,
        result=fmt_rate(result, lang),
        to_curr=to_curr,
        rate=fmt_rate(rate, lang),
    )
