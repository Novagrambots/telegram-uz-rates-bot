"""Хендлеры курсов криптовалют"""
import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.database import async_session
from bot.database.crud import get_latest_crypto_rates, get_user_language
from bot.i18n import t
from bot.keyboards.inline import get_back_keyboard
from bot.services.formatter import format_crypto_rates

logger = logging.getLogger(__name__)
router = Router()


async def _build_text(lang: str) -> str:
    async with async_session() as session:
        rates = await get_latest_crypto_rates(session)
    if not rates:
        return t("crypto.no_data", lang)
    return format_crypto_rates(rates, lang)


@router.message(Command("crypto"))
async def cmd_crypto(message: Message) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, message.from_user.id)
    text = await _build_text(lang)
    await message.answer(text, reply_markup=get_back_keyboard(lang), parse_mode="HTML")


@router.callback_query(F.data == "rates_crypto")
async def cb_rates_crypto(callback: CallbackQuery) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
    text = await _build_text(lang)
    try:
        await callback.message.edit_text(
            text, reply_markup=get_back_keyboard(lang), parse_mode="HTML"
        )
    except Exception:
        await callback.message.answer(
            text, reply_markup=get_back_keyboard(lang), parse_mode="HTML"
        )
    await callback.answer()
