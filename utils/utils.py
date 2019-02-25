from datetime import datetime
from qiniu import Auth, put_data
import hashlib
import random

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

def upload_file_to_qiniu(acess_key, secret_key, bucket_name, file_name, file_data):
    try:
        q = Auth(acess_key, secret_key)

        file_ext, file_name = file_name.split('.')[-1:-3:-1]
        file_name_md5 = hashlib.md5((file_name + str(random.randint(0, 100))).encode()).hexdigest()

        token = q.upload_token(bucket_name, file_name_md5, 300)

        ret, info = put_data(token, file_name_md5, file_data)
    except Exception as e:
        return {'ret': False, 'msg': str(e)}
    else:
        return {'ret': True, 'key': ret['key']}

def get_file_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower()

def allowed_file(file_ext, allow_extensions):
    return file_ext in allow_extensions

def get_file_type(file_ext):
    if file_ext in ['jpg', 'jpeg', 'png', 'gif']:
        return 0
    else:
        return 1