from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(message="Enter your name."), Length(max=120)],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Enter your email."),
            Email(message="Enter a valid email address."),
            Length(max=255),
        ],
    )
    subject = StringField(
        "Subject",
        validators=[DataRequired(message="Enter a subject."), Length(max=200)],
    )
    message = TextAreaField(
        "Message",
        validators=[DataRequired(message="Enter a message."), Length(max=5000)],
    )
    submit = SubmitField("Send message")