import re
from typing import Union

import bcrypt
from flask import Response, flash, redirect, render_template, request, session, url_for
from flask.views import MethodView

from app import db
from app.models import Subscriptions, Users

def add_to_db(new_subscription: Subscriptions) -> None:
    """
    Add new subscription to DataBase
    :param new_subscription: refer to Subscription Database
    :return:
    None
    """

    db.session.add(new_subscription)
    db.session.commit()


def delete_from_db(subscription_to_delete: Subscriptions) -> None:
    """
    Delete the selected subscription
    :param subscription_to_delete: Refer to Subscription DataBase
    :return:
    None
    """
    db.session.delete(subscription_to_delete)
    db.session.commit()


class LoginView(MethodView):
    def __init__(self):
        self.template_name = "login.html"

    def __check_if_password_valid(self, found_user, put_password):
        """
        Check if the password is correct
        :param found_user: Refer to the function field
        :param put_password: Refer to password
        :return:
        Depending on whether the password is correct or incorrect, it returns boolean
        """
        password = found_user.password

        if bcrypt.checkpw(
            str.encode(put_password, "utf-8"), str.encode(password, "utf-8")
        ):
            return True
        else:
            return False

    def get(self):
        """
        Check if the user is logged in session
        :effect:
        If user is logged in transfers to dashboard, if not transfers to login
        """

        if request.method == "GET" and "nick" not in session:
            return render_template("login.html")

        elif request.method == "GET" and "nick" in session:
            flash("You are logged !", "success")
            return redirect(url_for("dashboard"))

    def __invalid_credentials(self):
        """
        If user data are incorrect flash information
        :return:
        Return redirect to login
        """
        flash("Invalid username or password", "warning")
        return redirect(url_for("login"))

    def post(self) -> Union[Response, str]:
        """
        Login function
        :return:
        If login was successful transfer user to the dashboard otherwise it checks whether user data are correct
        """
        nickname = request.form["nickname"]
        password = request.form["password"]
        found_user = Users.query.filter_by(user_name=nickname).first()

        if found_user:
            is_password_valid = self.__check_if_password_valid(found_user, password)

            if is_password_valid is True:
                session["nickname"] = found_user.user_name
                session["email"] = found_user.email
                session["id"] = found_user._id
                flash("Logged successful!", "success")
                return redirect(url_for("dashboard"))

        return self.__invalid_credentials()


class RegisterView(MethodView):
    def __init__(self):
        self.template_name = "register.html"

    def get(self):

        """
        Renders templates of registration
        :return:
        Rendered template
        """

        return render_template("register.html")

    def post(self) -> Union[Response, str]:
        """
        Register user and check if he has an account
        :return:
        If user doesn't have an account register and return to login, otherwise flash information about having account
        """

        nickname = request.form["nickname"]
        email = request.form["email"]
        password = request.form["password"]
        found_user = Users.query.filter_by(user_name=nickname).first()

        if not found_user:
            new_user = Users(user_name=nickname, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("You have been successful register", "success")
            return redirect(url_for("login"))

        flash("You have been account", "warning")
        return redirect(url_for("register"))


class DashboardView(MethodView):
    def __init__(self):
        self.template_name = "dashboard.html"

    def get(self) -> Union[Response, str]:
        """
        Show information about owned subscriptions and check information about logged in session
        :return:
        If user is in session return dashboard otherwise transfer user to login
        """
        if "nickname" in session:
            nickname = session["nickname"]
            email = session["email"]
            id = session["id"]
            subscriptions = Subscriptions.query.filter_by(user_id=id).all()

            return render_template(
                self.template_name,
                nickname=nickname,
                email=email,
                subscriptions=subscriptions,
            )

        flash("You are not logged in !", "warning")

        return redirect(url_for("login"))

    def delete(self):
        """
        Delete selected subscription from DataBase
        :return:
        Delete subscription and flash information about deletion
        """
        subscription_id = session["id"]
        subscription_to_delete = Subscriptions.query.get(name=subscription_id)

        delete_from_db(subscription_to_delete)
        flash("Subscription deleted!", "success")


class AddSubscriptionView(MethodView):
    def __init__(self):
        """
        Set regex formats for price and data
        """
        self.template_name = "AddSubscription.html"
        self.DATE_FORMAT = "^((?:(\d{2}-\d{2}-\d{4})))$"
        self.PRICE_FORMAT = "[-+]?\d*\.|,?\d+|\d+"

    def get(self):
        return render_template("AddSubscription.html")

    def post(self) -> Union[Response, str]:
        """
        Adds subscription to DataBase and check do we have similar subscription, data and price format
        :return:
        If we don't have similar subscription and regex is correct  return flash information  about added subscription
        and transfer to dashboard otherwise if we have similar subscription flash message about existing subscription.
        If regex(data,price) is incorrect flash information about the wrong format and return user to Add
        """

        subscription_name = request.form["name"]
        start_date = request.form["start_date"]
        price = request.form["price"]
        found_subscription = Subscriptions.query.filter_by(
            name=subscription_name
        ).first()

        if "nickname" not in session:
            flash("You are not logged in !", "warning")

            return redirect(url_for("login"))

        elif found_subscription:
            flash("You have already subscription!", "warning")
            return redirect(url_for("add"))

        elif re.search(self.DATE_FORMAT, start_date) and re.search(
            self.PRICE_FORMAT, price
        ):
            new_subscription = Subscriptions(
                name=subscription_name,
                start_date=start_date,
                price=price,
                user_id=session["id"],
            )

            add_to_db(new_subscription)
            flash("Your subscription have been added", "success")
            return redirect(url_for("dashboard"))

        flash("Correct format is: d-m-y and price format is: 0,0 or 0.0", "warning")
        return redirect(url_for("add"))


class LogoutView(MethodView):
    def __init__(self):
        self.template_name = "logout.html"

    def get(self) -> Union[Response, str]:
        """
        Logout user from the session
        :return:
        If nickname is in session logout user elif transfer user to login
        """
        if "nickname" in session:
            session.pop("nickname", None)
            session.pop("email", None)
            flash("You have been logout", "success")

        elif request.method == "GET" and "nick" not in session:
            return redirect(url_for("login"))
        elif request.method == "GET" and "nick" in session:
            flash("You have account", "waring")

        return redirect(url_for("login"))


class DeleteSubscriptionView(MethodView):
    def delete(self, id):
        """
        Delete subscription by the request from HTML
        :param id: Get subscription id
        :return:
        Delete subscription from the Database and return information
        """

        subscription_to_delete = Subscriptions.query.get(id)
        delete_from_db(subscription_to_delete)
        return "Delete success", 204
