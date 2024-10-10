# config.py
class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'yu'
    MYSQL_PASSWORD = 'forever25.'
    MYSQL_DB = 'skillbridge'
    SECRET_KEY = '2004'

class TestingConfig(Config):
    # 测试配置
    TESTING = True
    MYSQL_DATABASE_DB = 'test_database'  # 使用测试数据库
    # 其他测试配置可以在这里添加