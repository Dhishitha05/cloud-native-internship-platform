from datetime import datetime

from app.extensions import db


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student_profiles.id"),
        nullable=False
    )

    internship_id = db.Column(
        db.Integer,
        db.ForeignKey("internships.id"),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="APPLIED",
        nullable=False
    )

    cover_letter = db.Column(
        db.Text
    )

    resume_url = db.Column(
        db.String(500)
    )

    applied_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "internship_id",
            name="unique_student_application"
        ),
    )