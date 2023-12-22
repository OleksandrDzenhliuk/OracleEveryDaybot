from app import bot
from telebot import types
from Database.database import get_user_id_and_zodiac_all, create_connection, get_user_id_and_luck_number_all, get_user_data
import threading
import time
from apscheduler.schedulers.background import BackgroundScheduler
from parser.main import parse
from datetime import datetime
from data import *
import ast
from app import check_user_session


database_file = 'sessions.db'
conn = create_connection(database_file)

scheduler = BackgroundScheduler()

def send_daily_message(user_id, zodiac_sign):
    try:
        username = get_user_data(conn, user_id)[2]
        check_user_session(user_id, username)
    

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton('✅ У меню')
        markup.add(item)
        
        if zodiac_sign != None:
            current_date = datetime.now()
            formatted_date = current_date.strftime('%d.%m.%Y')

            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT 
                    {zodiac_sign}
                FROM 
                    horoscope_predictions
                WHERE
                    date = '{formatted_date}';
            ''')

            user_data = cursor.fetchall()
            print(formatted_date)
            print(zodiac_sign)
            print(user_data)
            photo = open('static/image/other/every_day.jpg', 'rb')
            bot.send_photo(user_id, photo, 
                        caption=f"Сьогоднішній гороскоп для вас:\n\n{user_data[0][0]}",
                            parse_mode='html',
                                reply_markup=markup)
        elif zodiac_sign == None:
            check_user_session(user_id, username)
                
            markup = types.InlineKeyboardMarkup(row_width=3)

            item1  = types.InlineKeyboardButton('овен'      ,callback_data='zodiac_sing_aries')
            item2  = types.InlineKeyboardButton('телець'    ,callback_data='zodiac_sing_taurus')
            item3  = types.InlineKeyboardButton('близнюки'  ,callback_data='zodiac_sing_gemini')
            item4  = types.InlineKeyboardButton('рак'       ,callback_data='zodiac_sing_cancer')
            item5  = types.InlineKeyboardButton('лев'       ,callback_data='zodiac_sing_leo')
            item6  = types.InlineKeyboardButton('діва'      ,callback_data='zodiac_sing_virgo')
            item7  = types.InlineKeyboardButton('терези'    ,callback_data='zodiac_sing_libra')
            item8  = types.InlineKeyboardButton('скорпіон'  ,callback_data='zodiac_sing_scorpio')
            item9  = types.InlineKeyboardButton('стрілець'  ,callback_data='zodiac_sing_sagittarius')
            item10 = types.InlineKeyboardButton('козеріг'   ,callback_data='zodiac_sing_capricorn')
            item11 = types.InlineKeyboardButton('водолій'   ,callback_data='zodiac_sing_aquarius')
            item12 = types.InlineKeyboardButton('риби'      ,callback_data='zodiac_sing_pisces')

            markup.row(item1, item2, item3, item4)
            markup.row(item5, item6, item7, item8)
            markup.row(item9, item10, item11, item12)

            photo = open('static/image/other/start.jpg', 'rb')
            bot.send_photo(user_id, photo, 
                caption="Будь ласка оновіть дані вашого гороскопу\n\nОберіть свій зодіак:",
                    parse_mode='html',
                        reply_markup=markup)

    except Exception as e:
        print(f"Помилка при надсиланні повідомлення користувачу {user_id}: {e}")


def send_daily_message_2(user_id, your_luck_numbers):
    try:
        username = get_user_data(conn, user_id)[2]
        check_user_session(user_id, username)
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton('✅ У меню')
        markup.add(item)
        
        if your_luck_numbers != None:
           
            data_numbers = ast.literal_eval(your_luck_numbers)[0]
            data = lucky_number[data_numbers - 1]


            photo = open('static/image/other/every_day.jpg', 'rb')
            bot.send_photo(user_id, photo, 
                        caption=f"Ваше передбачення на сьогодні...\n\n{data}",
                            parse_mode='html',
                                reply_markup=markup)
    except Exception as e:
        print(f"Помилка при надсиланні повідомлення користувачу {user_id}: {e}")
        
def parse_data():
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS horoscope_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            aries TEXT,
            taurus TEXT,
            gemini TEXT,
            cancer TEXT,
            leo TEXT,
            virgo TEXT,
            libra TEXT,
            scorpio TEXT,
            sagittarius TEXT,
            capricorn TEXT,
            aquarius TEXT,
            pisces TEXT
        );
    ''')

    data = parse() 
    date_today = data['date_today']['today']
    values = [(date_today,) + tuple(data['horoscop_data'][key]['today'] for key in data['horoscop_data'])]

    cursor.executemany('''
        INSERT INTO horoscope_predictions (date, aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    ''', values)

    conn.commit()
    conn.close()

def update_users_in_db(user_id, zodiac_sign):
    try:
        username = get_user_data(conn, user_id)[2]
        check_user_session(user_id, username)

    except Exception as e:
        print(f"Помилка при оновлені користувача {user_id}: {e}") 
    
    
    
    
def send_daily_messages():
    for user in get_user_id_and_zodiac_all(conn):
        send_daily_message(user[0], user[1])
        
def send_daily_messages_2():
    for user in get_user_id_and_luck_number_all(conn):
        send_daily_message_2(user[0], user[1])
   
def update_users():
    for user in get_user_id_and_zodiac_all(conn):
        update_users_in_db(user[0], user[1])     
       
       
       
        
if __name__ == "__main__":
    # scheduler.add_job(parse_data, 'cron', hour=22, minute=0)
    
    scheduler.add_job(update_users, 'cron', hour=0, minute=0)
    scheduler.add_job(send_daily_messages, 'cron', hour=6, minute=0)
    scheduler.add_job(send_daily_messages_2, 'cron', hour=10, minute=0)
    
    scheduler.start()
    
    bot.infinity_polling()