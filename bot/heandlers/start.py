import textwrap
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from loguru import logger

from bot.keyboards.inline import get_start_buttons
from bot.state_group import UserStart
from news.models import TgUser

start_router = Router(name=__name__)


@start_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    user, _ = await TgUser.objects.aget_or_create(
        telegram_id=message.from_user.id,
    )

    user.username = message.from_user.username

    await user.asave()

    await message.answer(
        textwrap.dedent(
            '''
Добро пожаловать!

Я - ваш личный бот с новостями. Я буду держать вас в курсе последних событий и интересных статей.

Чтобы начать, просто напишите мне "новости" или "статьи", и я пришлю вам список последних новостей.

Если у вас есть вопросы или пожелания, не стесняйтесь задавать их мне!

Желаю приятного чтения!

'''
        ),
        reply_markup=get_start_buttons()
    )

    await state.set_state(UserStart.start)


@start_router.message(F.text == 'Меню')
async def get_menu(message: Message, state: FSMContext):
    await state.set_state(UserStart.menu)
    await message.answer(
        textwrap.dedent(
            '''Меню''',
        ),
        reply_markup=get_start_buttons()
    )
