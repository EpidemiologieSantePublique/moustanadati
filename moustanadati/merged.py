
# ======= C:\Users\HP\ged_2\app.py =======

from flask import Flask, render_template,  redirect, url_for, request


from application.home.home_controller import HomeController
from application.login.login_controller import LoginController
from application.logout.logout_controller import LogoutController
from application.test.test_controller import TestController
from infrastructures.flask_response_html_renderer import FlaskResponseHTMLRenderer
from infrastructures.sqlite_users import SqliteUsers
from infrastructures.flask_session import FlaskSession
from infrastructures.bcrypt_encrypt_password import BcryptEncryptPassword
from application.login.login_use_case import LoginUseCase
from application.login.login_presenter import LoginPresenter
from application.login.login_view_model import LoginViewModel

# ===========================
# Initialisation de Flask
# ===========================
app = Flask(__name__)
app.secret_key = "supersecretkey"

# ===========================
# Routes
# ===========================
@app.route('/')
def home():
    controller = HomeController(session=FlaskSession(), users=SqliteUsers())
    vm = controller.handle()

    renderer = FlaskResponseHTMLRenderer()
    result = renderer.render(vm, template_name="home.html")
    return renderer.to_flask_response(result)


@app.route('/login', methods=['GET'])
def show_login_form():
    if FlaskSession().is_user_registered():
        return redirect(url_for("home"))

    vm = LoginViewModel(error=False, user_id=None)
    renderer = FlaskResponseHTMLRenderer()
    result = renderer.render(vm, template_name="login.html")
    return renderer.to_flask_response(result)


@app.route('/login', methods=['POST'])
def login_user():
    controller = LoginController(
        use_case=LoginUseCase(users=SqliteUsers(), encrtypt_password=BcryptEncryptPassword()),
        presenter=LoginPresenter(),
        session=FlaskSession()
    )
    vm = controller.handle(request.form.get("username"), request.form.get("password"))

    if vm.error:
        FlaskSession().flash("Invalid credentials", "error")
        vm.redirect_to = url_for("show_login_form")
    else:
        vm.redirect_to = FlaskSession().consume_redirect_after_login() or url_for("home")

    renderer = FlaskResponseHTMLRenderer()
    result = renderer.render(vm)
    return renderer.to_flask_response(result)


@app.route('/logout')
def logout():
    controller = LogoutController(session=FlaskSession())
    controller.handle()
    return redirect(url_for("home"))

@app.route('/test')
def test_page():
    session = FlaskSession()
    if not session.is_user_registered():
        session.set_redirect_after_login(request.path)
        return redirect(url_for("show_login_form"))

    controller = TestController(
        session=session,
        users=SqliteUsers()
    )
    vm = controller.handle()

    renderer = FlaskResponseHTMLRenderer()
    result = renderer.render(vm, template_name="test.html")
    return renderer.to_flask_response(result)



# ===========================
# 🚀 Lancement de l'application
# ===========================
if __name__ == '__main__':
    app.run(debug=True)

# ======= C:\Users\HP\ged_2\init_db.py =======

# init_db.py

import sqlite3
import uuid
import hashlib
from infrastructures.bcrypt_encrypt_password import BcryptEncryptPassword


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect("ged.db")
    cursor = conn.cursor()

    # Création de la table users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Génération de l'utilisateur
    user_id = str(uuid.uuid4())
    username = "user"
    password_hash = BcryptEncryptPassword().encrypt("1234")

    # Insertion si non existant
    cursor.execute("""
        INSERT OR IGNORE INTO users (id, username, password)
        VALUES (?, ?, ?)
    """, (user_id, username, password_hash))

    conn.commit()
    conn.close()
    print("✅ Base de données initialisée avec l'utilisateur 'user'.")

if __name__ == "__main__":
    init_db()

# ======= C:\Users\HP\ged_2\application\__init__.py =======


# ======= C:\Users\HP\ged_2\application\home\__init__.py =======


# ======= C:\Users\HP\ged_2\application\home\home_controller.py =======

# application/home/home_controller.py

from interfaces.session_interface import ISession
from interfaces.users_interface import IUsers
from application.home.home_view_model import HomeViewModel

class HomeController:
    def __init__(self, session: ISession, users: IUsers):
        self.session = session
        self.users = users

    def handle(self):
        if not self.session.is_user_registered():
            return HomeViewModel(is_user_registered=False)

        user_id = self.session.get_registered_user_id()
        user = self.users.get_user_by_id(user_id)
        return HomeViewModel(
            is_user_registered=True,
            user_id=user_id,
            username=user.username
        )

# ======= C:\Users\HP\ged_2\application\home\home_view_model.py =======

# application/home/home_view_model.py

class HomeViewModel:
    def __init__(self, is_user_registered: bool, user_id: str = None, username: str = None, redirect_to: str | None = None, headers: dict = None):
        self.is_user_registered = is_user_registered
        self.user_id = user_id
        self.username = username
        self.redirect_to = redirect_to
        self.headers = headers or {}

    def to_dict(self):
        return {
            "is_user_registered": self.is_user_registered,
            "user_id": self.user_id,
            "username": self.username
        }

# ======= C:\Users\HP\ged_2\application\login\__init__.py =======


# ======= C:\Users\HP\ged_2\application\login\login_controller.py =======

# application/login/login_controller.py

from application.login.login_use_case import LoginUseCase
from application.login.login_presenter_interface import ILoginPresenter
from application.login.login_view_model import LoginViewModel
from application.login.login_request_dto import LoginRequest
from interfaces.session_interface import ISession

class LoginController:
    def __init__(self, use_case: LoginUseCase, presenter: ILoginPresenter, session: ISession):
        self.use_case = use_case
        self.presenter = presenter
        self.session = session

    def handle(self, username: str, password: str) -> LoginViewModel:
        request = LoginRequest(username, password)
        self.use_case.presenter = self.presenter
        self.use_case.execute(request)

        vm = self.presenter.modelview
        if not vm.error:
            self.session.register_user_id(vm.user_id)
        return vm

# ======= C:\Users\HP\ged_2\application\login\login_presenter_interface.py =======

# application/login/login_presenter_interface.py

from abc import ABC, abstractmethod
from application.login.login_result_dto import LoginResult

class ILoginPresenter(ABC):
    @abstractmethod
    def present(self, result: LoginResult) -> None: pass

# ======= C:\Users\HP\ged_2\application\login\login_presenter.py =======

# application/login/login_presenter.py

from typing import Optional

from application.login.login_presenter_interface import ILoginPresenter
from application.login.login_view_model import LoginViewModel
from application.login.login_result_dto import LoginResult

class LoginPresenter(ILoginPresenter):
    def __init__(self):
        self.modelview: Optional[LoginViewModel] = None

    def present(self, result: LoginResult) -> None:
        self.modelview = LoginViewModel(
            error=result.error,
            user_id=result.user_id,
            headers={}
        )

# ======= C:\Users\HP\ged_2\application\login\login_request_dto.py =======

# application/login/login_request.dto.py


class LoginRequest:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

# ======= C:\Users\HP\ged_2\application\login\login_result_dto.py =======

# application/login/login_resukt.dto.py

class LoginResult:
    def __init__(self, error: bool, user_id: str | None):
        self.error = error
        self.user_id = user_id




# ======= C:\Users\HP\ged_2\application\login\login_use_case.py =======

# application/login/login_use_case.py

from interfaces.users_interface import IUsers
from interfaces.encrypt_password_interface import IEncryptePassword
from application.login.login_presenter_interface import ILoginPresenter
from application.login.login_request_dto import LoginRequest
from application.login.login_result_dto import LoginResult

class LoginUseCase:
    def __init__(self, users: IUsers, encrtypt_password: IEncryptePassword):
        self.users = users
        self.encrypt_password = encrtypt_password
        self.presenter: ILoginPresenter = None

    def execute(self, request: LoginRequest) -> None:
        user = self.users.get_user_by_username(request.username)
        if user and self.encrypt_password.verify(request.password, user.password):
            result = LoginResult(error=False, user_id=user.id)
        else:
            result = LoginResult(error=True, user_id=None)
        self.presenter.present(result)

# ======= C:\Users\HP\ged_2\application\login\login_view_model.py =======


# application/login/login_view_model.py

class LoginViewModel:
    def __init__(self, error: bool, user_id: str | None, redirect_to: str | None = None, headers: dict = None):
        self.error = error
        self.user_id = user_id
        self.redirect_to = redirect_to
        self.headers = headers or {}

    def to_dict(self):
        return {
            "error": self.error,
            "user_id": self.user_id
        }

# ======= C:\Users\HP\ged_2\application\logout\__init__.py =======


# ======= C:\Users\HP\ged_2\application\logout\logout_controller.py =======

# application/logout/logout_controller.py

from flask import url_for

from interfaces.session_interface import ISession
from application.logout.logout_view_model import LogoutViewModel

class LogoutController:
    def __init__(self, session: ISession):
        self.session = session

    def handle(self) -> LogoutViewModel:
        self.session.unregister_user()
        self.session.flash("Vous avez été déconnecté avec succès.", "info")
        return LogoutViewModel(redirect_to=url_for("home"))

# ======= C:\Users\HP\ged_2\application\logout\logout_view_model.py =======

# application/logout/login_view_model.py

class LogoutViewModel:
    def __init__(self, redirect_to: str | None = None, headers: dict = None):
        self.redirect_to = redirect_to
        self.headers = headers or {}

    def to_dict(self):
        return {}  # Pas de données à afficher, juste une redirection

# ======= C:\Users\HP\ged_2\application\test\__init__.py =======


# ======= C:\Users\HP\ged_2\application\test\test_controller.py =======

# application/test/test_controller.py

from interfaces.session_interface import ISession
from interfaces.users_interface import IUsers

from application.test.test_view_model import TestViewModel

class TestController:
    def __init__(self, session: ISession, users: IUsers):
        self.session = session
        self.users = users

    def handle(self) -> TestViewModel:
        user_id = self.session.get_registered_user_id()
        user = self.users.get_user_by_id(user_id)
        return TestViewModel(user_id=user.id, username=user.username)

# ======= C:\Users\HP\ged_2\application\test\test_view_model.py =======


# application/test/test_view_model.py

class TestViewModel:
    def __init__(self, user_id: str, username: str, redirect_to: str | None = None, headers: dict = None):
        self.user_id = user_id
        self.username = username
        self.redirect_to = redirect_to
        self.headers = headers or {}

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username
        }

# ======= C:\Users\HP\ged_2\entities\__init__.py =======


# ======= C:\Users\HP\ged_2\entities\user.py =======

# entities/user.py

class User:
    def __init__(self, id: str, username: str, password: str):
        self.id = id
        self.username = username
        self.password = password

# ======= C:\Users\HP\ged_2\infrastructures\__init__.py =======


# ======= C:\Users\HP\ged_2\infrastructures\bcrypt_encrypt_password.py =======

# infrastructures/encrypt_password_interface.py

import bcrypt
from interfaces.encrypt_password_interface import IEncryptePassword

class BcryptEncryptPassword(IEncryptePassword):
    def encrypt(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify(self, password: str, crypted_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), crypted_password.encode())

# ======= C:\Users\HP\ged_2\infrastructures\flask_response_html_renderer.py =======

# infrastructures/flask_response_html_renderer.py

from flask import render_template, Response, make_response, redirect

from interfaces.renderer_interface import IRenderer
from interfaces.renderer_interface import RenderResult
from interfaces.view_model_interface import IViewModel

class FlaskResponseHTMLRenderer(IRenderer):
    def render(self, viewmodel: IViewModel, template_name: str | None = None) -> RenderResult:
        if viewmodel.redirect_to:
            return RenderResult(redirect_to=viewmodel.redirect_to)

        body = render_template(template_name, **viewmodel.to_dict()) if template_name else ""
        return RenderResult(
            body=body,
            status_code=200,
            headers=viewmodel.headers
        )

    def to_flask_response(self, result: RenderResult) -> Response:
       

        if result.redirect_to:
            response = redirect(result.redirect_to)
        else:
            response = make_response(result.body, result.status_code)

        for k, v in result.headers.items():
            response.headers[k] = v

        return response

# ======= C:\Users\HP\ged_2\infrastructures\flask_session.py =======

# infrastructures/flask_session.py


from flask import session, flash as flask_flash

from interfaces.session_interface import ISession


class FlaskSession(ISession):
    def is_user_registered(self) -> bool:
        return self.get_registered_user_id() is not None

    def unregister_user(self):
        session.pop("user_id", None)

    def get_registered_user_id(self) -> str | None:
        return session.get("user_id")

    def register_user_id(self, user_id: str):
        session["user_id"] = user_id

    def set_redirect_after_login(self, url: str):
        session["redirect_after_login"] = url

    def consume_redirect_after_login(self) -> str | None:
        return session.pop("redirect_after_login", None)

    def flash(self, message: str, category: str = "info"):
        flask_flash(message, category)


# ======= C:\Users\HP\ged_2\infrastructures\sqlite_users.py =======

# infrastructures/sqlite_users.py

from interfaces.users_interface import IUsers
from entities.user import User

import sqlite3
from typing import Optional

class SqliteUsers(IUsers):
    def __init__(self, db_path: str = "ged.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE id = ? LIMIT 1", (user_id,))
        row = cursor.fetchone()
        return User(*row) if row else None

    def get_user_by_username(self, username: str) -> Optional[User]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ? LIMIT 1", (username,))
        row = cursor.fetchone()
        return User(*row) if row else None


# ======= C:\Users\HP\ged_2\interfaces\__init__.py =======


# ======= C:\Users\HP\ged_2\interfaces\encrypt_password_interface.py =======

# interfaces/encrypt_password_interface.py

from abc import ABC, abstractmethod

class IEncryptePassword(ABC):
    @abstractmethod
    def encrypt(self, password: str) -> str: pass
    @abstractmethod
    def verify(self, password: str, crypted_password: str) -> bool: pass


# ======= C:\Users\HP\ged_2\interfaces\renderer_interface.py =======

# interfaces/renderer_interface.py

from abc import ABC, abstractmethod
from typing import Optional
from interfaces.view_model_interface import IViewModel


from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class RenderResult:
    body: str = ""
    status_code: int = 200
    headers: dict = field(default_factory=dict)
    redirect_to: Optional[str] = None



class IRenderer(ABC):
    @abstractmethod
    def render(self, viewmodel: IViewModel, template_name: Optional[str] = None) -> RenderResult:
        pass

# ======= C:\Users\HP\ged_2\interfaces\session_interface.py =======

# interfaces/session_interface.py

from abc import ABC, abstractmethod

class ISession(ABC):
    @abstractmethod
    def is_user_registered(self) -> bool: pass
    @abstractmethod
    def get_registered_user_id(self) -> str | None: pass
    @abstractmethod
    def unregister_user(self): pass
    @abstractmethod
    def register_user_id(self, user_id: str): pass
    @abstractmethod
    def set_redirect_after_login(self, url: str): pass
    @abstractmethod
    def consume_redirect_after_login(self) -> str | None: pass
    @abstractmethod
    def flash(self, message: str, category: str = "info"): pass




# ======= C:\Users\HP\ged_2\interfaces\users_interface.py =======

# interfaces/users_interface.py

from abc import ABC, abstractmethod
from entities.user import User


class IUsers(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User | None: pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> User | None: pass

# ======= C:\Users\HP\ged_2\interfaces\view_model_interface.py =======

#interfaces/view_model_interface.py

from typing import Protocol

class IViewModel(Protocol):
    def to_dict(self) -> dict: ...
    redirect_to: str | None
    headers: dict
