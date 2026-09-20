from datetime import datetime, timezone

from flask_login import UserMixin

from extensions import db, bcrypt


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Optional profile fields - all nullable, none required
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(120), nullable=True)
    photo_data = db.Column(db.LargeBinary, nullable=True)
    photo_mimetype = db.Column(db.String(50), nullable=True)

    def set_password(self, raw_password):
        self.password_hash = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    def __repr__(self):
        return f"<User {self.email}>"
