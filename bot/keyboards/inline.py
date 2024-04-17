from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callback_factory import MenuCallbackData


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
