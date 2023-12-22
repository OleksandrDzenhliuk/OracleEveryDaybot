from config import TOKEN
import telebot as tl
from telebot import types
import random
from data import *
import datetime
from Database.database import create_connection, create_users_table, insert_or_update_user, update_session, check_user_existence, get_user_data, count_users, update_zodiac, create_horoscope_table, update_horoscope_sign
import ast


# @OracleEveryDaybot

database_file = 'sessions.db'
conn = create_connection(database_file)


if conn is not None:
    create_users_table(conn)

use_state = {}
use_state_admin = {}

bot = tl.TeleBot(TOKEN)

def generate_random_numbers():
    random_numbers = random.sample(range(0, 49), 6)
    return random_numbers

def check_user_session(user_id, username):
    if check_user_existence(conn, user_id):
        data_user = get_user_data(conn, user_id)
                
        if data_user and data_user[7]:  
            last_update_datetime = datetime.datetime.strptime(data_user[7], "%Y-%m-%d %H:%M:%S.%f")
            zodiac = None
            if data_user[6]:
                zodiac = data_user[6]
            if last_update_datetime.date() < datetime.datetime.now().date():
                print(f"Користувач з ID_telegram {user_id} не оновлювався протягом останнього дня.")
                update_session(
                    conn=conn, 
                    ID_telegram=user_id, 
                    card_taro_id=random.randint(1, 22), 
                    luck_numbers=str(generate_random_numbers()), 
                    zodiac_sign=zodiac, 
                    last_update=datetime.datetime.now())

        print(f"У базі даних: {count_users(conn)} унікальних користувачів")
    else:
        insert_or_update_user(
            conn=conn, 
            ID_telegram=user_id, 
            username=username, 
            first_session_date=datetime.datetime.now(), 
            last_update=datetime.datetime.now())
        update_session(
            conn=conn, 
            ID_telegram=user_id, 
            card_taro_id=random.randint(1, 22), 
            luck_numbers=str(generate_random_numbers()), 
            zodiac_sign=None, 
            last_update=datetime.datetime.now())
        print(f"У базі даних новий користувач")    

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username

    check_user_session(user_id, username)
    
    data_user = get_user_data(conn, user_id)
    try:
        zodiac_sign = data_user[6]
    except:
        zodiac_sign = None
    
    if zodiac_sign == None:
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
        bot.send_photo(message.chat.id, photo, 
            caption="☀️🌙 Для отримання гороскопу оберіть ваш знак зодіаку",
                parse_mode='html',
                    reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('☀️ Передбачення на день')
        item2 = types.KeyboardButton('🃏 Пройти гадання на картах Таро')
        item3 = types.KeyboardButton('💝 Сумісність за Знаком Зодіаку')
        item4 = types.KeyboardButton('🌅 Східний гороскоп за роком народження')
        item5 = types.KeyboardButton('🔢 Гадання за методом Випадкових Чисел')

        markup.row(item1, item2)
        markup.row(item3, item4)
        markup.row(item5)

        photo = open('static/image/other/start.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, 
            caption="Що вміє цей бот?\n\nЗа допомогою нашого бота, ви кожного дня будете отримувати гороскоп для обраного вами знаку зодіаку❤️\n\nА також, в самому боті ви можете дізнатися:\n\n<strong>☀️ Передбачення на день\n🌅 Східний гороскоп за роком народження\n💝 Сумісність за Знаком Зодіаку\n🃏 Пройти гадання на картах Таро\n🔢 Гадання за методом Випадкових Чисел</strong>",
                parse_mode='html',
                    reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.chat.type == 'private':
        if message.text == '☀️ Передбачення на день':
            user_id = message.from_user.id
            username = message.from_user.username
            check_user_session(user_id, username)
            
            data_user = get_user_data(conn, user_id)
            try:
                zodiac_sign = data_user[6]
            except:
                zodiac_sign = None
            
            if zodiac_sign == None:
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
                bot.send_photo(message.chat.id, photo, 
                    caption="Будь ласка оновіть дані вашого гороскопу\n\nОберіть свій зодіак:",
                        parse_mode='html',
                            reply_markup=markup)
            else:
                data_user = get_user_data(conn, user_id)
                print(data_user)
                user_number = ast.literal_eval(data_user[5])[0]
                user_data = lucky_number[user_number]

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item = types.KeyboardButton('✅ У меню')
                markup.add(item)
                    
                photo = open('static/image/other/foresight.jpg', 'rb')
                bot.send_photo(message.chat.id, photo, 
                    caption=f"Передбачення на сьогодні:\n\n{user_data}",
                        parse_mode='html',
                            reply_markup=markup)
                
        if message.text == '🌅 Східний гороскоп за роком народження':
            user_id = message.from_user.id
            username = message.from_user.username
            check_user_session(user_id, username)   
            
            markup = types.InlineKeyboardMarkup(row_width=3)

            item1  = types.InlineKeyboardButton('Миша',     callback_data="eastern_horoscope_1")
            item2  = types.InlineKeyboardButton('Бик',      callback_data="eastern_horoscope_2")
            item3  = types.InlineKeyboardButton('Тигр',     callback_data="eastern_horoscope_3")
            item4  = types.InlineKeyboardButton('Кролик',   callback_data="eastern_horoscope_4")
            item5  = types.InlineKeyboardButton('Дракон',   callback_data="eastern_horoscope_5")
            item6  = types.InlineKeyboardButton('Змія',     callback_data="eastern_horoscope_6")
            item7  = types.InlineKeyboardButton('Кінь',     callback_data="eastern_horoscope_7")
            item8  = types.InlineKeyboardButton('Коза',     callback_data="eastern_horoscope_8")
            item9  = types.InlineKeyboardButton('Мавпа',    callback_data="eastern_horoscope_9")
            item10 = types.InlineKeyboardButton('Півень',   callback_data="eastern_horoscope_10")
            item11 = types.InlineKeyboardButton('Собака',   callback_data="eastern_horoscope_11")
            item12 = types.InlineKeyboardButton('Кабан',    callback_data="eastern_horoscope_12")

            markup.row(item1, item2,    item3,  item4)
            markup.row(item5, item6,    item7,  item8)
            markup.row(item9, item10,   item11, item12)

            photo = open('static/image/other/dragon.jpg', 'rb')
            
            bot.send_photo(message.chat.id, photo, 
                caption="🌅 Східний гороскоп за роком народження\n\n<strong>Оберіть істоту за вашим роком народження та отримайте точне передбачення на  2024 рік:</strong>",
                    parse_mode='html',
                        reply_markup=markup)

        if message.text == '💝 Сумісність за Знаком Зодіаку':
            user_id = message.from_user.id
            username = message.from_user.username
            check_user_session(user_id, username)


            markup = types.InlineKeyboardMarkup(row_width=3)
            
            item1   = types.InlineKeyboardButton('Овен ♈️',      callback_data="compatibility_first_1")
            item2   = types.InlineKeyboardButton('Телець ♉️',    callback_data="compatibility_first_2")
            item3   = types.InlineKeyboardButton('Близнюки ♊️',  callback_data="compatibility_first_3")
            item4   = types.InlineKeyboardButton('Рак ♋️',       callback_data="compatibility_first_4")
            item5   = types.InlineKeyboardButton('Лев ♌️',       callback_data="compatibility_first_5")
            item6   = types.InlineKeyboardButton('Діва ♍️',      callback_data="compatibility_first_6")
            item7   = types.InlineKeyboardButton('Терези ♎️',    callback_data="compatibility_first_7")
            item8   = types.InlineKeyboardButton('Скорпіон ♏️',  callback_data="compatibility_first_8")
            item9   = types.InlineKeyboardButton('Стрілець ♐️',  callback_data="compatibility_first_9")
            item10  = types.InlineKeyboardButton('Козеріг ♑️',   callback_data="compatibility_first_10")
            item11  = types.InlineKeyboardButton('Водолій ♒️',   callback_data="compatibility_first_11")
            item12  = types.InlineKeyboardButton('Риби ♓️',      callback_data="compatibility_first_12")

            markup.row(item1, item2,    item3,  item4)
            markup.row(item5, item6,    item7,  item8)
            markup.row(item9, item10,   item11, item12)

            photo = open(f'static/image/other/compatibility.jpg', 'rb')
        
            bot.send_photo(message.chat.id, photo, 
                caption="💕 Сумісність між двома знаками зодіаку\n\n🎲 Оберіть перший знак зодіаку:",
                    parse_mode='html',
                        reply_markup=markup)
        
        if message.text == '🃏 Пройти гадання на картах Таро':
            user_id = message.from_user.id
            username = message.from_user.username
            
            check_user_session(user_id, username)
            data_user = get_user_data(conn, user_id)
            try:
                zodiac_sign = data_user[6]
            except:
                zodiac_sign = None
            
            if zodiac_sign == None:
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
                bot.send_photo(message.chat.id, photo, 
                    caption="Будь ласка оновіть дані вашого гороскопу\n\nОберіть свій зодіак:",
                        parse_mode='html',
                            reply_markup=markup)
                
            else:
                rd = random.randint(1, 4)
                markup = types.InlineKeyboardMarkup(row_width=3)
                
                item1  = types.InlineKeyboardButton('1️⃣',   callback_data="card_taro_1")
                item2  = types.InlineKeyboardButton('2️⃣',   callback_data="card_taro_2")
                item3  = types.InlineKeyboardButton('3️⃣',   callback_data="card_taro_3")
                item4  = types.InlineKeyboardButton('4️⃣',   callback_data="card_taro_4")
                item5  = types.InlineKeyboardButton('5️⃣',   callback_data="card_taro_5")
                item6  = types.InlineKeyboardButton('6️⃣',   callback_data="card_taro_6")
                item7  = types.InlineKeyboardButton('7️⃣',   callback_data="card_taro_7")
                item8  = types.InlineKeyboardButton('8️⃣',   callback_data="card_taro_8")

                markup.row(item1, item2,    item3,  item4)
                markup.row(item5, item6,    item7,  item8)

                photo = open(f'static/image/TARO/pre_taro_{rd}.jpg', 'rb')
            
                bot.send_photo(message.chat.id, photo, 
                    caption="Гадання на картах Таро можна проходити тільки 1 раз на день‼️\n\n🃏 Оберіть карту, яка вам найбільше подобається:",
                        parse_mode='html',
                            reply_markup=markup)
            
            
        
        if message.text == '🔢 Гадання за методом Випадкових Чисел':
            user_id = message.from_user.id
            username = message.from_user.username
            
            check_user_session(user_id, username)

            data_user = get_user_data(conn, user_id)
            user_luck_number = ast.literal_eval(data_user[5])

            markup = types.InlineKeyboardMarkup(row_width=3)
            
            item1  = types.InlineKeyboardButton(user_luck_number[0],   callback_data="luck_number_1")
            item2  = types.InlineKeyboardButton(user_luck_number[1],   callback_data="luck_number_2")
            item3  = types.InlineKeyboardButton(user_luck_number[2],   callback_data="luck_number_3")
            item4  = types.InlineKeyboardButton(user_luck_number[3],   callback_data="luck_number_4")
            item5  = types.InlineKeyboardButton(user_luck_number[4],   callback_data="luck_number_5")
            item6  = types.InlineKeyboardButton(user_luck_number[5],   callback_data="luck_number_6")

            markup.row(item1, item2, item3, item4, item5, item6)

            photo = open(f'static/image/other/luck_number.jpg', 'rb')
        
            bot.send_photo(message.chat.id, photo, 
                caption=f"💫Оберіть ваше щасливе число!\nВаші числа на сьогодні:   <strong>{user_luck_number[0]}   {user_luck_number[1]}   {user_luck_number[2]}   {user_luck_number[3]}   {user_luck_number[4]}   {user_luck_number[5]}</strong>\n\nОберіть число зі списку та отримайте передбачення для вас:",
                    parse_mode='html',
                        reply_markup=markup)
        
        if message.text == '✅ У меню':
            user_id = message.from_user.id
            username = message.from_user.username
            check_user_session(user_id, username)
            
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('☀️ Передбачення на день')
            item2 = types.KeyboardButton('🃏 Пройти гадання на картах Таро')
            item3 = types.KeyboardButton('💝 Сумісність за Знаком Зодіаку')
            item4 = types.KeyboardButton('🌅 Східний гороскоп за роком народження')
            item5 = types.KeyboardButton('🔢 Гадання за методом Випадкових Чисел')

            markup.row(item1, item2)
            markup.row(item3, item4)
            markup.row(item5)

            bot.send_message(message.chat.id, 
                text="Що вміє цей бот?\n\nЗа допомогою нашого бота, ви кожного дня будете отримувати гороскоп для обраного вами знаку зодіаку❤️\n\nА також, в самому боті ви можете дізнатися:\n\n<strong>☀️ Передбачення на день\n🌅 Східний гороскоп за роком народження\n💝 Сумісність за Знаком Зодіаку\n🃏 Пройти гадання на картах Таро\n🔢 Гадання за методом Випадкових Чисел</strong>",
                    parse_mode='html',
                        reply_markup=markup)


        if message.text == '/admin':
            user_id = message.from_user.id
            username = message.from_user.username
            check_user_session(user_id, username)
            
            if use_state.get(user_id):
                if use_state[user_id] == "login_success":
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton('Записати / оновити дані гороскопу')
                    item2 = types.KeyboardButton('✅ У меню')

                    markup.row(item1)
                    markup.row(item2)
                    
                    bot.send_message(message.chat.id, text="Вітаємо в адмін функціоналі!", parse_mode='html', reply_markup=markup)

            else:
                use_state[user_id] = "waiting_to_input_password"
                bot.send_message(message.chat.id, text="Введіть password:", parse_mode='html')

        if use_state.get(message.from_user.id):
            user_id = message.from_user.id
            username = message.from_user.username
            check_user_session(user_id, username)

            if use_state[user_id] == "waiting_to_input_password":
                password_user = message.text
                if password_user == 'qwer1234':
                    use_state[user_id] = "login_success"
                    
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton('Записати / оновити дані гороскопу')
                    item2 = types.KeyboardButton('✅ У меню')
                    markup.row(item1)
                    markup.row(item2)
                    
                    bot.send_message(message.chat.id, text="Вітаємо в адмін функціоналі!", parse_mode='html', reply_markup=markup)

            if use_state[user_id] == "login_success":
                if use_state_admin.get(user_id): 
                    if use_state_admin[user_id]['status'] == "waiting_to_input_date":
                        
                        date = message.text
                        
                        is_table = create_horoscope_table(conn, date)
                        if is_table:
                            use_state_admin[user_id] = { 'status': 'waiting_to_input_zodiac', 'date':  date}
                            
                            markup = types.InlineKeyboardMarkup(row_width=3)
                    
                            item1   = types.InlineKeyboardButton('Овен ♈️',      callback_data="adminInput_zodiac_1")
                            item2   = types.InlineKeyboardButton('Телець ♉️',    callback_data="adminInput_zodiac_2")
                            item3   = types.InlineKeyboardButton('Близнюки ♊️',  callback_data="adminInput_zodiac_3")
                            item4   = types.InlineKeyboardButton('Рак ♋️',       callback_data="adminInput_zodiac_4")
                            item5   = types.InlineKeyboardButton('Лев ♌️',       callback_data="adminInput_zodiac_5")
                            item6   = types.InlineKeyboardButton('Діва ♍️',      callback_data="adminInput_zodiac_6")
                            item7   = types.InlineKeyboardButton('Терези ♎️',    callback_data="adminInput_zodiac_7")
                            item8   = types.InlineKeyboardButton('Скорпіон ♏️',  callback_data="adminInput_zodiac_8")
                            item9   = types.InlineKeyboardButton('Стрілець ♐️',  callback_data="adminInput_zodiac_9")
                            item10  = types.InlineKeyboardButton('Козеріг ♑️',   callback_data="adminInput_zodiac_10")
                            item11  = types.InlineKeyboardButton('Водолій ♒️',   callback_data="adminInput_zodiac_11")
                            item12  = types.InlineKeyboardButton('Риби ♓️',      callback_data="adminInput_zodiac_12")

                            markup.row(item1, item2,    item3,  item4)
                            markup.row(item5, item6,    item7,  item8)
                            markup.row(item9, item10,   item11, item12)
                    
                            bot.send_message(user_id, 
                                            text=f"Ви ввели дату - <strong>{use_state_admin[user_id]['date']}</strong>.\n\nТепер оберіть зодіак, який хочете додати/редагувати:", 
                                            parse_mode='html', reply_markup=markup)
                        else:
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            item1 = types.KeyboardButton('Записати / оновити дані гороскопу')
                            item2 = types.KeyboardButton('✅ У меню')
                            markup.row(item1)
                            markup.row(item2)
                            
                            bot.send_message(user_id, 
                                            text=f"Введена дата - {use_state_admin[user_id]['date']} не правильна.", 
                                            parse_mode='html', reply_markup=markup)
                        
                    if use_state_admin[user_id]['status'] == "waiting_to_input_zodiac_text":
                        text = message.text
                        
                        is_new_record = update_horoscope_sign(
                            conn=conn, 
                            date_to_record=use_state_admin[user_id]['date'],
                            zodiac_sign=use_state_admin[user_id]['zodiac'],
                            prediction=text
                        )
                        use_state_admin[user_id]['status'] = None
                        
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton('Записати / оновити дані гороскопу')
                        item2 = types.KeyboardButton('✅ У меню')
                        markup.row(item1)
                        markup.row(item2)
                            
                        if is_new_record:
                            bot.send_message(user_id, 
                                                text=f"✅ Дані оновлено.", 
                                                parse_mode='html', reply_markup=markup)
                        else:
                            bot.send_message(user_id, 
                                                text=f"❌ Дані не оновлено, помила запису.", 
                                                parse_mode='html', reply_markup=markup)
                        
                        
                        
            if message.text == "Записати / оновити дані гороскопу":
                user_id = message.from_user.id
                username = message.from_user.username
                check_user_session(user_id, username)

                if use_state.get(user_id) == "login_success":
                    use_state_admin[user_id] = {'status': 'waiting_to_input_date'}
                    bot.send_message(user_id, text="Напишіть дату дня, який хочете створити / редагувати:\n\nписати потрібно у форматі - 10.12.2023")
        

      



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data.find('eastern_horoscope') != -1:
                
                index = int(call.data.split('_')[2])
                    
                
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item = types.KeyboardButton('✅ У меню')
                markup.add(item)
                
                photo = open(f'static/image/eastern_horoscope/{index}.jpg', 'rb')
                bot.send_photo(call.message.chat.id, photo, 
                    caption=f"{eastern_horoscope[index - 1]}",
                        parse_mode='html',
                            reply_markup=markup)

            if call.data.find('card_taro') != -1:
                user_id = call.from_user.id
                username = call.from_user.username

                check_user_session(user_id, username)
                data_user = get_user_data(conn, user_id)
                card_id = data_user[4]

                caption = f"Ваша карта на сьогодні - №<strong>{card_id}</strong>\n\n{cards_taro_text[card_id - 1]}"

                text_length = len(caption)
                max_caption_length = 1000

                if text_length > max_caption_length:
                    chunks = [caption[i:i + max_caption_length] for i in range(0, text_length, max_caption_length)]
                else:
                    chunks = [caption]

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item = types.KeyboardButton('✅ У меню')
                markup.add(item)

                for i, chunk in enumerate(chunks):
                    parse_mode = 'html' if i == 0 else None

                    if i == 0:
                        photo = open(f'static/image/TARO/{card_id}.jpg', 'rb')
                        bot.send_photo(call.message.chat.id, photo, caption=chunk, parse_mode=parse_mode, reply_markup=markup)
                    else:
                        bot.send_message(call.message.chat.id, text=chunk, parse_mode=parse_mode, reply_markup=markup)




            if call.data.find('luck_number') != -1:
                index = int(call.data.split('_')[2])
                
                user_id = call.from_user.id
                username = call.from_user.username
                
                check_user_session(user_id, username)

                data_user = get_user_data(conn, user_id)
                user_luck_number = ast.literal_eval(data_user[5])
                
                number = user_luck_number[index - 1]
                
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item = types.KeyboardButton('✅ У меню')
                markup.add(item)
                
                bot.send_message(
                    call.message.chat.id,
                        text=f"🔮 Ваше передбачення...\n\n{lucky_number[number]}",
                            parse_mode='html',
                                reply_markup=markup)
                
                 
            if call.data.find('zodiac_sing') != -1:
                user_id = call.from_user.id
                
                who = call.data.split('_')[2]
                print(who)
                update_zodiac(conn, user_id, who)

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item = types.KeyboardButton('✅ У меню')
                markup.add(item)
                
                bot.send_message(
                    call.message.chat.id,
                        text=f"Тепер ваш знак - <strong>{who}</strong>\n\nНажміть ✅ У меню для ознайомлення з можливостями бота",
                            parse_mode='html',
                                reply_markup=markup)
                
                
            if call.data.find('compatibility_first') != -1:
                global index_first
                index_first = int(call.data.split('_')[2])

                user_id = call.from_user.id
                username = call.from_user.username
                check_user_session(user_id, username)


                markup = types.InlineKeyboardMarkup(row_width=3)
                
                item1   = types.InlineKeyboardButton('Овен ♈️',      callback_data="compatibility_second_1")
                item2   = types.InlineKeyboardButton('Телець ♉️',    callback_data="compatibility_second_2")
                item3   = types.InlineKeyboardButton('Близнюки ♊️',  callback_data="compatibility_second_3")
                item4   = types.InlineKeyboardButton('Рак ♋️',       callback_data="compatibility_second_4")
                item5   = types.InlineKeyboardButton('Лев ♌️',       callback_data="compatibility_second_5")
                item6   = types.InlineKeyboardButton('Діва ♍️',      callback_data="compatibility_second_6")
                item7   = types.InlineKeyboardButton('Терези ♎️',    callback_data="compatibility_second_7")
                item8   = types.InlineKeyboardButton('Скорпіон ♏️',  callback_data="compatibility_second_8")
                item9   = types.InlineKeyboardButton('Стрілець ♐️',  callback_data="compatibility_second_9")
                item10  = types.InlineKeyboardButton('Козеріг ♑️',   callback_data="compatibility_second_10")
                item11  = types.InlineKeyboardButton('Водолій ♒️',   callback_data="compatibility_second_11")
                item12  = types.InlineKeyboardButton('Риби ♓️',      callback_data="compatibility_second_12")

                markup.row(item1, item2,    item3,  item4)
                markup.row(item5, item6,    item7,  item8)
                markup.row(item9, item10,   item11, item12)

                photo = open(f'static/image/other/compatibility.jpg', 'rb')
            
                bot.send_photo(call.message.chat.id, photo, 
                    caption="💕 Сумісність між двома знаками зодіаку\n\n🎲 Оберіть другий знак зодіаку:",
                        parse_mode='html',
                            reply_markup=markup)

            if call.data.find('compatibility_second') != -1:
                global index_second
                index_second = int(call.data.split('_')[2])

                your_compatibility = compatibility[index_first - 1][index_second - 1]
                
                photo = open(f'static/image/other/compatibility_result.jpg', 'rb')
            
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item = types.KeyboardButton('✅ У меню')
                markup.add(item)
                
                bot.send_photo(call.message.chat.id, photo, 
                    caption=your_compatibility,
                        parse_mode='html',
                            reply_markup=markup)
                
                
            if call.data.find('adminInput_zodiac') != -1:
                user_id = call.from_user.id
                username = call.from_user.username
                check_user_session(user_id, username)
                if use_state[user_id] == "login_success":
                    if use_state_admin.get(user_id): 
                        if use_state_admin[user_id]['status'] == "waiting_to_input_zodiac":
                            index = int(call.data.split('_')[2])
                            zodiac = all_zodiac[index - 1]

                            use_state_admin[user_id] = { 
                                'status': 'waiting_to_input_zodiac_text',
                                'date': use_state_admin[user_id]['date'],
                                'zodiac': zodiac
                            }
                            
                            bot.send_message(call.message.chat.id, 
                                text=f"Введіть текст для зодіаку -  {zodiac} \nДля дати - {use_state_admin[user_id]['date']} :",
                                    parse_mode='html')
                
                    
    except Exception as e:
        print(repr(e))
        



if __name__ == "__main__":
    bot.infinity_polling()
