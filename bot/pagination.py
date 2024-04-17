from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from math import ceil
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.conf import settings
from loguru import logger
from bot.callback_factory import (PaginationCallbackData,
                                  BackCallbackData,
                                  PaginationCommentCallbackData,
                                  CurrencyNewsCallbackData,
                                  WriteCommentCallbackData,
                                  RefactoringNewsCallbackData)


async def paginate_markup(
        markup: InlineKeyboardMarkup,
        page: int = None,
        refacto_news: bool = False,
) -> InlineKeyboardMarkup:
    if refacto_news:
        items_per_page = 1
    else:
        items_per_page = settings.DEFAULT_PAGINATION_BOT

    if not page:
        page = 1

    total_items = len(markup.inline_keyboard)
    total_pages = ceil(total_items / items_per_page)
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    buttons = markup.inline_keyboard[start_index:end_index]
    if refacto_news:
        id_news = 0
        for list_buttons in buttons:
            for inline_button in list_buttons:
                id_news = inline_button.callback_data.split(':')[1]

    pagination_buttons = [
        InlineKeyboardButton(
            text=f'{page}/{total_pages}',
            callback_data='ignore'
        )
    ]

    if page > 1:
        pagination_buttons.insert(
            0, InlineKeyboardButton(
                text='⬅️',
                callback_data=PaginationCallbackData(
                    refacto_news=refacto_news,
                    page=page - 1,
                ).pack()
            )
        )
    else:
        pagination_buttons.insert(0, InlineKeyboardButton(
            text='⬅️',
            callback_data='ignore'
        )
                                  )

    # Next button
    if page < total_pages:
        pagination_buttons.append(
            InlineKeyboardButton(text="➡️",
                                 callback_data=PaginationCallbackData(
                                     page=page + 1,
                                     refacto_news=refacto_news,
                                 ).pack()
                                 )
        )
    else:
        pagination_buttons.append(InlineKeyboardButton(
            text="➡️",
            callback_data="ignore"
        )
        )

    buttons.append(pagination_buttons)

    if refacto_news:
        first_row = []
        two_row = []

        first_row.append(
            InlineKeyboardButton(
                text='Изменить заголовок',
                callback_data=RefactoringNewsCallbackData(
                    id=id_news,
                    change_title=True,
                ).pack()
            ))

        first_row.append(
            InlineKeyboardButton(
                text='Изменить текст',
                callback_data=RefactoringNewsCallbackData(
                    id=id_news,
                    change_text=True
                ).pack()
            )
        )

        two_row.append(
            InlineKeyboardButton(
                text='Удалить новость',
                callback_data=RefactoringNewsCallbackData(
                    id=id_news,
                    delete=True
                ).pack()
            )
        )

        buttons.append(first_row)
        buttons.append(two_row)

        buttons.append(
            [
                InlineKeyboardButton(
                    text='Редактировать комментарии',
                    callback_data=RefactoringNewsCallbackData(
                        id=id_news,
                        delete_comment=True,
                    ).pack()
                )
            ]
        )

        buttons.append(
            [
                InlineKeyboardButton(
                    text='Назад',
                    callback_data=BackCallbackData().pack()
                )
            ]
        )

    else:
        buttons.append([InlineKeyboardButton(
            text="Вернуться в меню",
            callback_data=BackCallbackData().pack()
        )
        ]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def paginate_comment(
        comments: list,
        id_news: int,
        page: int = None,
        id_comment: int = None,
) -> InlineKeyboardMarkup:
    if not page:
        page = 1

    total_items = len(comments)
    total_pages = ceil(total_items / 1)
    start_index = (page - 1) * 1
    end_index = start_index + 1

    pagination_buttons = InlineKeyboardBuilder()
    logger.info(start_index)
    if page > 1:
        pagination_buttons.button(
            text='⬅️', callback_data=PaginationCommentCallbackData(
                page=page - 1,
                start_index=start_index,
                end_index=end_index,
                id=id_news,
            )
        )
    else:
        pagination_buttons.button(
            text='⬅️', callback_data='ignore'
        )

    pagination_buttons.button(
        text=f'{page}/{total_pages}',
        callback_data='ignore'
    )
    # Next button
    if page < total_pages:
        pagination_buttons.button(
            text="➡️",
            callback_data=PaginationCommentCallbackData(
                id=id_news,
                page=page + 1,
                start_index=start_index,
                end_index=end_index,
            )
        )
    else:
        pagination_buttons.button(
            text="➡️",
            callback_data="ignore"
        )

    pagination_buttons.button(
        text='Оставить комментарий',
        callback_data=WriteCommentCallbackData()
    )

    if id_comment:
        pagination_buttons.button(
            text='Удалить комментарий',
            callback_data=RefactoringNewsCallbackData(
                id=id_comment,
                delete_comment=True
            )
        )

    pagination_buttons.button(
        text="Вернуться к новости",
        callback_data=CurrencyNewsCallbackData(
            id=id_news,
        )
    )

    pagination_buttons.adjust(3, 1)

    logger.info(start_index)
    logger.info(end_index)
    return pagination_buttons.as_markup()
