"""Inline-клавиатуры — главное меню, подписка, язык"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import settings
from bot.emojis import E_ID
from bot.i18n import t


def get_main_menu(lang: str = "ru", user_id: int = 0) -> InlineKeyboardMarkup:
    """Главное меню бота — курсы валют Узбекистана.

    Раскладка:
    [💵 ЦБ Узбекистана] [🏦 Банки]
    [💱 Конвертер]      [🪙 Крипта]
    [⚙️ Настройки]
    + [Админ-панель] для админов
    """
    buttons = [
        [
            InlineKeyboardButton(
                text=t("btn.cbu", lang),
                callback_data="rates_cbu",
                style="primary",
                icon_custom_emoji_id=E_ID["star"],
            ),
            InlineKeyboardButton(
                text=t("btn.banks", lang),
                callback_data="rates_banks",
                style="primary",
                icon_custom_emoji_id=E_ID["users"],
            ),
        ],
        [
            InlineKeyboardButton(
                text=t("btn.convert", lang),
                callback_data="rates_convert",
                style="primary",
                icon_custom_emoji_id=E_ID["refresh"],
            ),
            InlineKeyboardButton(
                text=t("btn.crypto", lang),
                callback_data="rates_crypto",
                style="primary",
                icon_custom_emoji_id=E_ID["lightning"],
            ),
        ],
        [
            InlineKeyboardButton(
                text=t("btn.settings", lang),
                callback_data="rates_settings",
                style="success",
                icon_custom_emoji_id=E_ID["gear"],
            ),
        ],
        [
            InlineKeyboardButton(
                text=t("btn.profile", lang),
                callback_data="my_profile",
                style="success",
                icon_custom_emoji_id=E_ID["profile"],
            ),
            InlineKeyboardButton(
                text=t("btn.help", lang),
                callback_data="help",
                style="success",
                icon_custom_emoji_id=E_ID["info"],
            ),
            InlineKeyboardButton(
                text=t("btn.language", lang),
                callback_data="change_language",
                style="success",
                icon_custom_emoji_id=E_ID["gear"],
            ),
        ],
    ]

    # кнопка админки для админов
    if user_id and user_id in settings.admin_id_list:
        buttons.append([InlineKeyboardButton(
            text=t("btn.admin_panel", lang),
            callback_data="admin_panel",
            style="danger",
            icon_custom_emoji_id=E_ID["lock"],
        )])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# алиас для совместимости с start.py (get_start_keyboard)
def get_start_keyboard(user_id: int = 0, lang: str = "ru") -> InlineKeyboardMarkup:
    """Алиас get_main_menu для совместимости с хендлером /start"""
    return get_main_menu(lang=lang, user_id=user_id)


def get_back_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Кнопка 'Назад' в главное меню"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t("btn.back", lang),
            callback_data="back_to_menu",
            style="success",
            icon_custom_emoji_id=E_ID["back"],
        )],
    ])


def get_subscription_keyboard(
    channels: list[dict], lang: str = "ru"
) -> InlineKeyboardMarkup:
    """Клавиатура подписки на каналы"""
    buttons = []
    for ch in channels:
        buttons.append([InlineKeyboardButton(
            text=f"{ch['title']}",
            url=ch["invite_link"],
            style="primary",
            icon_custom_emoji_id=E_ID["megaphone"],
        )])
    buttons.append([InlineKeyboardButton(
        text=t("btn.check_sub", lang),
        callback_data="check_subscription",
        style="success",
        icon_custom_emoji_id=E_ID["check"],
    )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора языка"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Русский",
                callback_data="set_lang_ru",
                style="primary",
                icon_custom_emoji_id=E_ID["flag_ru"],
            ),
            InlineKeyboardButton(
                text="O'zbek",
                callback_data="set_lang_uz",
                style="primary",
                icon_custom_emoji_id=E_ID["flag_uz"],
            ),
            InlineKeyboardButton(
                text="English",
                callback_data="set_lang_en",
                style="primary",
                icon_custom_emoji_id=E_ID["flag_gb"],
            ),
        ],
    ])
