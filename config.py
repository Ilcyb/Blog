from os import environ

class Config:
    MYSQL_USERNAME = environ.get('local_mysql_username')
    MYSQL_PASSWORD = environ.get('mysql_password')
    MYSQL_HOST = '127.0.0.1'
    MYSQL_CHARSET = 'utf8'
    ARTICLE_PER_PAGE = 6
    HOTEST_ARTICLE_NUMS = 5
    POWERD = 'Tencent Cloud'

class DevConfig(Config):
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