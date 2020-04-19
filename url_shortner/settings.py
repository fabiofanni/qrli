import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3' #os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

#DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'


