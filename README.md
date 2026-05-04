# Telegram UZ Rates Bot

Telegram-бот для отслеживания курсов валют Узбекистана.

**Возможности:**
- Курсы ЦБ Узбекистана (CBU) в реальном времени
- Курсы в коммерческих банках (покупка/продажа) с bank.uz
- Конвертер валют
- Курсы криптовалют (CoinGecko, пересчёт в UZS через ЦБ)
- Ежедневный дайджест в выбранное время
- Inline-режим: `@bot 100 USD EUR`
- Три языка: русский, узбекский, английский

## Стек

- Python 3.12 + aiogram 3.26
- PostgreSQL 16 + SQLAlchemy 2 + Alembic
- httpx (API запросы)
- Docker Compose

## Быстрый старт

```bash
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
docker-compose.yml — сервисы: bot, postgres, autoheal
Dockerfile         — образ бота (python:3.12-slim)
```

## Команды бота

| Команда | Описание |
|---------|----------|
| /start | Главное меню |
| /rates | Курсы ЦБ |
| /banks | Курсы в банках |
| /usd, /eur, /rub | Быстрый курс одной валюты |
| /convert | Конвертер валют |
| /crypto | Криптовалюты |
| /subscribe | Подписаться на дайджест |
| /unsubscribe | Отписаться |
| /history | История конвертаций |
| /profile | Мой профиль |
| /language | Сменить язык |

## Переменные окружения

Смотри `.env.example`. Ключевые:

```
BOT_TOKEN=         — токен от @BotFather
DB_PASSWORD=       — пароль PostgreSQL
ADMIN_IDS=         — ID администраторов (через запятую)
TIMEZONE=Asia/Tashkent
CBU_REFRESH_MIN=60
BANKS_REFRESH_MIN=30
CRYPTO_REFRESH_MIN=5
DAILY_DIGEST_TIME=09:00
```
