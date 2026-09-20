from flask import Blueprint, Response, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from extensions import db
from forms.account_forms import ChangePasswordForm, ProfileForm, UpdateEmailForm, UpdateNameForm
from models.user import User

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.before_request
@login_required
def require_login():
    pass


def _build_forms(name=None, email=None, bio=None, location=None):
    return {
        "name_form": UpdateNameForm(name=name if name is not None else current_user.name),
        "email_form": UpdateEmailForm(email=email if email is not None else current_user.email),
        "password_form": ChangePasswordForm(),
        "profile_form": ProfileForm(
            bio=bio if bio is not None else current_user.bio,
            location=location if location is not None else current_user.location,
        ),
    }


@dashboard_bp.route("/")
def index():
    return render_template("dashboard.html", **_build_forms())


@dashboard_bp.route("/update-name", methods=["POST"])
def update_name():
    forms = _build_forms()
    name_form = UpdateNameForm()
    forms["name_form"] = name_form

    if name_form.validate_on_submit():
        current_user.name = name_form.name.data.strip()
        db.session.commit()
        flash("Your name has been updated.", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("dashboard.html", **forms)


@dashboard_bp.route("/update-email", methods=["POST"])
def update_email():
    forms = _build_forms()
    email_form = UpdateEmailForm()
    forms["email_form"] = email_form

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

    return render_template("dashboard.html", **forms)


@dashboard_bp.route("/change-password", methods=["POST"])
def change_password():
    forms = _build_forms()
    password_form = ChangePasswordForm()
    forms["password_form"] = password_form

    if password_form.validate_on_submit():
        if not current_user.check_password(password_form.current_password.data):
            flash("Current password is incorrect.", "error")
        else:
            current_user.set_password(password_form.new_password.data)
            db.session.commit()
            flash("Your password has been changed.", "success")
            return redirect(url_for("dashboard.index"))

    return render_template("dashboard.html", **forms)


@dashboard_bp.route("/update-profile", methods=["POST"])
def update_profile():
    forms = _build_forms()
    profile_form = ProfileForm()
    forms["profile_form"] = profile_form

    if profile_form.validate_on_submit():
        current_user.bio = profile_form.bio.data.strip() if profile_form.bio.data else None
        current_user.location = profile_form.location.data.strip() if profile_form.location.data else None

        photo_file = profile_form.photo.data
        if photo_file and photo_file.filename:
            current_user.photo_data = photo_file.read()
            current_user.photo_mimetype = photo_file.mimetype

        db.session.commit()
        flash("Your profile has been updated.", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("dashboard.html", **forms)


@dashboard_bp.route("/photo/<int:user_id>")
def photo(user_id):
    user = User.query.get_or_404(user_id)
    if not user.photo_data:
        return "", 404
    return Response(user.photo_data, mimetype=user.photo_mimetype or "image/jpeg")
