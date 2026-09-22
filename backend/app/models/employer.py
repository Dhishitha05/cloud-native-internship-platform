from app.extensions import db


class EmployerProfile(db.Model):
    __tablename__ = "employer_profiles"

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

    company_name = db.Column(
        db.String(150),
        nullable=False
    )

    company_description = db.Column(
        db.Text
    )

    company_website = db.Column(
        db.String(300)
    )

    industry = db.Column(
        db.String(100)
    )

    location = db.Column(
        db.String(150)
    )
    internships = db.relationship(
        "Internship",
        backref="employer",
        cascade="all, delete-orphan"
    )