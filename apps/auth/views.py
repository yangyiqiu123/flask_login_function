from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user

from apps.app import db
from apps.auth.forms import LoginForm, SignUpForm
from apps.crud.models import User

# 用 blueprint 產生 auth
auth = Blueprint(
    # 第一個參數「 blueprint 」是 Flask Blueprint 的名稱，被用於路由的指定
    # 設定 endpoint 的前面的字
    # auth.index  crud.index  index 是不一樣的
    # 还是回到 url_for 函数，如果你在 html 的 jinja2 中调用，
    # 得这样写 url_for('name.index')，其中的 name 就是你定义的蓝图的 name 参数。
    "auth",
    # 第二個參數「 __name__ 」是 Flask Blueprint 的匯入名稱，這個名稱指定了 Blueprint 的來源。
    # __name__ 是一個內建變數，用於取得目前模組（檔案）的名稱。
    # 在建立藍圖（Blueprint）的過程中，將 __name__ 作為參數傳遞給藍圖建構函式的第二個參數，用於指定藍圖的名稱。
    __name__,
    template_folder="templates",
    static_folder="static",
)


# auth 是藍圖註冊到app 的名字
@auth.route("/")
def index():
    # 防止與其他藍圖的模板路徑重複
    # ? 要在 template 下建立 auth 目錄
    return render_template("auth/index.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        # 檢測郵件地址是否已經有人使用
        if user.is_duplicate_email():
            flash("這個郵件位址已經註冊過")
            return redirect(url_for("auth.signup"))

        # 登入使用者資訊
        db.session.add(user)
        db.session.commit()
        # 獎使用者資訊存入 session
        # 1
        # 保持登錄狀態：在使用 login_user 方法後，Flask-Login
        # 將自動管理用戶的登錄會話，並在後續請求中識別用戶，知道哪個用戶是已登錄的。
        # 2
        # 訪問保護：使用 login_user 方法後，我們可以通過 @login_required
        # 裝飾器來保護某些路由或視圖，只有已登錄的用戶才能訪問這些頁面。
        login_user(user)

        # 当用户未登录时访问需要登录的页面时，你可以将用户重定向到登录页面，
        # 并在登录成功后将其重定向回原始请求的页面。
        # 这时可以使用 next 参数来存储原始请求的 URL。
        # 在用户成功登录后，你可以从 next 参数中获取原始请求的 URL，并进行重定向

        # 運作步驟
        # 1
        # 點了有加 @login_required 的頁面
        # 2
        # Flask-Login 将会检查用户是否已经登录。
        # 如果用户未登录，则会将其重定向到登录页面，要求用户进行身份验证。
        # 只有在用户登录后，才能成功访问被保护的视图函数。
        # 3
        # 導向到的登錄頁面由 apps/app 中的
        # login_manager.login_view = "auth.signup" 指定
        # 4
        # @login_required在重定向时，会将原始请求的 URL 作为 next 参数添加到登录页面的 URL 中。
        # 5
        # 跳來這裡
        # 6
        # https://blog.csdn.net/it_zhonghua/article/details/89420896
        # 這裡的 next 是從表單的 form action傳來的，不是自己在網址上取得的
        # 如果 form action 沒傳 next近來
        # next_ 會返回 none
        # 遇到这种情况的时候会出现next参数为none的情况，因为跳转到登录页面是是有next参数的，
        # 但是点击登陆之后的URL next参数就没有了。
        next_ = request.args.get("next")
        print("---------------------------------------------------------")
        url = request.url  # 獲取完整的URL
        print(url)
        # print(next2)
        print(next_)
        # 如果原本要連進來的地方就是這裡的話
        # 或不是一個有效路徑的話
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("crud.users")
        return redirect(next_)
    return render_template("auth/signup.html", form=form)


@auth.route("/login", methods=["Get", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 獲取電子郵件
        user = User.query.filter_by(email=form.email.data).first()

        # 如果使用者存在且ˇ密碼一至 允許登入
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("crud.users"))
        flash("郵件或密碼不正確")
    return render_template("auth/login.html", form=form)
