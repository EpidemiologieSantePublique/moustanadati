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
