"""История конвертаций"""
import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.database import async_session
from bot.database.crud import get_conversion_history, get_user_language
from bot.i18n import t
from bot.keyboards.inline import get_back_keyboard
from bot.services.formatter import fmt_rate

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("history"))
async def cmd_history(message: Message) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, message.from_user.id)
        items = await get_conversion_history(session, message.from_user.id, limit=10)

    if not items:
        await message.answer(
            t("history.empty", lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode="HTML",
        )
        return

    lines = [t("history.title", lang), ""]
    for it in items:
        lines.append(
            t(
                "history.item",
                lang,
                date=it.created_at.strftime("%d.%m %H:%M"),
                amount=fmt_rate(float(it.amount), lang),
                from_curr=it.from_curr,
                result=fmt_rate(float(it.result), lang),
                to_curr=it.to_curr,
            )
        )

    await message.answer(
        "\n".join(lines),
        reply_markup=get_back_keyboard(lang),
        parse_mode="HTML",
    )
