import textwrap
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from loguru import logger

from bot.callback_factory import MenuCallbackData, PaginationCallbackData, CurrencyNewsCallbackData
from bot.keyboards.inline import get_start_buttons, get_news_buttons, comment_like_buttons
from bot.pagination import paginate_markup
from bot.state_group import UserStart, WorkWithNews
from news.models import TgUser, News

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
            reply_markup=comment_like_buttons(
                id_news=news.id,
                page=callback_data.page
            ),
        )
