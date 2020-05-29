import os, redis
from app import app

SECRET_KEY = os.getenv('SECRET_KEY', 'SECRET KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 自行配置
SQLALCHEMY_DATABASE_URI = ''
secret_key = '111111'

POST_PER_PAGE = 5

