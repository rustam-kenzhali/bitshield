from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

# Генерация ключа
key = get_random_bytes(16) # AES ключ должен быть либо 16, 24, или 32 байта в длину

# Функция для шифрования данных
def aes_encrypt(data):
    cipher = AES.new(key, AES.MODE_CBC) # Создаем новый шифр с режимом CBC
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size)) # Шифруем и паддим данные до нужного размера
    iv = base64.b64encode(cipher.iv).decode('utf-8') # IV для дешифрования
    ct = base64.b64encode(ct_bytes).decode('utf-8') # Зашифрованный текст
    return iv, ct

# Функция для дешифрования данных
def aes_decrypt(iv, ct):
    iv = base64.b64decode(iv) # Декодируем IV
    ct = base64.b64decode(ct) # Декодируем зашифрованный текст
    cipher = AES.new(key, AES.MODE_CBC, iv) # Создаем новый шифр с тем же режимом и IV
    pt = unpad(cipher.decrypt(ct), AES.block_size) # Дешифруем и убираем паддинг
    return pt.decode('utf-8')

# Пример использования
iv, ct = aes_encrypt("Дипломная работа")
print(f"Зашифрованное сообщение: {ct}")

pt = aes_decrypt(iv, ct)
print(f"Расшифрованное сообщение: {pt}")
