from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models import EmployerProfile
from app.decorators import role_required


employers_bp = Blueprint("employers", __name__)


@employers_bp.route("/profile", methods=["POST"])
@role_required("EMPLOYER")
def create_profile():
    user_id = int(get_jwt_identity())

    existing_profile = EmployerProfile.query.filter_by(
        user_id=user_id
    ).first()

    if existing_profile:
        return jsonify({
            "error": "Employer profile already exists"
        }), 409

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    company_name = data.get("company_name")

    if not company_name:
        return jsonify({
            "error": "company_name is required"
        }), 400

    profile = EmployerProfile(
        user_id=user_id,
        company_name=company_name,
        company_description=data.get("company_description"),
        company_website=data.get("company_website"),
        industry=data.get("industry"),
        location=data.get("location")
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({
        "message": "Employer profile created successfully",
        "profile": {
            "id": profile.id,
            "user_id": profile.user_id,
            "company_name": profile.company_name,
            "company_description": profile.company_description,
            "company_website": profile.company_website,
            "industry": profile.industry,
            "location": profile.location
        }
    }), 201


@employers_bp.route("/profile", methods=["GET"])
@role_required("EMPLOYER")
def get_profile():
    user_id = int(get_jwt_identity())

    profile = EmployerProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not profile:
        return jsonify({
            "message": "Employer profile not found"
        }), 404

    return jsonify({
        "id": profile.id,
        "user_id": profile.user_id,
        "company_name": profile.company_name,
        "company_description": profile.company_description,
        "company_website": profile.company_website,
        "industry": profile.industry,
        "location": profile.location
    }), 200


@employers_bp.route("/profile", methods=["PUT"])
@role_required("EMPLOYER")
def update_profile():
    user_id = int(get_jwt_identity())

    profile = EmployerProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not profile:
        return jsonify({
            "error": "Employer profile not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if "company_name" in data:
        profile.company_name = data["company_name"]

    if "company_description" in data:
        profile.company_description = data["company_description"]

    if "company_website" in data:
        profile.company_website = data["company_website"]

    if "industry" in data:
        profile.industry = data["industry"]

    if "location" in data:
        profile.location = data["location"]

    db.session.commit()

    return jsonify({
        "message": "Employer profile updated successfully"
    }), 200