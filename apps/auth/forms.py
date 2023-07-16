# 匯入 FlaskForm
from flask_wtf import FlaskForm

# 匯入 密碼 內文 發送欄位
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


# 我們定義了一個SignUpForm類，它繼承自FlaskForm。
class SignUpForm(FlaskForm):
    username = StringField(
        #  字段在表單中的標籤為 "使用者名稱"。
        # 當渲染表單時，
        # ? 這個標籤將顯示在用戶輸入框的旁邊，
        # 讓使用者知道這個輸入框用於輸入使用者名稱。
        "使用者名稱",
        validators=[DataRequired("必須填寫使用者名稱"), Length(1, 30, "請勿超出30字元")],
    )

    email = StringField(
        "郵件位址",
        validators=[
            DataRequired("必須填入郵件位址"),
            Email("請依照格式輸入"),
        ],
    )

    password = PasswordField("密碼", validators=[DataRequired("必須填寫密碼")])

    submit = SubmitField("提交表單")


# 我們定義了一個LoginForm類，它繼承自FlaskForm。
class LoginForm(FlaskForm):
    email = StringField(
        # ? 這個標籤將顯示在用戶輸入框的旁邊，
        "郵件地址",
        validators=[
            # 如果使用者未填寫，則會顯示"必須填寫電子郵件"這個錯誤訊息。
            DataRequired("必須填寫電子郵件"),
            # 用於檢查使用者輸入的電子郵件地址是否符合郵件格式
            Email("請依郵件格式輸入"),
        ],
    )
    password = PasswordField(
        "密碼",
        validators=[
            DataRequired("必須填寫密碼"),
        ],
    )
    submit = SubmitField("登入")
