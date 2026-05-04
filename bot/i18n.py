"""Мультиязычность — русский, узбекский, английский
Использование: from bot.i18n import t
  t("start.welcome", lang="ru", name="Иван")
"""

from bot.emojis import E

TRANSLATIONS = {
    # === /start ===
    "start.welcome": {
        "ru": (
            f"{E['bot']} <b>Привет, {{name}}!</b>\n\n"
            f"{E['chart']} Я покажу актуальные курсы валют Узбекистана — "
            "ЦБ, банки и криптовалюты.\n\n"
            f"{E['pin']} <b>Что умею:</b>\n"
            "Курсы ЦБ, банков, конвертер, крипта.\n\n"
            "Выбери действие ниже:"
        ),
        "uz": (
            f"{E['bot']} <b>Salom, {{name}}!</b>\n\n"
            f"{E['chart']} Men O'zbekiston valyuta kurslarini ko'rsataman — "
            "Markaziy bank, banklar va kriptovalyutalar.\n\n"
            f"{E['pin']} <b>Nima qila olaman:</b>\n"
            "MB kurslari, banklar, konverter, kripto.\n\n"
            "Quyidagi tugmalardan birini tanlang:"
        ),
        "en": (
            f"{E['bot']} <b>Hello, {{name}}!</b>\n\n"
            f"{E['chart']} I show current exchange rates for Uzbekistan — "
            "Central Bank, commercial banks and crypto.\n\n"
            f"{E['pin']} <b>What I can do:</b>\n"
            "CBU rates, banks, converter, crypto.\n\n"
            "Choose an action below:"
        ),
    },

    # === Кнопки главного меню ===
    "btn.cbu": {
        "ru": "ЦБ Узбекистана",
        "uz": "Markaziy bank",
        "en": "Central Bank",
    },
    "btn.banks": {
        "ru": "Банки",
        "uz": "Banklar",
        "en": "Banks",
    },
    "btn.convert": {
        "ru": "Конвертер",
        "uz": "Konverter",
        "en": "Converter",
    },
    "btn.crypto": {
        "ru": "Крипта",
        "uz": "Kripto",
        "en": "Crypto",
    },
    "btn.settings": {
        "ru": "Настройки",
        "uz": "Sozlamalar",
        "en": "Settings",
    },
    "btn.profile": {
        "ru": "Мой профиль",
        "uz": "Mening profilim",
        "en": "My profile",
    },
    "btn.help": {
        "ru": "Помощь",
        "uz": "Yordam",
        "en": "Help",
    },
    "btn.back": {
        "ru": "Назад",
        "uz": "Orqaga",
        "en": "Back",
    },
    "btn.language": {
        "ru": "Сменить язык",
        "uz": "Tilni o'zgartirish",
        "en": "Change language",
    },
    "btn.check_sub": {
        "ru": "Проверить подписку",
        "uz": "Obunani tekshirish",
        "en": "Check subscription",
    },
    "btn.subscribe": {
        "ru": "Подписаться на дайджест",
        "uz": "Kunlik xabarga obuna bo'lish",
        "en": "Subscribe to digest",
    },
    "btn.unsubscribe": {
        "ru": "Отписаться от дайджеста",
        "uz": "Kunlik xabardan obunani bekor qilish",
        "en": "Unsubscribe from digest",
    },

    # === Профиль ===
    "profile.title": {
        "ru": (
            f"{E['profile']} <b>Твой профиль</b>\n\n"
            f"{E['edit']} Имя: {{full_name}}\n"
            f"{E['info']} ID: <code>{{user_id}}</code>\n"
            f"{E['clock']} Зарегистрирован: {{created_at}}\n"
            f"{E['check']} Дайджест: {{digest_status}}\n"
        ),
        "uz": (
            f"{E['profile']} <b>Sizning profilingiz</b>\n\n"
            f"{E['edit']} Ism: {{full_name}}\n"
            f"{E['info']} ID: <code>{{user_id}}</code>\n"
            f"{E['clock']} Ro'yxatdan o'tgan: {{created_at}}\n"
            f"{E['check']} Kunlik xabar: {{digest_status}}\n"
        ),
        "en": (
            f"{E['profile']} <b>Your profile</b>\n\n"
            f"{E['edit']} Name: {{full_name}}\n"
            f"{E['info']} ID: <code>{{user_id}}</code>\n"
            f"{E['clock']} Registered: {{created_at}}\n"
            f"{E['check']} Digest: {{digest_status}}\n"
        ),
    },
    "profile.digest_on": {
        "ru": "Включён",
        "uz": "Yoqilgan",
        "en": "Enabled",
    },
    "profile.digest_off": {
        "ru": "Выключен",
        "uz": "O'chirilgan",
        "en": "Disabled",
    },

    # === Помощь ===
    "help.text": {
        "ru": (
            f"{E['book']} <b>Помощь</b>\n\n"
            f"{E['star']} /rates — курсы ЦБ Узбекистана\n"
            f"{E['star']} /banks — курсы в банках\n"
            f"{E['star']} /convert — конвертер валют\n"
            f"{E['star']} /crypto — курсы криптовалют\n"
            f"{E['star']} /subscribe — дайджест каждый день\n\n"
            f"{E['plane']} По вопросам: @{{admin_username}}"
        ),
        "uz": (
            f"{E['book']} <b>Yordam</b>\n\n"
            f"{E['star']} /rates — O'zbekiston MB kurslari\n"
            f"{E['star']} /banks — banklardagi kurslar\n"
            f"{E['star']} /convert — valyuta konverteri\n"
            f"{E['star']} /crypto — kriptovalyuta kurslari\n"
            f"{E['star']} /subscribe — har kunlik xabar\n\n"
            f"{E['plane']} Savollar uchun: @{{admin_username}}"
        ),
        "en": (
            f"{E['book']} <b>Help</b>\n\n"
            f"{E['star']} /rates — CBU exchange rates\n"
            f"{E['star']} /banks — commercial bank rates\n"
            f"{E['star']} /convert — currency converter\n"
            f"{E['star']} /crypto — cryptocurrency rates\n"
            f"{E['star']} /subscribe — daily digest\n\n"
            f"{E['plane']} Contact: @{{admin_username}}"
        ),
    },

    # === Подписка на каналы ===
    "sub.welcome": {
        "ru": (
            f"{E['bot']} <b>Привет!</b>\n\n"
            f"{E['chart']} Этот бот показывает курсы валют "
            "Узбекистана — быстро и бесплатно!\n\n"
            f"{E['lock']} <b>Для начала подпишись на каналы ниже:</b>\n\n"
            f"После подписки нажми «{E['check']} Проверить подписку»"
        ),
        "uz": (
            f"{E['bot']} <b>Salom!</b>\n\n"
            f"{E['chart']} Bu bot O'zbekiston valyuta kurslarini "
            "ko'rsatadi — tez va bepul!\n\n"
            f"{E['lock']} <b>Boshlash uchun quyidagi kanallarga obuna bo'ling:</b>\n\n"
            f"Obuna bo'lgandan keyin «{E['check']} Obunani tekshirish» tugmasini bosing"
        ),
        "en": (
            f"{E['bot']} <b>Hello!</b>\n\n"
            f"{E['chart']} This bot shows Uzbekistan exchange rates — "
            "fast and free!\n\n"
            f"{E['lock']} <b>To start, subscribe to the channels below:</b>\n\n"
            f"After subscribing, tap «{E['check']} Check subscription»"
        ),
    },
    "sub.not_subscribed": {
        "ru": (
            f"{E['cross']} <b>Ты ещё не подписался на все каналы:</b>\n\n"
            f"Подпишись и нажми «{E['check']} Проверить подписку» ещё раз."
        ),
        "uz": (
            f"{E['cross']} <b>Siz hali barcha kanallarga obuna bo'lmadingiz:</b>\n\n"
            f"Obuna bo'ling va «{E['check']} Obunani tekshirish» tugmasini qayta bosing."
        ),
        "en": (
            f"{E['cross']} <b>You haven't subscribed to all channels yet:</b>\n\n"
            f"Subscribe and tap «{E['check']} Check subscription» again."
        ),
    },
    "sub.success": {
        "ru": (
            f"{E['check']} <b>Отлично, {{name}}!</b>\n\n"
            f"Теперь ты можешь пользоваться ботом! {E['chart']}\n\n"
            "Выбери действие в меню."
        ),
        "uz": (
            f"{E['check']} <b>Ajoyib, {{name}}!</b>\n\n"
            f"Endi siz botdan foydalanishingiz mumkin! {E['chart']}\n\n"
            "Menyudan amalni tanlang."
        ),
        "en": (
            f"{E['check']} <b>Great, {{name}}!</b>\n\n"
            f"You can now use the bot! {E['chart']}\n\n"
            "Choose an action from the menu."
        ),
    },
    "sub.not_required": {
        "ru": f"{E['check']} Подписка не требуется!",
        "uz": f"{E['check']} Obuna talab qilinmaydi!",
        "en": f"{E['check']} No subscription required!",
    },
    "sub.check_alert_fail": {
        "ru": f"{E['cross']} Подпишись на все каналы!",
        "uz": f"{E['cross']} Barcha kanallarga obuna bo'ling!",
        "en": f"{E['cross']} Subscribe to all channels!",
    },
    "sub.check_alert_ok": {
        "ru": f"{E['check']} Подписка подтверждена!",
        "uz": f"{E['check']} Obuna tasdiqlandi!",
        "en": f"{E['check']} Subscription confirmed!",
    },

    # === Ошибки ===
    "error.generic": {
        "ru": f"{E['cross']} <b>Что-то пошло не так</b>\n\nПопробуй позже.",
        "uz": f"{E['cross']} <b>Nimadir xato ketdi</b>\n\nKeyinroq urinib ko'ring.",
        "en": f"{E['cross']} <b>Something went wrong</b>\n\nPlease try again later.",
    },
    "error.rate_limit": {
        "ru": f"{E['clock']} <b>Слишком много запросов!</b>\n\nПодожди {{seconds}} секунд и попробуй снова.",
        "uz": f"{E['clock']} <b>Juda ko'p so'rovlar!</b>\n\n{{seconds}} soniya kuting va qayta urinib ko'ring.",
        "en": f"{E['clock']} <b>Too many requests!</b>\n\nWait {{seconds}} seconds and try again.",
    },
    "error.not_found": {
        "ru": f"{E['cross']} Данные не найдены.",
        "uz": f"{E['cross']} Ma'lumot topilmadi.",
        "en": f"{E['cross']} Data not found.",
    },

    # === Выбор языка ===
    "lang.choose": {
        "ru": f"{E['gear']} <b>Выберите язык:</b>",
        "uz": f"{E['gear']} <b>Tilni tanlang:</b>",
        "en": f"{E['gear']} <b>Choose language:</b>",
    },
    "lang.changed": {
        "ru": f"{E['check']} Язык изменён на русский",
        "uz": f"{E['check']} Til o'zbek tiliga o'zgartirildi",
        "en": f"{E['check']} Language changed to English",
    },

    # === Администрация ===
    "admin.title": {
        "ru": f"{E['gear']} <b>Админ-панель</b>\n\nВыбери действие:",
        "uz": f"{E['gear']} <b>Admin panel</b>\n\nAmalni tanlang:",
        "en": f"{E['gear']} <b>Admin panel</b>\n\nChoose an action:",
    },
    "admin.no_access": {
        "ru": f"{E['lock']} У тебя нет доступа к админке.",
        "uz": f"{E['lock']} Sizda admin panelga kirish huquqi yo'q.",
        "en": f"{E['lock']} You don't have access to admin panel.",
    },
    "admin.channel_deleted": {
        "ru": f"{E['check']} Канал удалён!",
        "uz": f"{E['check']} Kanal o'chirildi!",
        "en": f"{E['check']} Channel deleted!",
    },
    "admin.channel_not_found": {
        "ru": f"{E['cross']} Канал не найден",
        "uz": f"{E['cross']} Kanal topilmadi",
        "en": f"{E['cross']} Channel not found",
    },
    "admin.no_message": {
        "ru": f"{E['cross']} Нет сообщения",
        "uz": f"{E['cross']} Xabar yo'q",
        "en": f"{E['cross']} No message",
    },
    "admin.stats": {
        "ru": (
            f"{E['chart']} <b>Статистика бота</b>\n\n"
            f"{E['users']} Всего юзеров: <b>{{total_users}}</b>\n"
            f"{E['star']} Новых сегодня: <b>{{today_users}}</b>\n"
            f"{E['check']} Подписаны на дайджест: <b>{{total_downloads}}</b>\n"
            f"{E['megaphone']} Каналов: <b>{{total_channels}}</b>"
        ),
        "uz": (
            f"{E['chart']} <b>Bot statistikasi</b>\n\n"
            f"{E['users']} Jami foydalanuvchilar: <b>{{total_users}}</b>\n"
            f"{E['star']} Bugungi yangilar: <b>{{today_users}}</b>\n"
            f"{E['check']} Kunlik xabarga obunalar: <b>{{total_downloads}}</b>\n"
            f"{E['megaphone']} Kanallar: <b>{{total_channels}}</b>"
        ),
        "en": (
            f"{E['chart']} <b>Bot statistics</b>\n\n"
            f"{E['users']} Total users: <b>{{total_users}}</b>\n"
            f"{E['star']} New today: <b>{{today_users}}</b>\n"
            f"{E['check']} Digest subscribers: <b>{{total_downloads}}</b>\n"
            f"{E['megaphone']} Channels: <b>{{total_channels}}</b>"
        ),
    },
    "admin.channels_empty": {
        "ru": f"{E['megaphone']} <b>Каналы</b>\n\nСписок пуст. Добавь канал кнопкой ниже.",
        "uz": f"{E['megaphone']} <b>Kanallar</b>\n\nRo'yxat bo'sh. Quyidagi tugma orqali kanal qo'shing.",
        "en": f"{E['megaphone']} <b>Channels</b>\n\nList is empty. Add a channel using the button below.",
    },
    "admin.channels_title": {
        "ru": f"{E['megaphone']} <b>Каналы для подписки:</b>\n",
        "uz": f"{E['megaphone']} <b>Obuna kanallari:</b>\n",
        "en": f"{E['megaphone']} <b>Subscription channels:</b>\n",
    },
    "admin.add_channel_id": {
        "ru": (
            f"{E['megaphone']} <b>Добавление канала</b>\n\n"
            "Отправь <b>ID канала</b> (например <code>-1001234567890</code>)\n\n"
            f"{E['bulb']} Узнать ID: добавь бота @getmyid_bot в канал"
        ),
        "uz": (
            f"{E['megaphone']} <b>Kanal qo'shish</b>\n\n"
            "<b>Kanal ID</b> raqamini yuboring (masalan <code>-1001234567890</code>)\n\n"
            f"{E['bulb']} ID bilish: @getmyid_bot ni kanalga qo'shing"
        ),
        "en": (
            f"{E['megaphone']} <b>Add channel</b>\n\n"
            "Send the <b>channel ID</b> (e.g. <code>-1001234567890</code>)\n\n"
            f"{E['bulb']} Get ID: add @getmyid_bot to the channel"
        ),
    },
    "admin.add_channel_title": {
        "ru": f"{E['edit']} Теперь отправь <b>название канала</b>:",
        "uz": f"{E['edit']} Endi <b>kanal nomini</b> yuboring:",
        "en": f"{E['edit']} Now send the <b>channel name</b>:",
    },
    "admin.add_channel_link": {
        "ru": (
            f"{E['link']} Теперь отправь <b>ссылку или юзернейм канала</b>\n\n"
            "Принимаю любой формат:\n"
            "• <code>https://t.me/your_channel</code>\n"
            "• <code>@your_channel</code>\n"
            "• <code>your_channel</code>"
        ),
        "uz": (
            f"{E['link']} Endi <b>kanal havolasi yoki username</b> yuboring\n\n"
            "Istalgan formatda:\n"
            "• <code>https://t.me/your_channel</code>\n"
            "• <code>@your_channel</code>\n"
            "• <code>your_channel</code>"
        ),
        "en": (
            f"{E['link']} Now send the <b>channel link or username</b>\n\n"
            "Any format accepted:\n"
            "• <code>https://t.me/your_channel</code>\n"
            "• <code>@your_channel</code>\n"
            "• <code>your_channel</code>"
        ),
    },
    "admin.channel_added": {
        "ru": f"{E['check']} <b>Канал добавлен!</b>",
        "uz": f"{E['check']} <b>Kanal qo'shildi!</b>",
        "en": f"{E['check']} <b>Channel added!</b>",
    },
    "admin.confirm_delete": {
        "ru": f"{E['warning']} <b>Удалить канал?</b>\n\nID: <code>{{channel_id}}</code>\n\nЭто действие нельзя отменить.",
        "uz": f"{E['warning']} <b>Kanalni o'chirishni xohlaysizmi?</b>\n\nID: <code>{{channel_id}}</code>\n\nBu amalni qaytarib bo'lmaydi.",
        "en": f"{E['warning']} <b>Delete channel?</b>\n\nID: <code>{{channel_id}}</code>\n\nThis action cannot be undone.",
    },
    "admin.id_not_number": {
        "ru": f"{E['cross']} ID должен быть числом. Попробуй ещё раз:",
        "uz": f"{E['cross']} ID raqam bo'lishi kerak. Qayta urinib ko'ring:",
        "en": f"{E['cross']} ID must be a number. Try again:",
    },
    "admin.title_too_long": {
        "ru": f"{E['cross']} Название слишком длинное (макс 200 символов)",
        "uz": f"{E['cross']} Nom juda uzun (maks 200 belgi)",
        "en": f"{E['cross']} Name is too long (max 200 characters)",
    },
    "admin.link_invalid": {
        "ru": f"{E['cross']} Не удалось распознать ссылку.\nПопробуй ещё:",
        "uz": f"{E['cross']} Havolani aniqlab bo'lmadi.\nQayta urinib ko'ring:",
        "en": f"{E['cross']} Could not parse the link.\nTry again:",
    },

    # === Кнопки ===
    "btn.admin_stats": {"ru": "Статистика", "uz": "Statistika", "en": "Statistics"},
    "btn.admin_channels": {"ru": "Каналы", "uz": "Kanallar", "en": "Channels"},
    "btn.admin_home": {"ru": "Главное меню", "uz": "Bosh menyu", "en": "Main menu"},
    "btn.admin_add": {"ru": "Добавить канал", "uz": "Kanal qo'shish", "en": "Add channel"},
    "btn.admin_back": {"ru": "Назад", "uz": "Orqaga", "en": "Back"},
    "btn.admin_cancel": {"ru": "Отмена", "uz": "Bekor qilish", "en": "Cancel"},
    "btn.admin_confirm_del": {"ru": "Да, удалить", "uz": "Ha, o'chirish", "en": "Yes, delete"},
    "btn.admin_cancel_del": {"ru": "Отмена", "uz": "Bekor qilish", "en": "Cancel"},
    "btn.admin_panel": {"ru": "Админ-панель", "uz": "Admin panel", "en": "Admin panel"},
    "btn.admin_broadcast": {"ru": "Рассылка", "uz": "Xabar yuborish", "en": "Broadcast"},

    # === Рассылка ===
    "admin.broadcast_prompt": {
        "ru": f"{E['plane']} <b>Массовая рассылка</b>\n\nОтправь текст/фото/видео для рассылки.\nПоддерживается HTML.",
        "uz": f"{E['plane']} <b>Ommaviy xabar</b>\n\nYuborish uchun matn/rasm/video yuboring.\nHTML qo'llab-quvvatlanadi.",
        "en": f"{E['plane']} <b>Mass broadcast</b>\n\nSend text/photo/video to broadcast.\nHTML supported.",
    },
    "admin.broadcast_preview": {
        "ru": f"{E['eye']} <b>Предпросмотр</b>\n\nОтправить это сообщение всем юзерам?",
        "uz": f"{E['eye']} <b>Oldindan ko'rish</b>\n\nBu xabarni barcha foydalanuvchilarga yuborishni xohlaysizmi?",
        "en": f"{E['eye']} <b>Preview</b>\n\nSend this message to all users?",
    },
    "admin.broadcast_confirm": {"ru": "Да, отправить", "uz": "Ha, yuborish", "en": "Yes, send"},
    "admin.broadcast_cancel": {"ru": "Отмена", "uz": "Bekor qilish", "en": "Cancel"},
    "admin.broadcast_started": {
        "ru": f"{E['plane']} Рассылка запущена... Ожидай отчёт.",
        "uz": f"{E['plane']} Xabar yuborilmoqda... Hisobotni kuting.",
        "en": f"{E['plane']} Broadcast started... Wait for report.",
    },
    "admin.broadcast_done": {
        "ru": f"{E['chart']} <b>Рассылка завершена!</b>\n\n{E['check']} Доставлено: <b>{{success}}</b>\n{E['cross']} Ошибок: <b>{{failed}}</b>\n{E['users']} Всего: <b>{{total}}</b>",
        "uz": f"{E['chart']} <b>Xabar yuborish tugadi!</b>\n\n{E['check']} Yetkazildi: <b>{{success}}</b>\n{E['cross']} Xatolar: <b>{{failed}}</b>\n{E['users']} Jami: <b>{{total}}</b>",
        "en": f"{E['chart']} <b>Broadcast complete!</b>\n\n{E['check']} Delivered: <b>{{success}}</b>\n{E['cross']} Failed: <b>{{failed}}</b>\n{E['users']} Total: <b>{{total}}</b>",
    },

    # === Описания команд бота (для меню Telegram) ===
    "cmd.start": {"ru": "Запустить бота", "uz": "Botni boshlash", "en": "Start the bot"},
    "cmd.menu": {"ru": "Главное меню", "uz": "Asosiy menyu", "en": "Main menu"},
    "cmd.help": {"ru": "Помощь", "uz": "Yordam", "en": "Help"},
    "cmd.profile": {"ru": "Мой профиль", "uz": "Mening profilim", "en": "My profile"},
    "cmd.language": {"ru": "Сменить язык", "uz": "Tilni o'zgartirish", "en": "Change language"},
    "cmd.rates": {"ru": "Курсы ЦБ", "uz": "MB kurslari", "en": "CBU rates"},
    "cmd.banks": {"ru": "Курсы в банках", "uz": "Banklardagi kurslar", "en": "Bank rates"},
    "cmd.convert": {"ru": "Конвертер валют", "uz": "Valyuta konverteri", "en": "Currency converter"},
    "cmd.usd": {"ru": "Курс доллара", "uz": "Dollar kursi", "en": "USD rate"},
    "cmd.eur": {"ru": "Курс евро", "uz": "Evro kursi", "en": "EUR rate"},
    "cmd.rub": {"ru": "Курс рубля", "uz": "Rubl kursi", "en": "RUB rate"},
    "cmd.crypto": {"ru": "Курсы крипты", "uz": "Kripto kurslari", "en": "Crypto rates"},
    "cmd.subscribe": {"ru": "Дайджест каждый день", "uz": "Har kunlik xabar", "en": "Daily digest"},
    "cmd.unsubscribe": {"ru": "Отписаться от дайджеста", "uz": "Obunani bekor qilish", "en": "Unsubscribe"},
    "cmd.history": {"ru": "История конвертаций", "uz": "Konvertatsiya tarixi", "en": "Conversion history"},

    # === Домен: курсы ЦБ ===
    "rates.title": {
        "ru": f"{E['chart']} <b>Курсы ЦБ Узбекистана</b>",
        "uz": f"{E['chart']} <b>O'zbekiston Markaziy Banki kurslari</b>",
        "en": f"{E['chart']} <b>Central Bank of Uzbekistan rates</b>",
    },
    "rates.no_data": {
        "ru": f"{E['cross']} Нет данных по курсам. Попробуйте позже.",
        "uz": f"{E['cross']} Kurs ma'lumotlari topilmadi. Keyinroq urinib ko'ring.",
        "en": f"{E['cross']} No rate data available. Please try again later.",
    },
    "rates.weekend_note": {
        "ru": f"{E['info']} Курс на пятницу — банки и ЦБ не работают по выходным.",
        "uz": f"{E['info']} Juma kuni kursi — banklar va MB dam olish kunlari ishlamaydi.",
        "en": f"{E['info']} Friday's rate — banks and CBU are closed on weekends.",
    },

    # === Банки ===
    "banks.choose_currency": {
        "ru": f"{E['bot']} <b>Выберите валюту</b> для просмотра курсов в банках:",
        "uz": f"{E['bot']} <b>Valyutani tanlang</b> — banklardagi kurslarni ko'rish uchun:",
        "en": f"{E['bot']} <b>Choose a currency</b> to view bank rates:",
    },
    "banks.title": {
        "ru": f"{E['chart']} <b>Курсы {{currency}} в банках</b>",
        "uz": f"{E['chart']} <b>Banklardagi {{currency}} kursi</b>",
        "en": f"{E['chart']} <b>{{currency}} rates in banks</b>",
    },
    "banks.empty": {
        "ru": f"{E['cross']} Нет данных по банкам, попробуйте позже.",
        "uz": f"{E['cross']} Bank ma'lumotlari topilmadi, keyinroq urinib ko'ring.",
        "en": f"{E['cross']} No bank data available, please try again later.",
    },
    "banks.show_all_btn": {
        "ru": "Все банки",
        "uz": "Barcha banklar",
        "en": "All banks",
    },
    "banks.buy": {
        "ru": "Покупка (best)",
        "uz": "Sotib olish (eng yaxshi)",
        "en": "Buy (best)",
    },
    "banks.sell": {
        "ru": "Продажа (best)",
        "uz": "Sotish (eng yaxshi)",
        "en": "Sell (best)",
    },

    # === Конвертер ===
    "convert.usage": {
        "ru": (
            f"{E['info']} <b>Использование:</b>\n"
            "<code>/convert 100 USD EUR</code>\n\n"
            "Или используйте кнопки ниже."
        ),
        "uz": (
            f"{E['info']} <b>Foydalanish:</b>\n"
            "<code>/convert 100 USD EUR</code>\n\n"
            "Yoki quyidagi tugmalardan foydalaning."
        ),
        "en": (
            f"{E['info']} <b>Usage:</b>\n"
            "<code>/convert 100 USD EUR</code>\n\n"
            "Or use the buttons below."
        ),
    },
    "convert.invalid": {
        "ru": f"{E['cross']} Некорректный формат. Пример: <code>/convert 100 USD UZS</code>",
        "uz": f"{E['cross']} Noto'g'ri format. Namuna: <code>/convert 100 USD UZS</code>",
        "en": f"{E['cross']} Invalid format. Example: <code>/convert 100 USD UZS</code>",
    },
    "convert.result": {
        "ru": (
            f"{E['refresh']} <b>{{amount}} {{from_curr}} = "
            "{result} {to_curr}</b>\n\n"
            f"{E['chart']} Курс: {{rate}}"
        ),
        "uz": (
            f"{E['refresh']} <b>{{amount}} {{from_curr}} = "
            "{result} {to_curr}</b>\n\n"
            f"{E['chart']} Kurs: {{rate}}"
        ),
        "en": (
            f"{E['refresh']} <b>{{amount}} {{from_curr}} = "
            "{result} {to_curr}</b>\n\n"
            f"{E['chart']} Rate: {{rate}}"
        ),
    },
    "convert.choose_from": {
        "ru": f"{E['refresh']} <b>Из какой валюты</b> конвертируем?",
        "uz": f"{E['refresh']} <b>Qaysi valyutadan</b> konvertatsiya qilamiz?",
        "en": f"{E['refresh']} <b>Convert from</b> which currency?",
    },
    "convert.choose_to": {
        "ru": f"{E['refresh']} <b>В какую валюту</b> конвертируем?",
        "uz": f"{E['refresh']} <b>Qaysi valyutaga</b> konvertatsiya qilamiz?",
        "en": f"{E['refresh']} <b>Convert to</b> which currency?",
    },
    "convert.enter_amount": {
        "ru": f"{E['edit']} Введите <b>сумму</b> для конвертации:",
        "uz": f"{E['edit']} Konvertatsiya uchun <b>miqdorni</b> kiriting:",
        "en": f"{E['edit']} Enter the <b>amount</b> to convert:",
    },
    "convert.same_currency": {
        "ru": f"{E['cross']} Валюты должны отличаться.",
        "uz": f"{E['cross']} Valyutalar har xil bo'lishi kerak.",
        "en": f"{E['cross']} Currencies must be different.",
    },
    "convert.no_rate": {
        "ru": f"{E['cross']} Нет курса для одной из валют. Попробуйте позже.",
        "uz": f"{E['cross']} Valyutalardan biri uchun kurs topilmadi. Keyinroq urinib ko'ring.",
        "en": f"{E['cross']} No rate found for one of the currencies. Please try again later.",
    },

    # === Крипта ===
    "crypto.title": {
        "ru": f"{E['lightning']} <b>Курсы криптовалют</b>",
        "uz": f"{E['lightning']} <b>Kriptovalyuta kurslari</b>",
        "en": f"{E['lightning']} <b>Cryptocurrency rates</b>",
    },
    "crypto.no_data": {
        "ru": f"{E['cross']} Нет данных по крипте, попробуйте позже.",
        "uz": f"{E['cross']} Kripto ma'lumotlari topilmadi, keyinroq urinib ko'ring.",
        "en": f"{E['cross']} No crypto data available, please try again later.",
    },
    "crypto.updated": {
        "ru": f"{E['clock']} Обновлено: {{time}}",
        "uz": f"{E['clock']} Yangilangan: {{time}}",
        "en": f"{E['clock']} Updated: {{time}}",
    },

    # === Подписка ===
    "subscribe.on": {
        "ru": f"{E['check']} <b>Вы подписались на ежедневный дайджест!</b>\n\nКурсы будут приходить каждое утро.",
        "uz": f"{E['check']} <b>Kunlik xabarga obuna bo'ldingiz!</b>\n\nKurslar har kuni ertalab yuboriladi.",
        "en": f"{E['check']} <b>You've subscribed to the daily digest!</b>\n\nRates will be sent every morning.",
    },
    "subscribe.off": {
        "ru": f"{E['check']} Вы отписались от дайджеста.",
        "uz": f"{E['check']} Kunlik xabardan obunangiz bekor qilindi.",
        "en": f"{E['check']} You've unsubscribed from the digest.",
    },
    "subscribe.digest_title": {
        "ru": f"{E['chart']} <b>Дайджест курсов</b>",
        "uz": f"{E['chart']} <b>Kurslar digesti</b>",
        "en": f"{E['chart']} <b>Rates digest</b>",
    },
    "subscribe.already": {
        "ru": f"{E['info']} Вы уже подписаны.",
        "uz": f"{E['info']} Siz allaqachon obuna bo'lgansiz.",
        "en": f"{E['info']} You're already subscribed.",
    },
    "subscribe.settings": {
        "ru": f"{E['gear']} <b>Настройки дайджеста</b>",
        "uz": f"{E['gear']} <b>Digest sozlamalari</b>",
        "en": f"{E['gear']} <b>Digest settings</b>",
    },

    # === История ===
    "history.title": {
        "ru": f"{E['book']} <b>История конвертаций</b>",
        "uz": f"{E['book']} <b>Konvertatsiyalar tarixi</b>",
        "en": f"{E['book']} <b>Conversion history</b>",
    },
    "history.empty": {
        "ru": f"{E['info']} У вас ещё нет конвертаций.",
        "uz": f"{E['info']} Sizda hali konvertatsiyalar yo'q.",
        "en": f"{E['info']} You have no conversions yet.",
    },
    "history.item": {
        "ru": "{date} — {amount} {from_curr} → <b>{result} {to_curr}</b>",
        "uz": "{date} — {amount} {from_curr} → <b>{result} {to_curr}</b>",
        "en": "{date} — {amount} {from_curr} → <b>{result} {to_curr}</b>",
    },

    # === Inline ===
    "inline.convert_title": {
        "ru": "{amount} {from_curr} = {result} {to_curr}",
        "uz": "{amount} {from_curr} = {result} {to_curr}",
        "en": "{amount} {from_curr} = {result} {to_curr}",
    },
    "inline.convert_description": {
        "ru": "Курс ЦБ: {rate}",
        "uz": "MB kursi: {rate}",
        "en": "CBU rate: {rate}",
    },
    "inline.error": {
        "ru": "Не удалось распарсить запрос. Пример: 100 USD EUR",
        "uz": "So'rovni o'qib bo'lmadi. Namuna: 100 USD EUR",
        "en": "Could not parse the request. Example: 100 USD EUR",
    },

    # === Ошибки API ===
    "error.api_unavailable": {
        "ru": f"{E['cross']} Источник данных временно недоступен. Попробуйте позже.",
        "uz": f"{E['cross']} Ma'lumot manbai vaqtincha mavjud emas. Keyinroq urinib ko'ring.",
        "en": f"{E['cross']} Data source is temporarily unavailable. Please try again later.",
    },
}


def t(key: str, lang: str = "ru", **kwargs) -> str:
    """Получить перевод по ключу и языку"""
    translations = TRANSLATIONS.get(key, {})
    text = translations.get(lang, translations.get("ru", f"[{key}]"))
    if kwargs:
        text = text.format(**kwargs)
    return text


_HTML_TAG_RE = __import__("re").compile(r"<[^>]+>")


def t_plain(key: str, lang: str = "ru", **kwargs) -> str:
    """Перевод без HTML-тегов — для callback.answer (toast/alert не парсит HTML)."""
    return _HTML_TAG_RE.sub("", t(key, lang, **kwargs))


def detect_language(language_code: str | None) -> str:
    """Определяет язык по Telegram: ru → русский, uz → узбекский, остальное → английский"""
    if not language_code:
        return "en"
    if language_code.startswith("ru"):
        return "ru"
    if language_code.startswith("uz"):
        return "uz"
    return "en"
