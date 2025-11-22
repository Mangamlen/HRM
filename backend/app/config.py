import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('HRM_SECRET_KEY', 'unsafe-dev-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('HRM_DATABASE_URL', 'sqlite:///' + os.path.join(basedir, '..', 'hrm.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXP_DAYS = 7
