import logging
import os
import db_method
from dotenv import load_dotenv
from middlewares import AccessMiddleware
from aiogram.utils.exceptions import MessageTextIsEmpty
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram import Bot, Dispatcher, executor, types
import menu_buttons as mb
import pars_cbr as cb

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
ACCESS_ID = os.getenv("TELEGRAM_ACCESS")

# Настройка ведения журнала логирования
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))


class AddCategory(StatesGroup):
    category = State()

class DelCategory(StatesGroup):
    category = State()


@dp.message_handler(commands=['start'])
async def welcome_massage(message: types.Message):
    """Этот обработчик будет вызываться, когда пользователь отправляет команду `/start`"""
    answer_message = (
        f'Привет👋\nЯ бот для ведения расходов🧐\n\n'
        f'Для добавления записи введите текст сообщения👇\n'
        f'✅Пример: 350 такси или 189.04 если есть копейки.\n'
        f'✅Сначала пишите сумму (если есть копейки, то пиши через точку), пробел, категорию расходов и нажмите "отправить".\n\n'
        f'О категориях: "Доступные категории"\n'
    )
    await message.answer(answer_message, reply_markup=mb.mainMenu)

# Опрашивает юзера
@dp.message_handler(content_types=['text'], text='➕Добавить категорию')
async def testing(message: types.Message):
    await message.answer(
        'Введите название категории'
    )
    await AddCategory.category.set()

# Добавляет категорию
@dp.message_handler(state=AddCategory.category)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    if answer in db_method.get_category_list():
        await message.answer('Такая категоря уже существует.')
        
        await state.finish()
    else:
        db_method.add_category(answer)
        await state.update_data(answer1=answer)
        data = await state.get_data()
        answer1 = data.get('answer1')
        await message.answer(f'Категория "{answer1}" добавлена.')

        await state.finish()


# Опрашивает юзера
@dp.message_handler(content_types=['text'], text='➖Удалить категорию')
async def testing(message: types.Message):
    await message.answer(
        'Введите название категории'
    )
    await DelCategory.category.set()

# Удаляет категорию
@dp.message_handler(state=DelCategory.category)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    if answer not in db_method.get_category_list():
        await message.answer('Такой категории не существует.')
        
        await state.finish()
    else:
        db_method.del_category(answer)
        await state.update_data(answer2=answer)
        await message.answer(f'Категория "{answer}" удалена.')

        await state.finish()


@dp.message_handler(commands=['del_last'])
async def delete_last_exp(message: types.message.Message):
    """Удаляет последнюю добавленную запись"""
    db_method.delete_last()
    await message.answer('Запись удалена!')


@dp.message_handler(content_types=['text'], text='❔Help')
async def help_massage(message: types.Message):
    """Этот обработчик будет вызываться, когда пользователь нажмёт кнопку help"""
    answer_message = (
        f'Для добавления записи введите его в формате:\n'
        f'Пример: 350 такси\n'
        f'Сначала пишите сумму, пробел, категорию расходов и нажмите "отправить".\n\n'
        f'Удалить последнюю запись: /del_last\n\n'
    )
    await message.answer(answer_message)


@dp.message_handler(content_types=['text'], text='✅Доступные категории')
async def category_list(message: types.Message):
    """Показывает список доступных категорий"""
    try:
        await message.answer(
            db_method.get_category_text()
        )
    except MessageTextIsEmpty:
        await message.answer('Список категорий пуст, добавьте категории.')


@dp.message_handler(content_types=['text'], text='🧾Последние добавленные')
async def last_expanses(message: types.Message):
    """Показывает последние 5 записей в расходы"""
    count_last = len(db_method.last())
    if count_last == 0:
        await message.answer('У вас ещё нет расходов')
    else:
        await message.answer(db_method.last_expense())


@dp.message_handler(content_types=['text'], text='💸Расходы за месяц')
async def month_expanses(message: types.Message):
    """Показывает расходы за месяц"""
    db_method.sum_of_month()
    await message.answer(db_method.sum_of_month())


@dp.message_handler(commands=['del_all'])
async def delete_all(message: types.Message):
    """Удаляет все записи из БД"""
    db_method.delete_all()
    await message.answer('Все записи удалены!')


@dp.message_handler(content_types=['text'], text='📃Расходы по категориям')
async def month_category_stat(message: types.Message):
    """Показывает расходы за месяц по категориям"""
    await message.answer(db_method.sum_of_month_category())


@dp.message_handler(content_types=['text'], text='💸Расходы за сегодня')
async def day_category_stat(message: types.Message):
    """Показывает расходы за сегодняшний день"""
    await message.answer(db_method.sum_of_today())


@dp.message_handler(content_types=['text'], text='📈Курс доллара')
async def usd_price_cb(message: types.Message):
    """Показывает курс доллра"""
    await message.answer(cb.usd_price())


@dp.message_handler()
async def add_expanse(message: types.Message):
    """Добавление записи в БД"""
    try:
        expanses = db_method.parse_msg(message.text)
        check_category = db_method.valid_category(expanses[1])
        if not check_category:
            await message.answer('Нет такой категории\nДоступные категории⤵️')
            await message.answer(db_method.get_category_text())
        else:
            db_method.write_on_db(expanses)
            answer_message = (
                f'Расходы добавлены:\nСумма: {expanses[0]}р.\nКатегория: {expanses[1]}\n\n'
            )
            await message.answer(answer_message)
    except ValueError:
        await message.answer(
            'Не понял тебя, проверь правильность ввода:\n'
            'Пример: 350 еда\n\n'
            'О категориях⤵️',
            reply_markup=mb.inline_kb
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
