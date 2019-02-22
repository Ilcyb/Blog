def get_page(page, size):

    limit = size
    offset = size * (page - 1)

    return offset, limit