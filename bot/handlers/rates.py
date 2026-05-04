"""Хендлеры курсов ЦБ Узбекистана"""
import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.database import async_session
from bot.database.crud import (
    get_bank_rates,
    get_latest_cbu_rates,
    get_previous_day_cbu_rates,
    get_user_language,
)
from bot.emojis import E, E_ID
from bot.i18n import t
from bot.keyboards.inline import get_back_keyboard
from bot.services.formatter import format_cbu_rates, fmt_int

logger = logging.getLogger(__name__)
router = Router()


def _refresh_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("btn.back", lang),
                    callback_data="back_to_menu",
                    style="success",
                    icon_custom_emoji_id=E_ID["back"],
                ),
            ]
        ]
    )


async def _build_cbu_text(lang: str) -> str:
    async with async_session() as session:
        rates = await get_latest_cbu_rates(session)
        prev = await get_previous_day_cbu_rates(session)
    if not rates:
        return t("rates.no_data", lang)
    return format_cbu_rates(rates, prev, lang)


@router.message(Command("rates"))
async def cmd_rates(message: Message) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, message.from_user.id)
    text = await _build_cbu_text(lang)
    await message.answer(text, reply_markup=get_back_keyboard(lang), parse_mode="HTML")


@router.callback_query(F.data == "rates_cbu")
async def cb_rates_cbu(callback: CallbackQuery) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
    text = await _build_cbu_text(lang)
    try:
        await callback.message.edit_text(
            text, reply_markup=get_back_keyboard(lang), parse_mode="HTML"
        )
    except Exception:
        await callback.message.answer(
            text, reply_markup=get_back_keyboard(lang), parse_mode="HTML"
        )
    await callback.answer()


async def _single_currency_message(currency: str, lang: str) -> str:
    """ЦБ + топ-3 банка"""
    async with async_session() as session:
        cbu = await get_latest_cbu_rates(session)
        bank_rates = await get_bank_rates(session, currency)

    rate = next((float(r.rate_uzs) for r in cbu if r.currency == currency), None)
    if rate is None:
        return t("rates.no_data", lang)

    lines = [f"<b>{currency}/UZS</b> (ЦБ): <b>{fmt_int(rate, lang)}</b> UZS", ""]

    if bank_rates:
        # топ-3 покупка
        by_buy = sorted(
            [r for r in bank_rates if r.rate_buy],
            key=lambda r: float(r.rate_buy),
            reverse=True,
        )[:3]
        lines.append(f"<b>{t('banks.buy', lang)}:</b>")
        for r in by_buy:
            lines.append(f"{E['star']} {r.bank_name} — {fmt_int(float(r.rate_buy), lang)}")

        by_sell = sorted(
            [r for r in bank_rates if r.rate_sell],
            key=lambda r: float(r.rate_sell),
        )[:3]
        if by_sell:
            lines.append("")
            lines.append(f"<b>{t('banks.sell', lang)}:</b>")
            for r in by_sell:
                lines.append(f"{E['star']} {r.bank_name} — {fmt_int(float(r.rate_sell), lang)}")

    return "\n".join(lines)


@router.message(Command("usd"))
async def cmd_usd(message: Message) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, message.from_user.id)
    text = await _single_currency_message("USD", lang)
    await message.answer(text, reply_markup=get_back_keyboard(lang), parse_mode="HTML")


@router.message(Command("eur"))
async def cmd_eur(message: Message) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, message.from_user.id)
    text = await _single_currency_message("EUR", lang)
    await message.answer(text, reply_markup=get_back_keyboard(lang), parse_mode="HTML")


@router.message(Command("rub"))
async def cmd_rub(message: Message) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, message.from_user.id)
    text = await _single_currency_message("RUB", lang)
    await message.answer(text, reply_markup=get_back_keyboard(lang), parse_mode="HTML")
