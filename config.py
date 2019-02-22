from os import environ

class Config:
    MYSQL_USERNAME = environ.get('MYSQL_USERNAME')
    MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD')
    MYSQL_HOST = environ.get('MYSQL_HOST', '127.0.0.1')
    MYSQL_PORT = environ.get('MYSQL_PORT', 3306)
    BLOG_DATABASE = 'blog'
    MYSQL_CHARSET = 'utf8'
    ARTICLE_PER_PAGE = 6
    HOTEST_ARTICLE_NUMS = 5
    POWERD = 'Tencent Cloud'
    SECRET_KEY = 'H^8dh2{^,?'
    BEIAN = '粤ICP备19015827号'

class DevConfig(Config):
    MYSQL_USERNAME = environ.get('MYSQL_USERNAME', 'root')
    MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD', 'root')
    MYSQL_DB = 'blog'

class TestConfig(Config):
    MYSQL_DB = 'blog_test'

class ProdConfig(Config):
    MYSQL_DB = 'blog'


configs = {
    'default': DevConfig,
    'test': TestConfig,
    'product': ProdConfig
}