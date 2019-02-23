from datetime import datetime

def get_page(page, size):

    limit = size
    offset = size * (page - 1)

    return offset, limit

def format_datetime(dt : datetime):
    return dt.strftime('%Y-%m-%d %H:%M')

def enctry_string(s, key, fernet):
    enctry_s = fernet.encrypt(s.encode())
    return enctry_s.decode()

def dectry_string(enctry_s, key, fernet):
    s_byte = fernet.decrypt(enctry_s.encode())
    return s_byte.decode()
