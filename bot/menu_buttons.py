from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# Кнопки для работы с расходами
btnLast = KeyboardButton('🧾Последние добавленные')
btnMonth = KeyboardButton('💸Расходы за месяц')
btnCategoryMonth = KeyboardButton('📃Расходы по категориям')
btnCategories = KeyboardButton('✅Доступные категории')
btnHelp = KeyboardButton('❔Help')
btnUsd = KeyboardButton('📈Курс доллара')
btnSumToday = KeyboardButton('💸Расходы за сегодня')
btnAdd = KeyboardButton('➕Добавить категорию')
btnDel = KeyboardButton('➖Удалить категорию')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnLast, btnSumToday, btnCategories)
mainMenu.row(btnCategoryMonth, btnMonth)
mainMenu.row(btnAdd, btnDel)
mainMenu.row(btnHelp, btnUsd)

# Inline кнопка
btnCategory = InlineKeyboardButton('Список категорий', callback_data='🔸Доступные категории')
inline_kb = InlineKeyboardMarkup().add(btnCategory)

