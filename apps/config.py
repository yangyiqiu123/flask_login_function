from pathlib import Path

basedir = Path(__file__).parent.parent


# 建立baseconfig類
class BaseConfig:
    SECRET_KEY = "2AZSMss3P5QpbcY2hBsJ"
    WTF_CSRF_SECRET_KEY = "AuwzyszU5sugKN7KZs6f"


class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


# 繼承 baseconfig 類，建立testconfig類
class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 測試不需要 csrf
    WTF_CSRF_ENABLED = False


config = {
    "testing": TestingConfig,
    "local": LocalConfig,
}
