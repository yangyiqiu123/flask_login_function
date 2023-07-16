from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from apps.app import db, login_manager


# 建立繼承 db.Model 的 User 類別
class User(db.Model, UserMixin):
    # 指定表格名稱
    __tablename__ = "users"
    # 定義直欄內容
    # primary_key :　每次新增一個新的 User 物件時，資料庫將自動為 id 欄位生成唯一的識別值，確保每個使用者都有唯一的主鍵值。
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def password(self):
        raise AttributeError("無法加載")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 檢測密碼
    # 檢測密碼是否與經過雜湊處理的密碼一致
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 檢測郵件位置是否已經有人使用
    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
