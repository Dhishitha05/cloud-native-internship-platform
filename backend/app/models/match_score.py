from datetime import datetime

from app.extensions import db


class MatchScore(db.Model):
    __tablename__ = "match_scores"

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

    score = db.Column(
        db.Float,
        nullable=False
    )

    matched_skills = db.Column(
        db.Text
    )

    missing_skills = db.Column(
        db.Text
    )

    calculated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "internship_id",
            name="unique_match_score"
        ),
    )