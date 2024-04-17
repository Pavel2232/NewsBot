import textwrap
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from loguru import logger

from bot.callback_factory import MenuCallbackData, PaginationCallbackData, CurrencyNewsCallbackData, \
    LikeCommentCallbackData, WriteCommentCallbackData, PaginationCommentCallbackData, RefactoringNewsCallbackData
from bot.keyboards.inline import get_start_buttons, get_news_buttons, comment_like_buttons, add_comment_buttons, \
    get_back_button, create_more_news_buttons
from bot.pagination import paginate_markup, paginate_comment
from bot.service_async import get_all_comments_by_news, get_all_news_title, get_all_news, get_all_me_news
from bot.state_group import UserStart, WorkWithNews
from news.models import TgUser, News, Like, Comment

news_router = Router(name=__name__)


@news_router.callback_query(MenuCallbackData().filter(F.see_news))
async def see_news(
        call: CallbackQuery,
        callback_data: MenuCallbackData,
        state: FSMContext):
    await state.set_state(WorkWithNews.see_news)
    news = await get_all_news()
    await call.message.edit_text(
        textwrap.dedent(
            'Новости'
        ),
        reply_markup=await paginate_markup(
            markup=await get_news_buttons(page=callback_data.page, news=news),
            page=callback_data.page
        )
    )


@news_router.callback_query(PaginationCallbackData.filter())
async def pagination_news(
        call: CallbackQuery,
        callback_data: PaginationCallbackData
):
    news = await get_all_news()
    await call.message.edit_reply_markup(
        reply_markup=await paginate_markup(
            markup=await get_news_buttons(page=callback_data.page, news=news),
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


@news_router.callback_query(MenuCallbackData.filter(F.create_news))
async def create_news(call: CallbackQuery, state: FSMContext):
    await state.set_state(WorkWithNews.create_news)

    await call.message.edit_text(
        textwrap.dedent('Введите Заголовок статьи'),
        reply_markup=get_back_button()
    )


@news_router.message(WorkWithNews.create_news)
async def get_title_news(message: Message, state: FSMContext):
    await state.set_state(WorkWithNews.write_text_news)

    if len(message.text) > 60:
        return await message.answer(
            textwrap.dedent('Максимальная длинна заголовка 60 символов')
        )

    news_title = await get_all_news_title()

    if message.text in news_title:
        return await message.answer(
            textwrap.dedent(
                'Статья с таким заголовком уже есть, придумайте новый'
            )
        )

    await state.update_data(title_news=message.text)

    await message.answer(
        textwrap.dedent('Введите текст новости')
    )


@news_router.message(WorkWithNews.write_text_news)
async def get_text_news_and_create(message: Message, state: FSMContext):
    await state.set_state(WorkWithNews.success_create_news)

    if len(message.text) > 4095:
        return await message.answer(
            textwrap.dedent('Максимальная длинна текста у статьи 4095 символов')
        )
    data_state = await state.get_data()
    user: TgUser = await TgUser.objects.filter(telegram_id=message.from_user.id).afirst()
    await News.objects.acreate(
        owner=user,
        title=data_state.get('title_news'),
        text=message.text,
    )

    await message.answer(
        textwrap.dedent('Новость успешно создана, хотите создать ещё Новость?'),
        reply_markup=create_more_news_buttons()
    )


@news_router.callback_query(MenuCallbackData.filter(F.refacto_news))
async def refacto_news(
        call: CallbackQuery,
        callback_data: MenuCallbackData,
        state: FSMContext):
    await state.set_state(WorkWithNews.refacto_news)

    news = await get_all_me_news(id_user=call.from_user.id)

    await call.message.edit_text(
        textwrap.dedent(
            'Мои новости'
        ),
        reply_markup=await paginate_markup(
            markup=await get_news_buttons(
                callback_data.page,
                news=news,
            ),
            page=callback_data.page,
            refacto_news=True,

        )
    )


@news_router.callback_query(RefactoringNewsCallbackData.filter(F.change_title))
async def change_title_news(
        call: CallbackQuery,
        callback_data: RefactoringNewsCallbackData,
        state: FSMContext):
    await state.set_state(WorkWithNews.refacto_news)

    news = await News.objects.filter(id=callback_data.id).afirst()
    if news:
        await state.set_state(WorkWithNews.change_title)
        await call.message.edit_text(
            textwrap.dedent(
                'Введите новый заголовок'
            ),
            reply_markup=get_back_button()
        )
        await state.update_data(id_news=news.id)

    else:
        await call.message.edit_text(
            textwrap.dedent(
                'Ваша новость была удалена Администратором'
            ),
            reply_markup=get_start_buttons()
        )


@news_router.message(WorkWithNews.change_title)
async def save_new_title_news(
        message: Message,
        state: FSMContext
):
    data_state = await state.get_data()

    news: News = await News.objects.filter(
        id=data_state.get('id_news'),
        owner__telegram_id=message.from_user.id
    ).afirst()

    logger.info(news)

    if not news:
        return await message.answer(
            textwrap.dedent(
                'Новость либо удалена Администратором, или вы не ее владелец'
            )
        )

    if len(message.text) > 60:
        return await message.answer(
            textwrap.dedent('Максимальная длинна заголовка 60 символов')
        )

    news_title = await get_all_news_title()

    if message.text in news_title:
        return await message.answer(
            textwrap.dedent(
                'Статья с таким заголовком уже есть, придумайте новый'
            )
        )

    news.title = message.text

    await news.asave()
    await state.set_state(WorkWithNews.refacto_news)
    await message.answer(
        textwrap.dedent('Заголовок успешно обновлен'),
        reply_markup=get_back_button()
    )


@news_router.callback_query(RefactoringNewsCallbackData.filter(F.change_text))
async def change_text_news(
        call: CallbackQuery,
        callback_data: RefactoringNewsCallbackData,
        state: FSMContext):
    await state.set_state(WorkWithNews.refacto_news)

    news = await News.objects.filter(
        id=callback_data.id,
        owner__telegram_id=call.from_user.id
    ).afirst()

    if news:
        await state.set_state(WorkWithNews.change_text)
        await call.message.edit_text(
            textwrap.dedent(
                'Введите новый текст'
            ),
            reply_markup=get_back_button()
        )
        await state.update_data(id_news=news.id)
    else:
        await call.message.edit_text(
            textwrap.dedent(
                'Ваша новость была удалена Администратором'
            ),
            reply_markup=get_start_buttons()
        )


@news_router.message(WorkWithNews.change_text)
async def save_new_text_news(
        message: Message,
        state: FSMContext
):
    data_state = await state.get_data()

    news: News = await News.objects.filter(
        id=data_state.get('id_news'),
        owner__telegram_id=message.from_user.id
    ).afirst()

    if not news:
        return await message.answer(
            textwrap.dedent('Новость либо удалена Администратором, или вы не ее владелец')
        )

    if len(message.text) > 4095:
        return await message.answer(
            textwrap.dedent('Максимальная длинна текста у статьи 4095 символов')
        )

    news.text = message.text

    await news.asave()
    await state.set_state(WorkWithNews.refacto_news)
    await message.answer(
        textwrap.dedent('Текст успешно обновлен'),
        reply_markup=get_back_button()
    )

@news_router.callback_query(RefactoringNewsCallbackData().filter(F.delete))
async def del_news(
        call: CallbackQuery,
        callback_data: RefactoringNewsCallbackData,
):
    news: News = await News.objects.filter(
        id=callback_data.id,
        owner__telegram_id=call.from_user.id
    )

    await news.adelete()

    await call.message.answer(
        textwrap.dedent(
            'Новость успешно удалена'
        ),
        reply_markup=get_start_buttons()
    )
