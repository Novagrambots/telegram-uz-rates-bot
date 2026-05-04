"""Хендлеры курсов в банках"""
import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.database import async_session
from bot.database.crud import get_bank_rates, get_user_language
from bot.emojis import E, E_ID
from bot.i18n import t
from bot.keyboards.inline import get_back_keyboard
from bot.services.formatter import format_bank_rates, fmt_int

logger = logging.getLogger(__name__)
router = Router()

CURRENCIES = ["USD", "EUR", "RUB"]

_CCY_FLAG = {
    "USD": "🇺🇸",
    "EUR": "🇪🇺",
    "RUB": "🇷🇺",
    "GBP": "🇬🇧",
    "KZT": "🇰🇿",
    "CNY": "🇨🇳",
    "JPY": "🇯🇵",
    "TRY": "🇹🇷",
    "UZS": "🇺🇿",
}


def _currencies_kb(lang: str) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text=f"{_CCY_FLAG.get(c, '')} {c}".strip(),
                callback_data=f"banks_{c}",
                style="primary",
            )
            for c in CURRENCIES
        ],
        [InlineKeyboardButton(
            text=t("btn.back", lang),
            callback_data="back_to_menu",
            style="success",
            icon_custom_emoji_id=E_ID["back"],
        )],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _all_kb(currency: str, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=t("banks.show_all_btn", lang),
                callback_data=f"banks_{currency}_all",
                style="primary",
                icon_custom_emoji_id=E_ID["users"],
            )],
            [InlineKeyboardButton(
                text=t("btn.back", lang),
                callback_data="rates_banks",
                style="success",
                icon_custom_emoji_id=E_ID["back"],
            )],
        ]
    )


@router.message(Command("banks"))
async def cmd_banks(message: Message) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, message.from_user.id)
    await message.answer(
        t("banks.choose_currency", lang),
        reply_markup=_currencies_kb(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "rates_banks")
async def cb_rates_banks(callback: CallbackQuery) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
    try:
        await callback.message.edit_text(
            t("banks.choose_currency", lang),
            reply_markup=_currencies_kb(lang),
            parse_mode="HTML",
        )
    except Exception:
        await callback.message.answer(
            t("banks.choose_currency", lang),
            reply_markup=_currencies_kb(lang),
            parse_mode="HTML",
        )
    await callback.answer()


@router.callback_query(F.data.regexp(r"^banks_(USD|EUR|RUB)$"))
async def cb_banks_currency(callback: CallbackQuery) -> None:
    currency = callback.data.split("_", 1)[1]
    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
        rates = await get_bank_rates(session, currency)

    if not rates:
        text = t("banks.empty", lang)
        kb = get_back_keyboard(lang)
    else:
        text = format_bank_rates(rates, currency, lang, top_n=5)
        kb = _all_kb(currency, lang)

    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        await callback.message.answer(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.regexp(r"^banks_(USD|EUR|RUB)_all$"))
async def cb_banks_all(callback: CallbackQuery) -> None:
    currency = callback.data.split("_")[1]
    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
        rates = await get_bank_rates(session, currency)

    if not rates:
        text = t("banks.empty", lang)
    else:
        lines = [f"{E['users']} <b>Все банки — {currency}</b>", ""]
        for i, r in enumerate(rates, start=1):
            buy = fmt_int(float(r.rate_buy), lang) if r.rate_buy else "—"
            sell = fmt_int(float(r.rate_sell), lang) if r.rate_sell else "—"
            lines.append(f"{i}. <b>{r.bank_name}</b>: {buy} / {sell}")
        text = "\n".join(lines)
        # обрезаем под лимит Telegram
        if len(text) > 3900:
            text = text[:3900] + "\n..."

    try:
        await callback.message.edit_text(
            text, reply_markup=get_back_keyboard(lang), parse_mode="HTML"
        )
    except Exception:
        await callback.message.answer(
            text, reply_markup=get_back_keyboard(lang), parse_mode="HTML"
        )
    await callback.answer()
