import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        print(f'Successfully connected to the SQLite database: {db_file}')
        return conn
    except Error as e:
        print(f"Error connecting to the database: {e}")
    return conn

        
def create_users_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_telegram TEXT UNIQUE,
                username TEXT,
                first_session_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                card_taro_id INTEGER,
                luck_numbers TEXT,
                zodiac_sign TEXT,
                last_update DATETIME
            );
        ''')
        print('Successfully created the users table.')
    except Error as e:
        print(e)

def insert_or_update_user(conn, ID_telegram, username, first_session_date, last_update):
	try:
		cursor = conn.cursor()
		cursor.execute('''
			INSERT OR REPLACE INTO users (
				ID_telegram, username, first_session_date, last_update)
			VALUES (?, ?, ?, ?);
		''', (ID_telegram, username, first_session_date, last_update))
		conn.commit()
		print('Successfully updated or inserted a user record.')
	except Error as e:
		print(e)
        
def update_session(conn, ID_telegram, card_taro_id, luck_numbers, zodiac_sign, last_update):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET card_taro_id = ?, luck_numbers = ?, zodiac_sign = ?, last_update = ?
            WHERE ID_telegram = ?;
        ''', (card_taro_id, luck_numbers, zodiac_sign, last_update, ID_telegram))
        conn.commit()
        print('Successfully updated a user session.')
    except Error as e:
        print(e)

def update_zodiac(conn, ID_telegram, zodiac_sign):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET zodiac_sign = ?
            WHERE ID_telegram = ?;
        ''', (zodiac_sign, ID_telegram))
        conn.commit()
        print('Successfully updated a user session.')
    except Error as e:
        print(e)

def check_user_existence(conn, ID_telegram):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE ID_telegram = ?", (ID_telegram,))
        result = cursor.fetchone()
        return result is not None
    except Error as e:
        print(e)
        return False
    
    
def get_user_data(conn, user_id_telegram):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE ID_telegram = ?", (user_id_telegram,))
        user_data = cursor.fetchone()
        return user_data
    except Error as e:
        print(e)
        return None
    
def count_users(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        result = cursor.fetchone()
        return result[0] if result else 0
    except Error as e:
        print(e)
        return 0
    
def get_user_id_and_zodiac_all(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ID_telegram, zodiac_sign FROM users")
        user_data = cursor.fetchall()
        return user_data
    except Error as e:
        print(e)
        return None
    
def get_user_id_and_luck_number_all(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ID_telegram, luck_numbers FROM users")
        user_data = cursor.fetchall()
        return user_data
    except Error as e:
        print(e)
        return None
    
def create_horoscope_table(conn, date_to_record):
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT COUNT(*) FROM horoscope_predictions WHERE date = ?', (date_to_record,))
        existing_records = cursor.fetchone()[0]

        if existing_records > 0:
            return True
        else:
            cursor.execute('INSERT INTO horoscope_predictions (date) VALUES (?)', (date_to_record,))
            conn.commit()
            return True

    except Exception as e:
        print(f"Error: {e}")
        return False
    
def update_horoscope_sign(conn, date_to_record, zodiac_sign, prediction):
    cursor = conn.cursor()
    try:
        cursor.execute(f'UPDATE horoscope_predictions SET {zodiac_sign} = ? WHERE date = ?', (prediction, date_to_record))
        conn.commit()
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False