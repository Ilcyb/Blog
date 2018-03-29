from os import environ

class Config:
    mysql_username = environ.get('mysql_username')
    mysql_password = environ.get('mysql_password')
    mysql_host = '127.0.0.1'
    mysql_charset = 'utf8'

class DevConfig(Config):
    mysql_db = 'blog_dev'

class TestConfig(Config):
    mysql_db = 'blog_test'

class ProdConfig(Config):
    mysql_db = 'blog'


configs = {
    'default': DevConfig,
    'test': TestConfig,
    'product': ProdConfig
}