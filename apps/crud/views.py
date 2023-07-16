# 匯入 db
from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

from apps.app import db

# 匯入 使用者登入表單
from apps.crud.forms import UserForm

# 匯入 User 類別
from apps.crud.models import User

# 使用blueprint 建立 crud 應用程式
crud = Blueprint(
    # Blueprint 名稱家在各個端點名稱前面
    "crud",
    # Blueprint 應用程式套件(apps.crud.views)名稱
    # __name__ 是一个在 Python 中的特殊变量，它表示当前模块的名称。
    __name__,
    # 預設無效，優先度比跟目錄的低， 要特定的話一定要給
    template_folder="templates",
    # 預設無效，優先度比跟目錄的低， 要特定的話一定要給
    static_folder="static",
)


# 建立 index端點並回傳index.html
@crud.route("/")
@login_required
def index():
    # Flask 会在模板文件夹(templates)中查找名为 "crud/index.html" 的模板文件。
    return render_template("crud/index.html")


@crud.route("/users/new", methods=["GET", "POST"])
@login_required
def create_user():
    # 建立表單
    form = UserForm()
    # 驗證表單值
    if form.validate_on_submit():
        # 建立使用者
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)


@crud.route("/users")
@login_required
def users():
    # """取得使用者列表"""
    users = User.query.all()
    return render_template("crud/index.html", users=users)


@crud.route("/users/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    form = UserForm()

    # 使用 User 模型取得使用者
    user = User.query.filter_by(id=user_id).first()

    # 般情況下，form.validate_on_submit()方法會在POST 請求中進行驗證。
    # 它會檢查表單數據是否符合定義的驗證規則，並返回一個布爾值來表示驗證結果。
    # form.validate_on_submit()方法通常在處理POST 請求時進行表單驗證。對於GET 請求，它將始終返回False，
    #! 因為GET 請求不會提交表單數據。
    # 發送表單後，修改內容並重新導向使用者料表葉面
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))

    # form.validate() ， get會過
    # 請求方法為get時 回傳 html 檔案
    return render_template("crud/edit.html", user=user, form=form)


@crud.route("/users/<user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))


@crud.route("/sql")
@login_required
def sql():
    # 取得主健值為2的 User 物件
    # db.session.query(User).get(2)

    # 獲取全部記錄
    # db.session.query(User).all()

    # 獲取記錄總數
    # db.session.query(User).count()

    ########################################################################

    # 用 query filter進行select

    # 用 filter_by
    # 取德 id=2 username = "admin" 的所有紀錄
    # db.session.query(User).filter_by(id=2, username="adaim").all()

    # 用 filter
    # db.session.query(User).filter(User.id==2, User.username=="adaim").all()

    # 指定取得指定件數為1
    # db.session.query(User).limit(1).all()

    # 這個查詢的目的是在 User 模型中，查詢從索引為 2 開始的一筆記錄，並限制返回結果的數量為 1。
    # db.session.query(User).limit(1).offset(2).all()

    # 排序 username
    # db.session.query(User).order_by("username").all()

    # ? 重新排列user id 保持連續姓
    # users = User.query.order_by(User.id.asc()).all()
    # for index, user in enumerate(users, start=1):
    #     user.id = index
    #     db.session.add(user)
    # db.session.commit()

    # 建立 username 的群組
    # db.session.query(User).group_by("username").all()

    ########################################################################

    # # insert

    # # 建立使用者物件
    # user = User(username="使用者名稱", email="flaskbook@gmail.com", password="密碼")

    # # 增加使用者
    # db.session.add(user)

    # # 進行提交
    # db.session.commit()

    ########################################################################

    # # update
    # # 更改資料庫中的資料

    # # 先找到要改的
    # user = db.session.query(User).filter_by(id=1).first()

    # user.username = "使用者名稱2"
    # user.email = "flaskbook2@gmail.com"
    # user.password = "密碼2"
    # db.session.add(user)
    # db.session.commit()

    ########################################################################

    # # Delete

    # user = db.session.query(User).filter_by(id=1).delete()
    # db.session.commit()

    return "請確認控制台日志"
