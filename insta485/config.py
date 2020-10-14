"""Insta485 development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = (
    b'>\x91@>\\o?\x03\x8bk\x06\xb7L\xbf\xcd\xf7\x84\x84\x93z\xdd)\n\xb6'
)
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
INSTA485_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = INSTA485_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = INSTA485_ROOT/'var'/'insta485.sqlite3'

POSTGRESQL_DATABASE_HOST = "localhost"
POSTGRESQL_DATABASE_PORT = 5432
POSTGRESQL_DATABASE_USER = "postgres"
POSTGRESQL_DATABASE_PASSWORD = None
POSTGRESQL_DATABASE_DB = "insta485"
