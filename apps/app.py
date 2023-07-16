from pathlib import Path

from flask import Flask, render_template

# login
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# 簡易防範 csrf
from flask_wtf.csrf import CSRFProtect

# 加載組態物件
from apps.config import config

db = SQLAlchemy()

csrf = CSRFProtect()

# 建立 logingmanager 的實體
login_manager = LoginManager()
# 在 login_view屬性，指定未登入時重新導向的端點
login_manager.login_view = "auth.signup"
# 在 login_message 屬性指定登入後的顯示訊息
# 不顯示任何內容
login_manager.login_message = ""


#! 寫成函數可用 .env 檔案跟改要啟動的 app
#! 跟改 .env 後要重新啟動 flask
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

    # 與 db 連動
    db.init_app(app)
    Migrate(app, db)

    # login_manager 與 app 連動
    login_manager.init_app(app)

    # 增加防範 csrf 功能
    csrf.init_app(app)

    # ? 操作資料庫藍圖
    # 從 crud 套件匯入 views
    from apps.crud import views as crud_views

    # 將藍圖登入至應用程式
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    # ? 建立驗證功能藍圖
    from apps.auth import views as auth_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    @app.route("/")
    def index():
        return render_template("welcome.html")

    return app


def create_app2():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "hello"

    return app


# app = create_app()


# @app.route("/")
# def index():
#     return render_template("welcome.html")


# if __name__ == "__main__":
#     app.run()
