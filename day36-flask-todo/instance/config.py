import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL',
    'postgresql://todouser:todopass@db:5432/tododb'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
