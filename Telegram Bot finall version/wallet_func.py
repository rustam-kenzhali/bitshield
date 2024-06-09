from web3 import Web3
from eth_account import Account

# a13f1c0ef8b06cc97831dcfb524bfe73c6326b69a05a9e21aa2e2fe2b3305b67
# 0x0af898eA02e8fC0263ebefac35a6D51922B7e95D

# Для Binance Smart Chain (BSC)
bsc_rpc_url = 'https://bsc-testnet-rpc.publicnode.com'
bsc_web3 = Web3(Web3.HTTPProvider(bsc_rpc_url))

bsc_rpc_url_2nd = 'https://bsc-testnet.public.blastapi.io'
bsc_web3_2nd = Web3(Web3.HTTPProvider(bsc_rpc_url_2nd))


# Для Ethereum
eth_rpc_url = 'https://ethereum-sepolia-rpc.publicnode.com' 
eth_web3 = Web3(Web3.HTTPProvider(eth_rpc_url))


# Для Polygon
plg_rpc_url = 'https://rpc-amoy.polygon.technology'
plg_web3 = Web3(Web3.HTTPProvider(plg_rpc_url))
plg_rpc_url_2nd = 'https://polygon-amoy-bor-rpc.publicnode.com'
plg_web3_2nd = Web3(Web3.HTTPProvider(plg_rpc_url_2nd))


def create_wallet():
    # Проверяем успешность подключения
    global bsc_web3, bsc_web3_2nd
    if bsc_web3.is_connected():
        print("Успешное подключение к BNB Chain")
    elif bsc_web3_2nd.is_connected(): 
        bsc_web3 = bsc_web3_2nd
        print("Успешное подключение к BNB Chain")
    else:
        print("Не удалось подключиться к BNB Chain")
        return

    # Генерируем новый кошелек
    account = Account.create()
    private_key = account._private_key.hex()
    address = account.address

    # Выводим адрес кошелька и приватный ключ
    print(f"Адрес кошелька: {address}")
    print(f"Приватный ключ: {private_key}")

    return address, private_key


def wallet_balance_info(wallet_address):
    global bsc_web3, bsc_web3_2nd, eth_web3, plg_web3, plg_web3_2nd

    wallet_address = '0x0af898eA02e8fC0263ebefac35a6D51922B7e95D'

    # Убедитесь, что подключение успешно
    if bsc_web3.is_connected():
        print("Успешное подключение к BNB Chain 1")
    elif bsc_web3_2nd.is_connected(): 
        bsc_web3 = bsc_web3_2nd
        print("Успешное подключение к BNB Chain 2")
    else:
        print("Не удалось подключиться к BNB Chain")
        return

    
    if eth_web3.is_connected():
        print("Успешное подключение к Сети Etherium")
    else:
        print("Не удалось подключиться к Сети Etherium")
        return

    if plg_web3.is_connected():
        print("Успешное подключение к Сети Polygon 1")
    elif plg_rpc_url_2nd.is_connected():
        print("Успешное подключение к Сети Polygon 2")
        plg_web3 = plg_rpc_url_2nd
    else:
        print("Не удалось подключиться к Сети Polygon")
        return

    # Получаем баланс кошелька 
    bnb_balance = bsc_web3.from_wei(bsc_web3.eth.get_balance(wallet_address), 'ether')
    eth_balance = eth_web3.from_wei(eth_web3.eth.get_balance(wallet_address), 'ether')
    plg_balance = plg_web3.from_wei(plg_web3.eth.get_balance(wallet_address), 'ether')

    # return bnb_balance, eth_balance, plg_balance

    return bnb_balance, eth_balance, plg_balance
    # Конвертируем баланс из Wei в BNB и выводим
    # print(f"Баланс кошелька: {bsc_web3.from_wei(bnb_balance, 'ether')} BNB")
    # print(f"Баланс ETH: {eth_web3.from_wei(eht_balance, 'ether')} ETH")
    # print(f"Баланс PLG: {plg_web3.from_wei(plg_balance, 'ether')} MATIC")


def send_crypto_to_wallet(amount, recipient_address, crypto_type):
    global bsc_web3, bsc_web3_2nd, eth_web3, plg_web3, plg_web3_2nd

    sender_address = "0x0af898eA02e8fC0263ebefac35a6D51922B7e95D"
    private_key = "a13f1c0ef8b06cc97831dcfb524bfe73c6326b69a05a9e21aa2e2fe2b3305b67"
    web3 = eth_web3

    if crypto_type == 'eth':
        amount_wei = eth_web3.to_wei(amount, 'ether')

        gas_price = eth_web3.eth.gas_price
        estimated_gas = eth_web3.eth.estimate_gas({
            'to': recipient_address,
            'value': 2_000_000_000,
        })

        nonce = eth_web3.eth.get_transaction_count(sender_address)

        transaction = {
            'chainId': eth_web3.eth.chain_id,
            'from': sender_address,
            'to': recipient_address,
            'value': amount_wei,
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': estimated_gas,
        }
        web3 = eth_web3


    elif crypto_type == 'bnb':
        if bsc_web3.is_connected():
            print("Успешное подключение к BNB Chain 1")
        elif bsc_web3_2nd.is_connected(): 
            bsc_web3 = bsc_web3_2nd
            print("Успешное подключение к BNB Chain 2")
        else:
            print("Не удалось подключиться к BNB Chain")
            return
        
        amount_wei = bsc_web3.to_wei(amount, 'ether')

        gas_price = bsc_web3.eth.gas_price
        estimated_gas = bsc_web3.eth.estimate_gas({
            'to': recipient_address,
            'value': 12_000_000_000,
        })
        print(estimated_gas)

        nonce = bsc_web3.eth.get_transaction_count(sender_address)

        transaction = {
            'chainId': bsc_web3.eth.chain_id,
            'from': sender_address,
            'to': recipient_address,
            'value': amount_wei,
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': 21000, # Стандартный лимит газа для простой транзакции
        }
        web3 = bsc_web3

    elif crypto_type == 'matic':
        if plg_web3.is_connected():
            print("Успешное подключение к Сети Polygon 1")
        elif plg_rpc_url_2nd.is_connected():
            print("Успешное подключение к Сети Polygon 2")
            plg_web3 = plg_rpc_url_2nd
        else:
            print("Не удалось подключиться к Сети Polygon")
            return
        
        amount_wei = plg_web3.to_wei(amount, 'ether')

        gas_price = plg_web3.eth.gas_price
        estimated_gas = plg_web3.eth.estimate_gas({
            'to': recipient_address,
            'value': 2_000_000_000,
        })

        nonce = plg_web3.eth.get_transaction_count(sender_address)

        transaction = {
            'chainId': plg_web3.eth.chain_id,
            'from': sender_address,
            'to': recipient_address,
            'value': amount_wei,
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': estimated_gas,
        }
        web3 = plg_web3


    
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    return transaction_hash.hex(), crypto_type

    