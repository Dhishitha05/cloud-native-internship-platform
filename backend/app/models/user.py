from datetime import datetime

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    student_profile = db.relationship(
        "StudentProfile",
        backref="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    employer_profile = db.relationship(
        "EmployerProfile",
        backref="user",
        uselist=False,
        cascade="all, delete-orphan"
    )