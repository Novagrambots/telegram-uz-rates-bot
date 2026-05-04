"""Хендлеры подписки на ежедневный дайджест"""
import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.database import async_session
from bot.database.crud import (
    get_user_language,
    remove_daily_subscriber,
    upsert_daily_subscriber,
)
from bot.i18n import t
from bot.keyboards.inline import get_back_keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("subscribe"))
async def cmd_subscribe(message: Message) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, message.from_user.id)
        await upsert_daily_subscriber(session, message.from_user.id)
    await message.answer(
        t("subscribe.on", lang),
        reply_markup=get_back_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(Command("unsubscribe"))
async def cmd_unsubscribe(message: Message) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, message.from_user.id)
        await remove_daily_subscriber(session, message.from_user.id)
    await message.answer(
        t("subscribe.off", lang),
        reply_markup=get_back_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "rates_settings")
async def cb_settings(callback: CallbackQuery) -> None:
    """Простые настройки — подписка/отписка"""
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    from bot.emojis import E_ID

    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=t("btn.subscribe", lang),
                callback_data="sub_on",
                style="primary",
                icon_custom_emoji_id=E_ID["check"],
            )],
            [InlineKeyboardButton(
                text=t("btn.unsubscribe", lang),
                callback_data="sub_off",
                style="danger",
                icon_custom_emoji_id=E_ID["cross"],
            )],
            [InlineKeyboardButton(
                text=t("btn.back", lang),
                callback_data="back_to_menu",
                style="success",
                icon_custom_emoji_id=E_ID["back"],
            )],
        ]
    )
    text = (
        f"{t('subscribe.settings', lang)}\n\n"
        f"Часовой пояс: <code>Asia/Tashkent</code>\n"
        f"Время дайджеста: <code>09:00</code>"
    )
    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        await callback.message.answer(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "sub_on")
async def cb_sub_on(callback: CallbackQuery) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
        await upsert_daily_subscriber(session, callback.from_user.id)
    try:
        await callback.message.edit_text(
            t("subscribe.on", lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode="HTML",
        )
    except Exception:
        pass
    await callback.answer()


@router.callback_query(F.data == "sub_off")
async def cb_sub_off(callback: CallbackQuery) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
        await remove_daily_subscriber(session, callback.from_user.id)
    try:
        await callback.message.edit_text(
            t("subscribe.off", lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode="HTML",
        )
    except Exception:
        pass
    await callback.answer()
