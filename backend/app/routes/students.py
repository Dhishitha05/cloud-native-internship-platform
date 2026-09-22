from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models import StudentProfile
from app.decorators import role_required


students_bp = Blueprint("students", __name__)


@students_bp.route("/profile", methods=["GET"])
@role_required("STUDENT")
def get_profile():
    user_id = int(get_jwt_identity())

    profile = StudentProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not profile:
        return jsonify({
            "message": "Student profile not found"
        }), 404

    return jsonify({
        "id": profile.id,
        "user_id": profile.user_id,
        "college": profile.college,
        "degree": profile.degree,
        "branch": profile.branch,
        "graduation_year": profile.graduation_year,
        "bio": profile.bio,
        "resume_url": profile.resume_url,
        "interests": profile.interests,
        "preferred_domain": profile.preferred_domain
    }), 200
@students_bp.route("/profile", methods=["POST"])
@role_required("STUDENT")
def create_profile():
    user_id = int(get_jwt_identity())

    existing_profile = StudentProfile.query.filter_by(
        user_id=user_id
    ).first()

    if existing_profile:
        return jsonify({
            "error": "Student profile already exists"
        }), 409

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    profile = StudentProfile(
        user_id=user_id,
        college=data.get("college"),
        degree=data.get("degree"),
        branch=data.get("branch"),
        graduation_year=data.get("graduation_year"),
        bio=data.get("bio"),
        resume_url=data.get("resume_url"),
        interests=data.get("interests"),
        preferred_domain=data.get("preferred_domain")
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({
        "message": "Student profile created successfully",
        "profile": {
            "id": profile.id,
            "user_id": profile.user_id,
            "college": profile.college,
            "degree": profile.degree,
            "branch": profile.branch,
            "graduation_year": profile.graduation_year,
            "bio": profile.bio,
            "resume_url": profile.resume_url,
            "interests": profile.interests,
            "preferred_domain": profile.preferred_domain
        }
    }), 201
@students_bp.route("/profile", methods=["PUT"])
@role_required("STUDENT")
def update_profile():
    user_id = int(get_jwt_identity())

    profile = StudentProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not profile:
        return jsonify({
            "error": "Student profile not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if "college" in data:
        profile.college = data["college"]

    if "degree" in data:
        profile.degree = data["degree"]

    if "branch" in data:
        profile.branch = data["branch"]

    if "graduation_year" in data:
        profile.graduation_year = data["graduation_year"]

    if "bio" in data:
        profile.bio = data["bio"]

    if "resume_url" in data:
        profile.resume_url = data["resume_url"]

    if "interests" in data:
        profile.interests = data["interests"]

    if "preferred_domain" in data:
        profile.preferred_domain = data["preferred_domain"]

    db.session.commit()

    return jsonify({
        "message": "Student profile updated successfully"
    }), 200