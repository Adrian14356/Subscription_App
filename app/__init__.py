from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from app.config import Config
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow




db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
ma = Marshmallow()


def create_app():
    """
    Create app and records views
    :return:
    Transfer user to appropriate views
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app = app, db = db)

    from .main import (
        DashboardView,
        LoginView,
        RegisterView,
        LogoutView,
        AddSubscriptionView,
        DeleteSubscriptionView,
    )

    app.add_url_rule("/dashboard", view_func=DashboardView.as_view("dashboard"))
    app.add_url_rule("/login", view_func=LoginView.as_view("login"))
    app.add_url_rule("/register", view_func=RegisterView.as_view("register"))
    app.add_url_rule("/logout", view_func=LogoutView.as_view("logout"))
    app.add_url_rule("/add", view_func=AddSubscriptionView.as_view("add"))
    app.add_url_rule("/delete/<int:id>", view_func=DeleteSubscriptionView.as_view("delete"))

    return app
