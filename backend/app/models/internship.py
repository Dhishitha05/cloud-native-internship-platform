from datetime import datetime

from app.extensions import db


class Internship(db.Model):
    __tablename__ = "internships"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    employer_id = db.Column(
        db.Integer,
        db.ForeignKey("employer_profiles.id"),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    domain = db.Column(
        db.String(100),
        nullable=False
    )

    location = db.Column(
        db.String(150)
    )

    duration_months = db.Column(
        db.Integer
    )

    stipend = db.Column(
        db.Float
    )

    eligibility = db.Column(
        db.Text
    )

    application_deadline = db.Column(
        db.DateTime
    )

    status = db.Column(
        db.String(30),
        default="OPEN",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    internship_skills = db.relationship(
        "InternshipSkill",
        backref="internship",
        cascade="all, delete-orphan"
    )
    applications = db.relationship(
        "Application",
        backref="internship",
        cascade="all, delete-orphan"
    )
    match_scores = db.relationship(
        "MatchScore",
        backref="internship",
        cascade="all, delete-orphan"
    )