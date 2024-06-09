import sqlite3

# Function to initialize the database
def init_db():
    db_path = 'bot.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create tables if they don't exist
    c.execute('''CREATE TABLE IF NOT EXISTS companies (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 company TEXT UNIQUE,
                 wallet TEXT UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 company_id TEXT,
                 user_tg TEXT,
                 user_role TEXT,
                 FOREIGN KEY(company_id) REFERENCES companies(company))''')
    c.execute('''CREATE TABLE IF NOT EXISTS transaction_history (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 company_id TEXT,
                 user_tg TEXT,
                 amount TEXT,
                 type TEXT,
                 hax TEXT,
                 FOREIGN KEY(company_id) REFERENCES companies(company))''')
    conn.commit()
    conn.close()

def company_exists(company_name):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('SELECT * FROM companies WHERE company = ?', (company_name,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def insert_company(company_name, wallet):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('INSERT INTO companies (company, wallet) VALUES (?, ?)', (company_name, wallet))
    conn.commit()
    conn.close()

def insert_user(company_name, user_tg):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (company_id, user_tg, user_role) VALUES (?, ?, ?)', (company_name, user_tg, "user"))
    conn.commit()
    conn.close()

def insert_admin(company_name, user_tg):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (company_id, user_tg, user_role) VALUES (?, ?, ?)', (company_name, user_tg, "admin"))
    conn.commit()
    conn.close()


def find_company_by_user_tg(user_tg):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('SELECT company_id FROM users WHERE user_tg = ?', (user_tg,))
    company = c.fetchone()
    conn.close()
    return company[0] if company else None

def get_all_users(company_name):
    print(company_name)
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('SELECT user_tg FROM users WHERE company_id = ?', (company_name,))
    users = c.fetchall()
    conn.close()
    clear_users = []
    for user in users:
        clear_users.append(user[0])
    
    print(clear_users)
    return clear_users

def delete_user(user_tg):

    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE user_tg = ?', (user_tg,))
    conn.commit()
    conn.close()

    print(f'User with ID {user_tg} has been deleted.')

def get_user_wallet(user_tg):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()

    # Retrieve the wallet for the given user_id
    c.execute('''
        SELECT companies.wallet
        FROM users
        JOIN companies ON users.company_id = companies.company
        WHERE users.user_tg = ?''', (user_tg,))
    wallet = c.fetchone()

    conn.close()

    # Check if the user was found and return the wallet if available
    if wallet:
        return wallet[0]  # Assuming the query returns a single value, extract it from the tuple
    else:
        return None  # Return None if the user or wallet is not found


def user_role(user_tg):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()

    # Retrieve the wallet for the given user_id
    c.execute('''
        SELECT user_role
        FROM users
        WHERE user_tg = ?''', (user_tg,))
    user_role = c.fetchone()

    conn.close()

    return user_role[0]


def transaction_history(user_tg, amount, crypto_type, hax):  
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    company = find_company_by_user_tg(user_tg)

    c.execute('INSERT INTO transaction_history (company_id, user_tg, amount, type, hax) VALUES (?, ?, ?, ?, ?)', (company, user_tg, amount, crypto_type, hax))
    conn.commit()
    conn.close()
