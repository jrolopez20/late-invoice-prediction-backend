import os


class Config:
    DEBUG: True


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost/test_db")


config_settings = {"development": DevelopmentConfig}
