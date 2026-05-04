# bot_4_rates_uz

Telegram-бот для отслеживания курсов валют Узбекистана.

**Возможности:**
- Курсы ЦБ Узбекистана (CBU) в реальном времени
- Курсы в коммерческих банках (покупка/продажа)
- Конвертер валют
- Графики динамики курсов (matplotlib)
- Курсы криптовалют (CoinGecko)
- Алерты: уведомление когда курс достигает порога
- Ежедневный дайджест в выбранное время
- Три языка: русский, узбекский, английский

## Стек

- Python 3.12 + aiogram 3.26
- PostgreSQL 16 + SQLAlchemy 2 + Alembic
- httpx (API запросы)
- matplotlib (графики)
- Local Bot API (порт 8084)

## Быстрый старт

```bash
cd /home/ulugbek/telegram_bots/tg_bots/bot_4_rates_uz
cp .env.example .env
# Заполнить BOT_TOKEN, DB_PASSWORD, ADMIN_IDS в .env
docker compose up -d --build
```

## Структура

```
bot/               — исходный код
  handlers/        — хендлеры команд и callback
  services/        — бизнес-логика (API, планировщик, форматтер)
  database/        — модели и CRUD
  middlewares/     — подписка, rate limit
  keyboards/       — inline-клавиатуры
alembic/           — миграции БД
docker-compose.yml — сервисы: bot, bot-api, postgres, autoheal
Dockerfile         — образ бота (python:3.12-slim + matplotlib deps)
```

## Команды бота

| Команда | Описание |
|---------|----------|
| /start | Главное меню |
| /rates | Курсы ЦБ |
| /banks | Курсы в банках |
| /usd, /eur, /rub | Быстрый курс |
| /convert | Конвертер |
| /chart | График курса |
| /crypto | Криптовалюты |
| /alerts | Алерты на курс |
| /subscribe | Дайджест ежедневно |
| /history | История конвертаций |

## Переменные окружения

Смотри `.env.example`. Ключевые:

```
BOT_TOKEN=         — токен от @BotFather
DB_PASSWORD=       — пароль PostgreSQL
ADMIN_IDS=         — ID администраторов (через запятую)
TIMEZONE=Asia/Tashkent
CBU_REFRESH_MIN=60
CRYPTO_REFRESH_MIN=5
```
