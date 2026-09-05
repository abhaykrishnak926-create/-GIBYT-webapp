from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from extensions import db
from forms.account_forms import ChangePasswordForm, UpdateEmailForm, UpdateNameForm
from models.user import User

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.before_request
@login_required
def require_login():
    pass


@dashboard_bp.route("/")
def index():
    name_form = UpdateNameForm(name=current_user.name)
    email_form = UpdateEmailForm(email=current_user.email)
    password_form = ChangePasswordForm()
    return render_template(
        "dashboard.html",
        name_form=name_form,
        email_form=email_form,
        password_form=password_form,
    )


@dashboard_bp.route("/update-name", methods=["POST"])
def update_name():
    name_form = UpdateNameForm()
    email_form = UpdateEmailForm(email=current_user.email)
    password_form = ChangePasswordForm()

    if name_form.validate_on_submit():
        current_user.name = name_form.name.data.strip()
        db.session.commit()
        flash("Your name has been updated.", "success")
        return redirect(url_for("dashboard.index"))

    return render_template(
        "dashboard.html",
        name_form=name_form,
        email_form=email_form,
        password_form=password_form,
    )


@dashboard_bp.route("/update-email", methods=["POST"])
def update_email():
    name_form = UpdateNameForm(name=current_user.name)
    email_form = UpdateEmailForm()
    password_form = ChangePasswordForm()

    if email_form.validate_on_submit():
        if not current_user.check_password(email_form.current_password.data):
            flash("Current password is incorrect.", "error")
        else:
            new_email = email_form.email.data.strip().lower()
            existing = User.query.filter(User.email == new_email, User.id != current_user.id).first()
            if existing:
                flash("That email is already in use by another account.", "error")
            else:
                current_user.email = new_email
                db.session.commit()
                flash("Your email has been updated.", "success")
                return redirect(url_for("dashboard.index"))

    return render_template(
        "dashboard.html",
        name_form=name_form,
        email_form=email_form,
        password_form=password_form,
    )


@dashboard_bp.route("/change-password", methods=["POST"])
def change_password():
    name_form = UpdateNameForm(name=current_user.name)
    email_form = UpdateEmailForm(email=current_user.email)
    password_form = ChangePasswordForm()

    if password_form.validate_on_submit():
        if not current_user.check_password(password_form.current_password.data):
            flash("Current password is incorrect.", "error")
        else:
            current_user.set_password(password_form.new_password.data)
            db.session.commit()
            flash("Your password has been changed.", "success")
            return redirect(url_for("dashboard.index"))

    return render_template(
        "dashboard.html",
        name_form=name_form,
        email_form=email_form,
        password_form=password_form,
    )