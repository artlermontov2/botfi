import psycopg2
from datetime import datetime
import pytz


conn = psycopg2.connect(
    dbname='name_db', user='postgres',
    password='password',
    host='db', port='5432'
)
cur = conn.cursor()


# Создание таблицы расходов
cur.execute(
    """CREATE TABLE IF NOT EXISTS financial(
    fin_id SERIAL PRIMARY KEY,
    money NUMERIC(8,2) NOT NULL,
    category VARCHAR (255) NOT NULL,
    date TIMESTAMP NOT NULL);"""
)
conn.commit()

# Создание таблицы категорий
cur.execute(
    """CREATE TABLE IF NOT EXISTS categories(
    category VARCHAR (255) NOT NULL);"""
)
conn.commit()

# cur.execute("DROP TABLE financial")
# conn.commit()


def write_on_db(value: tuple):
    """Создание записи в БД"""
    cur.execute('INSERT INTO financial (money, category, date)VALUES (%s, %s, %s)', value)
    conn.commit()


def add_category(text):
    """Добавляет категорию в таблицу"""
    value = (text,)
    cur.execute('INSERT INTO categories (category)VALUES (%s)', value)
    conn.commit()


def get_category_list() -> list:
    """Возвращает список категорий"""

    cur.execute(
        "SELECT * FROM categories"
    )
    result = cur.fetchall()
    list_categories = [i[0] for i in result]
    return list_categories


def get_category_text() -> str:
    """Возвращает категории в виде текста, для сообщения"""
    categories = ''
    for i in get_category_list():
        categories += i + '\n'
    return categories


def read(table: str, columns: list[str]):
    """Чтение из БД"""
    columns_joined = ", ".join(columns)
    cur.execute(f"SELECT {columns_joined} FROM {table}")
    return cur.fetchall()[0][0]


def last() -> list:
    """Возвращает список кортежей с последними 5 записями"""
    cur.execute("SELECT category, money, date FROM financial ORDER BY date DESC LIMIT 5")
    return cur.fetchall()


def last_expense() -> str:
    """Возвращает строку из последних 5 записей"""
    expense = 'Последние внесённые расходы:\n'
    for i in last():
        expense += f'{i[0]} - {str(i[1])}р., дата: {str(i[2])}\n'
    return expense


def delete(row_id: int):
    """Удаляет запись по ID"""
    cur.execute(f"DELETE FROM financial WHERE fin_id={row_id}")
    conn.commit()


def delete_all():
    """Удаляет все записи"""
    cur.execute("DELETE FROM financial")
    conn.commit()


def delete_last():
    """Удаляет последнюю запись"""
    cur.execute("SELECT fin_id FROM financial ORDER BY date DESC LIMIT 1")
    result = cur.fetchall()
    id = result[0][0]
    delete(id)


def del_category(text):
    """Удаляет категорию"""
    cur.execute(f"DELETE FROM categories WHERE category='{text}'")
    conn.commit()


def sum_of_month() -> str:
    """Возвращает сумму расходов за последний месяц"""
    tz = pytz.timezone("Europe/Moscow")
    dt = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    month_now = str(dt.split('-')[1])
    year_now = str(dt.split('-')[0])
    date_now = dt.split(' ')[0]
    cur.execute(
        f"""SELECT SUM (money) 
        FROM financial 
        WHERE date::date >= date '{year_now}-{month_now}-01' AND date::date <= date '{date_now}'""" 
    )
    result = cur.fetchall()
    if result[0][0] is None:
        return 'У вас ещё нет расходов'
    return f'Сумма расходов в этом месяце: {round(result[0][0], 2)}р.'


def sum_of_month_category() -> str:
    """Возвращает сумму расходов за последний месяц по всем категориям"""
    tz = pytz.timezone("Europe/Moscow")
    dt = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    month_now = dt.split('-')[1]
    year_now = dt.split('-')[0]
    date_now = dt.split(' ')[0]
    statistic = 'Расходы по категориям в текущем месяце:\n'
    for c in get_category_list():
        cur.execute(
        f"""SELECT SUM (money) 
        FROM financial 
        WHERE date::date >= date '{year_now}-{month_now}-01' AND date::date <= date '{date_now}' AND category = '{c}'""" 
    )
        result = cur.fetchall()
        if result[0][0] is None:
            statistic += f'{c}: 0р.\n'
        else:
            statistic += f'{c}: {round(result[0][0], 2)}р.\n'
    return statistic


def sum_of_today() -> str:
    """Возвращает сумму трат за текущий день"""
    tz = pytz.timezone("Europe/Moscow")
    dt = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    date_now = dt.split(' ')[0]
    cur.execute(f"SELECT SUM (money) FROM financial WHERE date::date = date '{date_now}'")
    result = cur.fetchall()
    if result[0][0] is None:
        return 'У вас ещё нет расходов'
    return f'Сумма расходов за сегодняшний день: {round(result[0][0], 2)}р.'


def parse_msg(text_msg: str) -> tuple:
    """Получает на вход текст сообщения, парсит его и возвращает кортеж из данных"""
    tz = pytz.timezone("Europe/Moscow")
    dt_now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    data_msg = text_msg.split(' ')
    expanse = [float(data_msg[0]), data_msg[1], dt_now]
    return tuple(expanse)


def valid_category(data_tuple) -> bool:
    """Проверяет наличие категории в списке доступных"""
    for _ in get_category_list():
        if data_tuple in get_category_list():
            return True
        else:
            return False



