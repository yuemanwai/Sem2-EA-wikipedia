import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # 放上cloud, 可以簡用rds, 放endpoint係(.env)
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS').split(',')
    POSTS_PER_PAGE = 10
    LANGUAGES = ['en', 'es', 'zh']
    # 要有domain,然後去google申請條key, https://www.google.com/recaptcha/admin
    RECAPTCHA_PUBLIC_KEY=os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY=os.environ.get('RECAPTCHA_PRIVATE_KEY')