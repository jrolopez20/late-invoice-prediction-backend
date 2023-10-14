import os


class Config:
    DEBUG: True


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost/test_db")
    API_KEY = os.environ.get("API_KEY", "")


config_settings = {"development": DevelopmentConfig}
