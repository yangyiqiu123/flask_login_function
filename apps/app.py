from pathlib import Path

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# 簡易防範 csrf
from flask_wtf.csrf import CSRFProtect

# 加載組態物件
from apps.config import config

db = SQLAlchemy()

csrf = CSRFProtect()


def create_app(config_key):
    app = Flask(__name__)

    # 設定應用程式的組態 from_mapping 方法
    # app.config.from_mapping(
    #     SECRET_KEY="2AZSMss3P5QpbcY2hBsJ",
    #     # __file__获取当前的路径
    #     SQLALCHEMY_DATABASE_URI=(
    #         f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}"
    #     ),
    #     # 防止彈出警告
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False,
    #     SQLALCHEMY_ECHO=True,
    #     # 增加防範 csrf 功能
    #     WTF_CSRF_SECRET_KEY="AuwzyszU5sugKN7KZs6f",
    # )

    app.config.from_object(config[config_key])

    db.init_app(app)
    Migrate(app, db)

    # 增加防範 csrf 功能
    csrf.init_app(app)

    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    @app.route("/")
    def index():
        return render_template("welcome.html")

    return app


# app = create_app()


# @app.route("/")
# def index():
#     return render_template("welcome.html")


# if __name__ == "__main__":
#     app.run()
