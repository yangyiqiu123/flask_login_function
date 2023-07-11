from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, length


# 新增與編輯使用者的表單類別
class UserForm(FlaskForm):
    # 設定表單中 username 屬性的標籤和驗證器
    username = StringField(
        "使用者名稱 ",
        validators=[
            DataRequired(message="必須填寫使用者名稱"),
            length(max=30, message="請勿輸入超過30個字元"),
        ],
    )
    # 設定表單中 email 屬性的標籤和驗證器
    email = StringField(
        "郵件位置 ",
        validators=[
            DataRequired(message="必須填寫電子郵件"),
            Email(message="請依照電子郵件格式輸入"),
        ],
    )
    # 設定表單中 password 屬性的標籤和驗證器
    password = PasswordField(
        "密碼 ",
        validators=[
            DataRequired(message="必須填寫密碼"),
        ],
    )
    # 設定表單中 submit 的內容
    submit = SubmitField("提交表單")

    # 自製驗證器
    # validate_ + 欄位名稱
    # def validate_username(self, username):
    #     if not username.data:
    #         raise ValidationError("必須填寫使用者名稱")
