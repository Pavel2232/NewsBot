import textwrap
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from loguru import logger

from bot.callback_factory import MenuCallbackData, PaginationCallbackData, CurrencyNewsCallbackData, \
    LikeCommentCallbackData, WriteCommentCallbackData, PaginationCommentCallbackData
from bot.keyboards.inline import get_start_buttons, get_news_buttons, comment_like_buttons, add_comment_buttons
from bot.pagination import paginate_markup, paginate_comment
from bot.service_async import get_all_comments_by_news
from bot.state_group import UserStart, WorkWithNews
from news.models import TgUser, News, Like, Comment

news_router = Router(name=__name__)


@news_router.callback_query(MenuCallbackData().filter(F.see_news))
async def see_news(
        call: CallbackQuery,
        callback_data: MenuCallbackData,
        state: FSMContext):
    await state.set_state(WorkWithNews.see_news)

    await call.message.edit_text(
        textwrap.dedent(
            'Новости'
        ),
        reply_markup=await paginate_markup(
            markup=await get_news_buttons(callback_data.page),
            page=callback_data.page
        )
    )


@news_router.callback_query(PaginationCallbackData.filter())
async def pagination_news(
        call: CallbackQuery,
        callback_data: PaginationCallbackData
):
    await call.message.edit_reply_markup(
        reply_markup=await paginate_markup(
            markup=await get_news_buttons(page=callback_data.page),
            page=callback_data.page
        )
    )


@news_router.callback_query(CurrencyNewsCallbackData.filter())
async def currency_news(
        call: CallbackQuery,
        callback_data: CurrencyNewsCallbackData
):
    news: News = await News.objects.filter(id=callback_data.id).afirst()
    if news:
        await call.message.edit_text(
            text=textwrap.dedent(news.text),
            reply_markup=await comment_like_buttons(
                id_news=news.id,
                page=callback_data.page
            ),
        )


@news_router.callback_query(LikeCommentCallbackData.filter(F.like))
async def like_news(
        call: CallbackQuery,
        callback_data: LikeCommentCallbackData
):
    news: News = await News.objects.filter(id=callback_data.id).afirst()
    user: TgUser = await TgUser.objects.filter(telegram_id=call.from_user.id).afirst()
    if news:
        like, created = await Like.objects.aget_or_create(
            owner=user,
            news=news,
        )

        if not created:
            if like.like:
                like.like = False
            else:
                like.like = True

            await like.asave()

        await call.message.edit_reply_markup(
            reply_markup=await comment_like_buttons(
                id_news=news.id,
                page=callback_data.page
            ),
        )


@news_router.callback_query(LikeCommentCallbackData.filter(F.comment))
async def comment_news(
        call: CallbackQuery,
        callback_data: LikeCommentCallbackData,
        state: FSMContext
):
    await state.set_state(WorkWithNews.see_comment)

    comments = await get_all_comments_by_news(id_news=callback_data.id)

    await state.update_data(id_news=callback_data.id)

    if comments:
        comment = comments[0:1]
        logger.info(comment)
        await call.message.edit_text(
            text=textwrap.dedent(
                f'''
От {comment[0].owner_name}

{comment[0].text}
'''
            ),
            reply_markup=await paginate_comment(
                comments=comments,
                id_news=callback_data.id,
            )
        )
    else:
        await call.message.edit_text(
            text='Нет комментариев',
            reply_markup=add_comment_buttons(id_news=callback_data.id)
        )


@news_router.callback_query(PaginationCommentCallbackData.filter())
async def comment_news_pagination(
        call: CallbackQuery,
        callback_data: PaginationCommentCallbackData,
        state: FSMContext
):
    await state.set_state(WorkWithNews.see_comment)

    comments = await get_all_comments_by_news(id_news=callback_data.id)

    await state.update_data(id_news=callback_data.id)
    logger.info(callback_data)

    if comments:

        comment = comments[callback_data.start_index + 1:callback_data.end_index + 1]
        try:
            await call.message.edit_text(
                text=textwrap.dedent(
                    f'''
        От {comment[0].owner_name}

        {comment[0].text}
        '''
                ),
                reply_markup=await paginate_comment(
                    comments=comments,
                    id_news=callback_data.id,
                    page=callback_data.page
                )
            )
        except TelegramBadRequest:
            callback_data.page += 1


@news_router.callback_query(WriteCommentCallbackData.filter())
async def write_comment_news(
        call: CallbackQuery,
        state: FSMContext
):
    await state.set_state(WorkWithNews.write_comment)

    await call.message.answer(
        textwrap.dedent('Введите комментарий')
    )


@news_router.message(WorkWithNews.write_comment)
async def create_comment_news(
        message: Message,
        state: FSMContext
):
    data_state = await state.get_data()
    text_comment = message.text
    owner: TgUser = await TgUser.objects.filter(telegram_id=message.from_user.id).afirst()
    news: News = await News.objects.filter(id=data_state.get('id_news')).afirst()

    if news:
        comment = await Comment.objects.acreate(
            owner=owner,
            news=news
        )

        comment.text = text_comment

        await comment.asave()

        await message.answer(
            textwrap.dedent('Написать ещё 1 комментарий?'),
            reply_markup=add_comment_buttons(id_news=data_state.get('id_news'))
        )
        await state.set_state(WorkWithNews.see_news)
    else:

        await message.answer(
            textwrap.dedent('К сожалению новость была удалена'),
            reply_markup=get_start_buttons()
        )

        await state.set_state(UserStart.menu)
