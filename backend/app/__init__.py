import os

from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import text

from .extensions import db, migrate, jwt
from .models import (
    User,
    StudentProfile,
    EmployerProfile,
    Skill,
    StudentSkill,
    InternshipSkill,
    Internship,
    Application,
    MatchScore
)
from .routes.students import students_bp
from .routes.employers import employers_bp
from .routes.internships import internships_bp
from .routes.applications import applications_bp
from .routes.skills import skills_bp
from .routes.matching import matching_bp
# Load .env before creating the Flask app
load_dotenv()


def create_app():
    app = Flask(__name__)

    # Read database configuration
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    # Check that required configuration exists
    if not all([db_user, db_password, db_host, db_port, db_name]):
        raise RuntimeError("Database configuration is missing from .env")

    # MySQL connection
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    from .routes.auth import auth_bp
    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )
    app.register_blueprint(
        students_bp,
        url_prefix="/api/students"
    )
    app.register_blueprint(
        employers_bp,
        url_prefix="/api/employers"
    )
    app.register_blueprint(
        internships_bp,
        url_prefix="/api/internships"
    )
    app.register_blueprint(
        applications_bp,
        url_prefix="/api/applications"
    )
    app.register_blueprint(
        skills_bp,
        url_prefix="/api/skills"
    )
    app.register_blueprint(
        matching_bp,
        url_prefix="/api/matching"
    )
    @app.route("/")
    def home():
        return {
            "message": "Cloud-Native Internship & Skill Matching Platform API is running!"
        }

    @app.route("/db-test")
    def db_test():
        try:
            result = db.session.execute(text("SELECT DATABASE()"))
            database_name = result.scalar()

            return {
                "status": "success",
                "database": database_name
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }, 500

    return app