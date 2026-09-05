from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class UpdateNameForm(FlaskForm):
    name = StringField(
        "Full name",
        validators=[DataRequired(message="Enter your name."), Length(min=2, max=120)],
    )
    submit_name = SubmitField("Update name")


class UpdateEmailForm(FlaskForm):
    email = StringField(
        "New email",
        validators=[DataRequired(message="Enter an email."), Email(message="Enter a valid email address."), Length(max=255)],
    )
    current_password = PasswordField(
        "Current password",
        validators=[DataRequired(message="Enter your current password to confirm this change.")],
    )
    submit_email = SubmitField("Update email")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current password",
        validators=[DataRequired(message="Enter your current password.")],
    )
    new_password = PasswordField(
        "New password",
        validators=[DataRequired(message="Enter a new password."), Length(min=8, message="Use at least 8 characters.")],
    )
    confirm_new_password = PasswordField(
        "Confirm new password",
        validators=[DataRequired(message="Confirm your new password."), EqualTo("new_password", message="Passwords must match.")],
    )
    submit_password = SubmitField("Change password")