from os import environ, urandom

class Config:
    MYSQL_USERNAME = environ.get('MYSQL_USERNAME')
    MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD')
    BLOG_DATABASE = 'blog'
    MYSQL_CHARSET = 'utf8'
    ARTICLE_PER_PAGE = 6
    HOTEST_ARTICLE_NUMS = 5
    POWERD = 'Tencent Cloud'
    SECRET_KEY = urandom(24)
    COOKIE_EXPIRE = 3 * 60 * 60
    BEIAN = '粤ICP备19015827号'
    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])
    MAX_CONTENT_LENGTH = 1024 * 1024 * 10
    QINIU_ACCESS_KEY = environ.get('QINIU_ACCESS_KEY')
    QINIU_SECRET_KEY = environ.get('QINIU_SECRET_KEY')
    QINIU_BUCKET_NAME = environ.get('QINIU_BUCKET_NAME')
    QINIU_BUCKET_URL = environ.get('QINIU_BUCKET_URL')

class DevConfig(Config):
    MYSQL_USERNAME = environ.get('MYSQL_USERNAME', 'root')
    MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD', 'root')
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306

class TestConfig(Config):
    pass

class ProdConfig(Config):
    MYSQL_HOST = environ.get('MYSQL_HOST')
    MYSQL_PORT = environ.get('MYSQL_PORT')


configs = {
    'default': DevConfig,

    'dev': DevConfig,
    'test': TestConfig,
    'production': ProdConfig
}