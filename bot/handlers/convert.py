"""Хендлеры конвертера валют"""
import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.database import async_session
from bot.database.crud import (
    get_latest_cbu_rates,
    get_user_language,
    save_conversion,
)
from bot.emojis import E_ID
from bot.i18n import t, t_plain
from bot.keyboards.inline import get_back_keyboard
from bot.services.formatter import format_conversion_result

logger = logging.getLogger(__name__)
router = Router()

SUPPORTED = ["UZS", "USD", "EUR", "RUB", "GBP", "CNY", "KZT", "JPY", "TRY"]

_CCY_FLAG = {
    "UZS": "🇺🇿",
    "USD": "🇺🇸",
    "EUR": "🇪🇺",
    "RUB": "🇷🇺",
    "GBP": "🇬🇧",
    "CNY": "🇨🇳",
    "KZT": "🇰🇿",
    "JPY": "🇯🇵",
    "TRY": "🇹🇷",
}


class ConvertStates(StatesGroup):
    waiting_from = State()
    waiting_to = State()
    waiting_amount = State()


def _currency_kb(prefix: str, lang: str) -> InlineKeyboardMarkup:
    rows = []
    row = []
    for c in SUPPORTED:
        row.append(InlineKeyboardButton(
            text=f"{_CCY_FLAG.get(c, '')} {c}".strip(),
            callback_data=f"{prefix}_{c}",
            style="primary",
        ))
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton(
        text=t("btn.back", lang),
        callback_data="back_to_menu",
        style="success",
        icon_custom_emoji_id=E_ID["back"],
    )])
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def _build_rate_map() -> dict[str, float]:
    """{currency: rate_to_uzs}. UZS = 1.0"""
    async with async_session() as session:
        cbu = await get_latest_cbu_rates(session)
    rate_map = {s.currency: float(s.rate_uzs) for s in cbu}
    rate_map["UZS"] = 1.0
    return rate_map


async def _do_convert(
    user_id: int,
    amount: float,
    from_curr: str,
    to_curr: str,
    lang: str,
) -> str:
    rate_map = await _build_rate_map()
    if from_curr not in rate_map or to_curr not in rate_map:
        return t("convert.no_rate", lang)

    if from_curr == to_curr:
        return t("convert.same_currency", lang)

    # сумма в UZS
    amount_uzs = amount * rate_map[from_curr]
    # обратно в целевую
    result = amount_uzs / rate_map[to_curr]
    rate_used = rate_map[from_curr] / rate_map[to_curr]

    async with async_session() as session:
        try:
            await save_conversion(
                session,
                user_id=user_id,
                amount=amount,
                from_curr=from_curr,
                to_curr=to_curr,
                result=result,
                rate_used=rate_used,
            )
        except Exception as e:
            logger.warning("save_conversion failed: %s", e)

    return format_conversion_result(amount, from_curr, to_curr, result, rate_used, lang)


@router.message(Command("convert"))
async def cmd_convert(message: Message, state: FSMContext) -> None:
    """/convert 100 USD EUR — мгновенный ответ"""
    async with async_session() as session:
        lang = await get_user_language(session, message.from_user.id)

    args = (message.text or "").split()[1:]
    if len(args) >= 3:
        try:
            amount = float(args[0].replace(",", "."))
            from_curr = args[1].upper()
            to_curr = args[2].upper()
        except ValueError:
            await message.answer(t("convert.invalid", lang), parse_mode="HTML")
            return
        text = await _do_convert(
            message.from_user.id, amount, from_curr, to_curr, lang
        )
        await message.answer(text, reply_markup=get_back_keyboard(lang), parse_mode="HTML")
        return

    # иначе FSM
    await state.set_state(ConvertStates.waiting_from)
    await message.answer(
        t("convert.choose_from", lang),
        reply_markup=_currency_kb("conv_from", lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "rates_convert")
async def cb_rates_convert(callback: CallbackQuery, state: FSMContext) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
    await state.set_state(ConvertStates.waiting_from)
    try:
        await callback.message.edit_text(
            t("convert.choose_from", lang),
            reply_markup=_currency_kb("conv_from", lang),
            parse_mode="HTML",
        )
    except Exception:
        await callback.message.answer(
            t("convert.choose_from", lang),
            reply_markup=_currency_kb("conv_from", lang),
            parse_mode="HTML",
        )
    await callback.answer()


@router.callback_query(ConvertStates.waiting_from, F.data.startswith("conv_from_"))
async def cb_convert_from(callback: CallbackQuery, state: FSMContext) -> None:
    from_curr = callback.data.replace("conv_from_", "")
    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
    await state.update_data(from_curr=from_curr)
    await state.set_state(ConvertStates.waiting_to)
    await callback.message.edit_text(
        t("convert.choose_to", lang),
        reply_markup=_currency_kb("conv_to", lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(ConvertStates.waiting_to, F.data.startswith("conv_to_"))
async def cb_convert_to(callback: CallbackQuery, state: FSMContext) -> None:
    to_curr = callback.data.replace("conv_to_", "")
    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
    data = await state.get_data()
    if data.get("from_curr") == to_curr:
        await callback.answer(t_plain("convert.same_currency", lang), show_alert=True)
        return
    await state.update_data(to_curr=to_curr)
    await state.set_state(ConvertStates.waiting_amount)
    await callback.message.edit_text(
        t("convert.enter_amount", lang),
        reply_markup=get_back_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(ConvertStates.waiting_amount)
async def msg_convert_amount(message: Message, state: FSMContext) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, message.from_user.id)
    try:
        amount = float((message.text or "").replace(",", ".").replace(" ", ""))
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer(t("convert.invalid", lang), parse_mode="HTML")
        return

    data = await state.get_data()
    from_curr = data.get("from_curr")
    to_curr = data.get("to_curr")
    await state.clear()

    text = await _do_convert(message.from_user.id, amount, from_curr, to_curr, lang)
    await message.answer(text, reply_markup=get_back_keyboard(lang), parse_mode="HTML")
