import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.storage.redis import RedisStorage
from django.conf import settings
from django.core.management import BaseCommand

from bot.commands import set_commands
from bot.heandlers.news import news_router
from bot.heandlers.start import start_router
from bot.logging_settings.logging import configure_logger


async def on_startup(bot: Bot):
    await set_commands(bot)
    configure_logger(True)


async def main():
    logger = logging.getLogger('Tg')

    logger.info("Starting bot")

    bot = Bot(settings.TG_TOKEN_BOT)

    storage = RedisStorage.from_url(settings.REDIS_URL)

    dp = Dispatcher(storage=storage)

    dp.include_routers(start_router)
    dp.include_routers(news_router)

    try:
        await on_startup(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except TelegramNetworkError:
        logging.critical('Нет интернета')


class Command(BaseCommand):

    def handle(self, *args, **options):
        asyncio.run(main())
