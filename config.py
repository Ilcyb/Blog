from os import environ, urandom
from cryptography.fernet import Fernet

class Config:
    MYSQL_USERNAME = environ.get('MYSQL_USERNAME')
    MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD')
    BLOG_DATABASE = 'blog'
    MYSQL_CHARSET = 'utf8'
    ARTICLE_PER_PAGE = 6
    HOTEST_ARTICLE_NUMS = 5
    POWERD = 'Tencent Cloud'
    SECRET_KEY = urandom(24)
    FERNET_KEY = Fernet.generate_key()
    FERNET = Fernet(FERNET_KEY)
    COOKIE_EXPIRE = 3 * 60 * 60
    BEIAN = '粤ICP备19015827号'

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