import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
import sqlite3
from blockchain import add_data, deactivate_account, get_all_platforms, get_login_and_password, update_account_data
from bot_config import bot
from database import delete_user, find_company_by_user_tg, get_all_users, user_role
from bot_func import process_company_name_step,wallet_address,wallet_balance,send_crypto, add_member
import time
from threading import Thread


@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    create_account_button = KeyboardButton("Create Account")
    join_account_button = KeyboardButton("Join to the Account")
    info_button = KeyboardButton("Info")
    markup.add(create_account_button, join_account_button, info_button)
    bot.reply_to(message, "Choose an option:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Create Account")
def handle_create_account(message):
    msg = bot.send_message(message.chat.id, "Please enter the name of your company:")
    bot.register_next_step_handler(msg, lambda m: process_company_name_step(m, handle_main))
    schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)

@bot.message_handler(func=lambda message: message.text == "Join to the Account")
def handle_create_account(message):

    company = find_company_by_user_tg(message.from_user.username)
    if company:
        bot.send_message(message.chat.id, f"You are joined to {company} account")
        handle_main(message)
    else :
        bot.send_message(message.chat.id, "You don't belong to more than one company")

    
def handle_main(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    password_manager_button = KeyboardButton("Password Manager")
    cryptocurrency_manager_button = KeyboardButton("Cryptocurrency Manager")
    man_member_button = KeyboardButton("Member Manager")
    # delete_account_button = KeyboardButton("Delete Account")
    markup.add(password_manager_button, cryptocurrency_manager_button, man_member_button)
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)
    schedule_deletion(message.chat.id, [message.message_id], 300)

@bot.message_handler(func=lambda message: message.text == "Password Manager")
def handle_password_manager(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    create = KeyboardButton('Create Platform')
    edit = KeyboardButton('Edit Account')
    delete = KeyboardButton('Delete Account')
    view_accounts = KeyboardButton('View Accounts')
    back = KeyboardButton("Back")
    markup.add(create, edit, delete, view_accounts, back)
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)
    # schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)

# ---- Pasword Manager
    
# ---- Create Platform -----    

@bot.message_handler(func=lambda message: message.text == 'Create Platform')
def handle_create(message):
    bot.send_message(message.chat.id, 'Please enter the platform for the account:')
    bot.register_next_step_handler_by_chat_id(message.chat.id, process_platform_step, message.from_user.id)
    schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)

def process_platform_step(message, user_id):
    platform = message.text
    msg = bot.send_message(message.chat.id, 'Please enter the email for the account:')
    bot.register_next_step_handler(msg, process_email_step, user_id, platform)
    schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)

def process_email_step(message, user_id, platform):
    email = message.text
    msg = bot.send_message(message.chat.id, 'Now, please enter the password for the account:')
    bot.register_next_step_handler(msg, process_password_step, user_id, platform, email)
    schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)

def process_password_step(message, user_id, platform, email):
    password = message.text
    company = find_company_by_user_tg(message.from_user.username)
    
    if company:
        add_data(company,platform,email,password)
        
        bot.send_message(message.chat.id, f'Account has been successfully created for company: {company} on platform: {platform}')
    else:
        bot.send_message(message.chat.id, 'Your company was not found in the database.')
    
    schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)

# ---- ----
    
# ---- View Platform ----
    
@bot.message_handler(func=lambda message: message.text == 'View Accounts')
def view_accounts_callback(message):
    company = find_company_by_user_tg(message.from_user.username) 
    print(company)
    username = message.from_user.username
    print(username)
    platforms = get_all_platforms(company)
    print(platforms)
   

    try:
        markup = InlineKeyboardMarkup()
        for platform in platforms:
            button = InlineKeyboardButton(platform, callback_data='platform_' + platform)
            markup.add(button)
        bot.send_message(message.chat.id, "Select a platform:", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error retrieving platforms: {str(e)}")
    schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)



@bot.callback_query_handler(func=lambda call: call.data.startswith('platform_'))
def handle_platform_selection(call):
    platform = call.data[len('platform_'):]
    company = find_company_by_user_tg(call.from_user.username)

    try:
        login, password = get_login_and_password(company,platform)
        bot.send_message(call.message.chat.id, f'Login: <code>{login}</code> \nPassword: <code>{password}</code>', parse_mode='HTML')
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error retrieving account data: {str(e)}")
    
    schedule_deletion(call.message.chat.id, [call.message.message_id, call.message.message_id + 1], 300)

# ---- ----
    
# ---- Edit Platform ----
@bot.message_handler(func=lambda message: message.text == 'Edit Account')
def handle_edit(message):
    company = find_company_by_user_tg(message.from_user.username) 
    print(company)
    username = message.from_user.username
    print(username)
    platforms = get_all_platforms(company)
    print(platforms)
   

    try:
        markup = InlineKeyboardMarkup()
        for platform in platforms:
            button = InlineKeyboardButton(platform, callback_data='edit_platform' + platform)
            markup.add(button)
        bot.send_message(message.chat.id, "Select a platform to edit:", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error retrieving platforms: {str(e)}")
    schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_platform'))
def handle_platform_selection_edit(call):
    platform = call.data[len('edit_platform'):]
    msg = bot.send_message(call.message.chat.id, "Please enter the new email for the account:")
    bot.register_next_step_handler(msg, process_email_edit_step, platform)
    schedule_deletion(call.message.chat.id, [call.message.message_id, call.message.message_id + 1], 300)


def process_email_edit_step(message, platform_name):
    new_email = message.text
    bot.send_message(message.chat.id, "Please enter the new password for the account:")
    bot.register_next_step_handler(message, process_password_edit_step, platform_name, new_email)
    schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)

def process_password_edit_step(message, platform_name, new_email):
    new_password = message.text
    company = find_company_by_user_tg(message.from_user.username)


    update_account_data(company, platform_name, new_email, new_password)
    bot.send_message(message.chat.id, "Account details updated successfully.")
    schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)

# ---- ----
    
# ---- Delete Platform ---

@bot.message_handler(func=lambda message: message.text == 'Delete Account')
def handle_delete(message):
    company = find_company_by_user_tg(message.from_user.username) 
    print(company)
    username = message.from_user.username
    print(username)
    platforms = get_all_platforms(company)
    print(platforms)
   

    try:
        markup = InlineKeyboardMarkup()
        for platform in platforms:
            button = InlineKeyboardButton(platform, callback_data='del_platform' + platform)
            markup.add(button)
        bot.send_message(message.chat.id, "Select a platform:", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error retrieving platforms: {str(e)}")
    schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)



@bot.callback_query_handler(func=lambda call: call.data.startswith('del_platform'))
def handle_platform_selection_del(call):
    platform = call.data[len('del_platform'):]
    company = find_company_by_user_tg(call.from_user.username)

    try:
        deactivate_account(company,platform)
        bot.send_message(call.message.chat.id, f"Account for platform {platform} deleted successfully.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error retrieving account data: {str(e)}")
    
    schedule_deletion(call.message.chat.id, [call.message.message_id, call.message.message_id + 1], 300)

# ---- -----

# ---- Call Back
    
@bot.message_handler(func=lambda message: message.text == 'Ваcк')
def back_main(message):
    handle_main(message)

# ---- ----
    
# ---- Crypto Manager ----

@bot.message_handler(func=lambda message: message.text == "Cryptocurrency Manager")
def handle_create_crypto(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    address = KeyboardButton("Wallet Address")
    balance = KeyboardButton("Wallet Balance")
    send = KeyboardButton("Send Cryptocurrency")
    back = KeyboardButton("Back")
    markup.add(address, balance, send, back)
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)


# ---- ----
    
# ---- Go Back ----
    
@bot.message_handler(func=lambda message: message.text == "Back")
def handle_back(message):
    handle_main(message)

# ---- ----

# ---- Crypto Wallet Address ----

@bot.message_handler(func=lambda message: message.text == "Wallet Address")
def handle_wallet_address(message):
    wallet_address(message)

# ---- ----

# ---- Crypto Wallet Balance ----

@bot.message_handler(func=lambda message: message.text == "Wallet Balance")
def handle_wallet_balance(message):
    wallet_balance(message)

# ---- ----
    

# ---- Send Crypto -----

@bot.message_handler(func=lambda message: message.text == "Send Cryptocurrency")
def handle_send_crypto(message):
    markup = InlineKeyboardMarkup(row_width=1)  
    eth = InlineKeyboardButton('Etherium', callback_data='eth')
    bnb = InlineKeyboardButton('BNB Chain', callback_data='bnb')
    poly = InlineKeyboardButton('Polygon', callback_data='matic')
    markup.add(eth, bnb, poly)

    wallet_balance(message, markup)

    # bot.send_message(message.chat.id, "Your corporate wallet balance:\n 1. Etherium: 0.02 ETH \n 2. BNB Chain: 0.04875875 BNB \n 3. Polygon: 0.2 MATIC", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'eth')
def handle_eth(call):
    msg = bot.send_message(call.message.chat.id, 'Please enter the destination address:')
    bot.register_next_step_handler(msg, process_destination_address, 'eth')  

@bot.callback_query_handler(func=lambda call: call.data == 'bnb')
def handle_bnb(call):
    msg = bot.send_message(call.message.chat.id, 'Please enter the destination address:')
    bot.register_next_step_handler(msg, process_destination_address, 'bnb') 

@bot.callback_query_handler(func=lambda call: call.data == 'matic')
def handle_poly(call):
    msg = bot.send_message(call.message.chat.id, 'Please enter the destination address:')
    bot.register_next_step_handler(msg, process_destination_address, 'matic')  

def process_destination_address(message, crypto_type):
    address = message.text  # Получаем адрес от пользователя
    msg = bot.send_message(message.chat.id, 'Please enter the amount to send:')
    bot.register_next_step_handler(msg, send_crypto, address, crypto_type)  # Передаем полученный адрес и тип криптовалюты

# ----- ----

def delete_message_later(chat_id, message_id, delay_seconds):
    time.sleep(delay_seconds)
    bot.delete_message(chat_id, message_id)

def schedule_deletion(chat_id, message_ids, delay_seconds):
    for message_id in message_ids:
        thread = Thread(target=delete_message_later, args=(chat_id, message_id, delay_seconds))
        thread.start()

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(message, "Available commands:\n"
                          "/start - Start the bot\n"
                          "/help - Display help message")
    schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)



@bot.message_handler(func=lambda message: message.text == "Info")
def handle_info(message):
    info_message = "Hello dear friend,\n\n" \
                   "I am a Corporate Password and Cryptocurrency Management Bot, a tool designed to secure and efficiently manage your company's key assets. I offer automated solutions for storing, managing, and regulating access to corporate passwords and cryptocurrency wallets."
    bot.reply_to(message, info_message)
    schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)



# ---- Member Manager ----
    
@bot.message_handler(func=lambda message: message.text == "Member Manager")
def handle_man_member(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    print(user_role(message.from_user.username))
    if (user_role(message.from_user.username) == 'admin'):
        add = KeyboardButton("Add Member")
        view = KeyboardButton("View Member")
        delt = KeyboardButton("Delete Member")
        back = KeyboardButton("Back")
        markup.add(add, view, delt, back)
    else:
        view = KeyboardButton("View Member")
        back = KeyboardButton("Back")
        markup.add(view, back)


    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)
    schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)

# ---- Go Back ----
@bot.message_handler(func=lambda message: message.text == "Back")
def handle_back(message):
    handle_main(message)

# ---- ----
    
# ---- Add Member ----

@bot.message_handler(func=lambda message: message.text == "Add Member")
def handle_add_member(message):
    if (user_role(message.from_user.username) == 'user'):
        handle_main(message)
    msg = bot.send_message(message.chat.id, "To add a user, send the user's nickname\n"
                           "Example: @mr_kenzhali")
    bot.register_next_step_handler(msg, add_member)
    schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)

@bot.message_handler(func=lambda message: message.text == "Delete Member")
def handle_del_member(message):
    if (user_role(message.from_user.username) == 'user'):
        handle_main(message)
    company = find_company_by_user_tg(message.from_user.username)
    users = get_all_users(company)

    if users:
        markup = InlineKeyboardMarkup()
        for user in users:
            button = InlineKeyboardButton(user, callback_data='delete_' + user)
            markup.add(button)
        bot.send_message(message.chat.id, "Select a user to delete:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "No users found for your company.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_'))
def del_list(call):
    user_to_delete = call.data[len('delete_'):]
    delete_user(user_to_delete)
    bot.send_message(call.message.chat.id, f"User {user_to_delete} deleted successfully.")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

# def handle_del_member(message):
#     bot.send_message(message.chat.id, 'Which one do you want delete:')
#     bot.register_next_step_handler_by_chat_id(message.chat.id, del_list, message.from_user.id)

# def del_list(message, user_id):
#     user = message.text
#     delete_user(user)
#     schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)
    
@bot.message_handler(func=lambda message: message.text == "View Member")
def handle_view_member(message):
    company = find_company_by_user_tg(message.from_user.username) 
    user = get_all_users(company)

    try:
       markup = InlineKeyboardMarkup()
       for platform in user:
           button = InlineKeyboardButton(platform, callback_data='view' + platform)
           markup.add(button)
       bot.send_message(message.chat.id, "Select a platform:", reply_markup=markup)
    except Exception as e:
       bot.send_message(message.chat.id, f"Error retrieving platforms: {str(e)}")
    # schedule_deletion(call.message.chat.id, [call.message.message_id, call.message.message_id + 1], 300)
    
    # bot.send_message(message.chat.id, "View123")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "I'm sorry, I don't understand that command. Use /help for available commands.")
    schedule_deletion(message.chat.id, [message.message_id, message.message_id + 1], 300)

def run_bot():
    bot.polling()
