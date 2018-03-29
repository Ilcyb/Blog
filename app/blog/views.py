from . import blog

@blog.route('/')
def index(methods=['GET']):
    return 'hello wordl'