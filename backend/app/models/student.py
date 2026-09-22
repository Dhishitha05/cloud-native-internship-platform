from app.extensions import db


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    college = db.Column(
        db.String(150),
        nullable=False
    )
    branch = db.Column(db.String(100))
    degree = db.Column(
        db.String(100),
        nullable=False
    )

    graduation_year = db.Column(
        db.Integer,
        nullable=False
    )

    bio = db.Column(
        db.Text
    )

    resume_url = db.Column(
        db.String(500)
    )
    interests = db.Column(
        db.Text
    )
    preferred_domain = db.Column(
        db.String(100)
    )
    applications = db.relationship(
        "Application",
        backref="student",
        cascade="all, delete-orphan"
    )
    match_scores = db.relationship(
        "MatchScore",
        backref="student",
        cascade="all, delete-orphan"
    )