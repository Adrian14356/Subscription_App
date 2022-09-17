import os

class Config:

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT_INTERNAL')}/{os.getenv('POSTGRES_DATABASE')}"
    )
    SECRET_KEY = os.getenv('SECRET_KEY')
