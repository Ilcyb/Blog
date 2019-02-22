from datetime import datetime

def get_page(page, size):

    limit = size
    offset = size * (page - 1)

    return offset, limit

def format_datetime(dt : datetime):
    return dt.strftime('%Y-%m-%d %H:%M')