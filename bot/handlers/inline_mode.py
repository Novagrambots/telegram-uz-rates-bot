"""Inline-режим конвертера: @bot 100 USD [EUR]"""
import logging
import re
import uuid

from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from bot.database import async_session
from bot.database.crud import get_latest_cbu_rates, get_user_language
from bot.emojis import E
from bot.i18n import t
from bot.services.formatter import fmt_rate

logger = logging.getLogger(__name__)
router = Router()

SUPPORTED = {"UZS", "USD", "EUR", "RUB", "GBP", "CNY", "KZT", "JPY", "TRY"}
DEFAULT_TARGETS = ["UZS", "EUR", "RUB"]

QUERY_RE = re.compile(
    r"^\s*([\d\s.,]+)\s+([A-Za-z]{3})(?:\s+([A-Za-z]{3}))?\s*$"
)


@router.inline_query()
async def inline_convert(query: InlineQuery) -> None:
    """Парсит '100 USD [EUR]' и отдаёт результаты конвертации по ЦБ"""
    text = query.query or ""
    async with async_session() as session:
        lang = await get_user_language(session, query.from_user.id)
        cbu = await get_latest_cbu_rates(session)

    rate_map = {s.currency: float(s.rate_uzs) for s in cbu}
    rate_map["UZS"] = 1.0

    m = QUERY_RE.match(text)
    if not m:
        # пустой результат с подсказкой
        await query.answer(
            results=[
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=t("inline.error", lang),
                    description="Пример: 100 USD EUR",
                    input_message_content=InputTextMessageContent(
                        message_text=t("inline.error", lang)
                    ),
                )
            ],
            cache_time=10,
            is_personal=True,
        )
        return

    try:
        amount_str = m.group(1).replace(" ", "").replace(",", ".")
        amount = float(amount_str)
    except ValueError:
        amount = 0.0

    from_curr = m.group(2).upper()
    to_specific = m.group(3)
    to_specific = to_specific.upper() if to_specific else None

    if from_curr not in rate_map or amount <= 0:
        await query.answer(
            results=[
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=t("inline.error", lang),
                    description=f"{from_curr} недоступна",
                    input_message_content=InputTextMessageContent(
                        message_text=t("inline.error", lang)
                    ),
                )
            ],
            cache_time=10,
            is_personal=True,
        )
        return

    targets = [to_specific] if to_specific else DEFAULT_TARGETS
    targets = [c for c in targets if c in rate_map and c != from_curr]

    results = []
    for to in targets:
        amount_uzs = amount * rate_map[from_curr]
        result = amount_uzs / rate_map[to]
        rate = rate_map[from_curr] / rate_map[to]

        title = t(
            "inline.convert_title",
            lang,
            amount=fmt_rate(amount, lang),
            from_curr=from_curr,
            result=fmt_rate(result, lang),
            to_curr=to,
        )
        descr = t("inline.convert_description", lang, rate=fmt_rate(rate, lang))

        msg_text = (
            f"{E['refresh']} <b>{fmt_rate(amount, lang)} {from_curr}</b> = "
            f"<b>{fmt_rate(result, lang)} {to}</b>\n"
            f"{E['chart']} Курс: {fmt_rate(rate, lang)}"
        )

        results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=title,
                description=descr,
                input_message_content=InputTextMessageContent(
                    message_text=msg_text, parse_mode="HTML"
                ),
            )
        )

    await query.answer(results=results, cache_time=30, is_personal=True)
