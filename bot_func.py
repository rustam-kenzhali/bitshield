from database import company_exists, insert_company, get_user_wallet, insert_user, find_company_by_user_tg, insert_user, insert_admin, transaction_history
from bot_config import bot
from wallet_func import create_wallet, wallet_balance_info, send_crypto_to_wallet

def process_company_name_step(message, handle_main):
    tag = message.from_user.username
    company_name = message.text
    

    if company_exists(company_name):
        bot.send_message(message.chat.id, "This company name already exists. Please try a different name.")
        return

    # Create a new cryptocurrency wallet
    address, private_key = create_wallet()
  
    # Insert new company into database
    insert_company(company_name,address)
    insert_admin(company_name,tag)
    message_text = f"Your account has been created successfully. Your wallet address is {address} \nYour private key is <tg-spoiler>{private_key}</tg-spoiler>"
    bot.send_message(message.chat.id, message_text, parse_mode='HTML')
    handle_main(message)


# bot_func
def wallet_address(message):
    tag = message.from_user.username
    wallet = get_user_wallet(tag)
    bot.send_message(message.chat.id, "Your corporate wallet address: \n" f"{wallet}")


def wallet_balance(message, markup=None):
    tag = message.from_user.username
    wallet = get_user_wallet(tag)
    bnb_balance, eth_balance, plg_balance = wallet_balance_info(wallet)

    bot.send_message(message.chat.id, "Your corporate wallet balance: \n"
                     f"1. Etherium: {eth_balance} ETH \n"
                     f"2. BNB Chain: {bnb_balance} BNB \n"
                     f"3. Polygon: {plg_balance} MATIC", reply_markup=markup)
    


# def send_crypto(message):
#    bot.send_message(message.chat.id, f"Rustma gay 3")

def send_crypto(message, recipient_address, crypto_type):
    amount = message.text  # Получаем количество от пользователя
    transfer_address, crypto_type = send_crypto_to_wallet(amount, recipient_address, crypto_type)
    transaction_history(message.from_user.username, amount, crypto_type, transfer_address)
    bot.send_message(message.chat.id, "Cryptocurrencies successfully shipped \n"
                                    "Check your balance")

    
        
    #     bot.send_message(message.chat.id, f'Successfully sent {amount} {crypto_type.upper()} to {address}')

def add_member(message):
    user_tg = message.text
    company = find_company_by_user_tg(message.from_user.username)
    insert_user(company, user_tg.replace("@", ""))
    bot.send_message(message.chat.id, f"{user_tg} successfully added")




