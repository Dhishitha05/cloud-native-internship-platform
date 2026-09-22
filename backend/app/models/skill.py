from app.extensions import db


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    category = db.Column(
        db.String(100)
    )

    student_skills = db.relationship(
        "StudentSkill",
        backref="skill",
        cascade="all, delete-orphan"
    )
    internship_skills = db.relationship(
        "InternshipSkill",
        backref="skill",
        cascade="all, delete-orphan"
    )
class StudentSkill(db.Model):
    __tablename__ = "student_skills"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student_profiles.id"),
        nullable=False
    )

    skill_id = db.Column(
        db.Integer,
        db.ForeignKey("skills.id"),
        nullable=False
    )

    proficiency = db.Column(
        db.String(50)
    )

    years_experience = db.Column(
        db.Float
    )

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "skill_id",
            name="unique_student_skill"
        ),
    )
class InternshipSkill(db.Model):
    __tablename__ = "internship_skills"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    internship_id = db.Column(
        db.Integer,
        db.ForeignKey("internships.id"),
        nullable=False
    )

    skill_id = db.Column(
        db.Integer,
        db.ForeignKey("skills.id"),
        nullable=False
    )

    skill_type = db.Column(
        db.String(20),
        nullable=False
    )

    weight = db.Column(
        db.Float,
        default=1.0
    )

    __table_args__ = (
        db.UniqueConstraint(
            "internship_id",
            "skill_id",
            name="unique_internship_skill"
        ),
    )
    