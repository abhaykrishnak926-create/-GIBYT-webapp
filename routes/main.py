from flask import Blueprint, flash, redirect, render_template, url_for

from extensions import db
from forms.contact_form import ContactForm
from models.contact_message import ContactMessage

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/work")
def work():
    return render_template("work.html")


@main_bp.route("/products")
def products():
    return render_template("products.html")


@main_bp.route("/careers")
def careers():
    return render_template("careers.html")


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        entry = ContactMessage(
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            subject=form.subject.data.strip(),
            message=form.message.data.strip(),
        )
        db.session.add(entry)
        db.session.commit()
        flash("Thanks - we've got your message and will get back to you soon.", "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html", form=form)