from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callback_factory import MenuCallbackData, CurrencyNewsCallbackData, LikeCommentCallbackData
from bot.service_async import get_all_news


def get_start_buttons() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()

    markup.button(
        text='Смотреть Новости',
        callback_data=MenuCallbackData(
            see_news=True
        )
    )

    markup.button(
        text='Создать Новость',
        callback_data=MenuCallbackData(
            create_news=True
        )
    )

    markup.button(
        text='Редактировать Мои Новости',
        callback_data=MenuCallbackData(
            refacto_news=True
        )
    )

    markup.adjust(1)

    return markup.as_markup()


async def get_news_buttons(page: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()

    news = await get_all_news()

    for novelty in news:
        markup.button(
            text=novelty.title,
            callback_data=CurrencyNewsCallbackData(
                id=novelty.id,
                page=page
            )
        )

    markup.adjust(1)

    return markup.as_markup()


def comment_like_buttons(id_news: int, page: int = 0) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()

    markup.button(
        text='❤️',
        callback_data=LikeCommentCallbackData(
            id=id_news,
            like=True
        )
    )

    markup.button(
        text='💬',
        callback_data=LikeCommentCallbackData(
            id=id_news,
            comment=True
        )
    )

    markup.button(
        text='Назад к новостям',
        callback_data=MenuCallbackData(
            see_news=True,
            page=page
        )
    )

    markup.adjust(2)

    return markup.as_markup()
