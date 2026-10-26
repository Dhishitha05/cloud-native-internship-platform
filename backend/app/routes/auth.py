from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models.user import User
from app.models.student import StudentProfile
from app.models.employer import EmployerProfile
from app.decorators import role_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/test", methods=["GET"])
def auth_test():
    return jsonify({
        "message": "Authentication API is working"
    })


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not name or not email or not password or not role:
        return jsonify({
            "error": "name, email, password and role are required"
        }), 400

    role = role.upper()

    if role not in ("STUDENT", "EMPLOYER"):
        return jsonify({
            "error": "Role must be STUDENT or EMPLOYER"
        }), 400

    company_name = data.get("company_name")

    if role == "EMPLOYER" and not company_name:
        return jsonify({
            "error": "company_name is required for employers"
        }), 400
    current_app.logger.info("Registration email received: %r", email)
    if User.query.filter_by(email=email).first():
        current_app.logger.warning(
        "Email already exists in database: %r", email
        )
        return jsonify({"error": "Email already registered"}), 409

    try:
        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            role=role
        )

        db.session.add(user)
        db.session.flush()

        if role == "STUDENT":
            profile = StudentProfile(
                user_id=user.id,
                college="",
                degree="",
                branch="",
                graduation_year=2028,
                bio="",
                resume_url="",
                interests="",
                preferred_domain=""
            )
        else:
            profile = EmployerProfile(
                user_id=user.id,
                company_name=company_name,
                company_description="",
                company_website="",
                industry="",
                location=""
            )

        db.session.add(profile)
        db.session.commit()

        return jsonify({
            "message": "User and profile registered successfully",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }), 201

    except Exception:
        db.session.rollback()
        current_app.logger.exception(
            "Registration and profile creation failed"
        )
        return jsonify({
            "error": "Registration failed. Please try again."
        }), 500
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    if not check_password_hash(
        user.password_hash,
        password
    ):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }), 200
@auth_bp.route("/student-test", methods=["GET"])
@role_required("STUDENT")
def student_test():
    return jsonify({
        "message": "Welcome Student! You have access to this endpoint."
    }), 200
@auth_bp.route("/employer-test", methods=["GET"])
@role_required("EMPLOYER")
def employer_test():
    return jsonify({
        "message": "Welcome Employer! You have access to this endpoint."
    }), 200