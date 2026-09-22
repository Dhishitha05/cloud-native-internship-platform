from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models import Internship, EmployerProfile
from app.decorators import role_required


internships_bp = Blueprint("internships", __name__)


# --------------------------------------------------
# CREATE INTERNSHIP
# --------------------------------------------------

@internships_bp.route("/", methods=["POST"])
@role_required("EMPLOYER")
def create_internship():

    user_id = int(get_jwt_identity())

    employer = EmployerProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not employer:
        return jsonify({
            "error": "Employer profile not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    required_fields = [
        "title",
        "description",
        "domain"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "error": f"{field} is required"
            }), 400

    deadline = None

    if data.get("application_deadline"):
        try:
            deadline = datetime.fromisoformat(
                data["application_deadline"]
            )
        except ValueError:
            return jsonify({
                "error": "Invalid application_deadline format"
            }), 400

    internship = Internship(
        employer_id=employer.id,
        title=data["title"],
        description=data["description"],
        domain=data["domain"],
        location=data.get("location"),
        duration_months=data.get("duration_months"),
        stipend=data.get("stipend"),
        eligibility=data.get("eligibility"),
        application_deadline=deadline
    )

    db.session.add(internship)
    db.session.commit()

    return jsonify({
        "message": "Internship created successfully",
        "internship": {
            "id": internship.id,
            "title": internship.title,
            "description": internship.description,
            "domain": internship.domain,
            "location": internship.location,
            "duration_months": internship.duration_months,
            "stipend": internship.stipend,
            "eligibility": internship.eligibility,
            "application_deadline": (
                internship.application_deadline.isoformat()
                if internship.application_deadline
                else None
            ),
            "status": internship.status
        }
    }), 201


# --------------------------------------------------
# GET ALL OPEN INTERNSHIPS
# --------------------------------------------------

@internships_bp.route("/", methods=["GET"])
@role_required("STUDENT", "EMPLOYER", "ADMIN")
def get_internships():

    internships = Internship.query.filter_by(
        status="OPEN"
    ).order_by(
        Internship.created_at.desc()
    ).all()

    result = []

    for internship in internships:
        result.append({
            "id": internship.id,
            "employer_id": internship.employer_id,
            "title": internship.title,
            "description": internship.description,
            "domain": internship.domain,
            "location": internship.location,
            "duration_months": internship.duration_months,
            "stipend": internship.stipend,
            "eligibility": internship.eligibility,
            "application_deadline": (
                internship.application_deadline.isoformat()
                if internship.application_deadline
                else None
            ),
            "status": internship.status
        })

    return jsonify(result), 200


# --------------------------------------------------
# GET SINGLE INTERNSHIP
# --------------------------------------------------

@internships_bp.route("/<int:internship_id>", methods=["GET"])
@role_required("STUDENT", "EMPLOYER", "ADMIN")
def get_internship(internship_id):

    internship = Internship.query.get(internship_id)

    if not internship:
        return jsonify({
            "error": "Internship not found"
        }), 404

    return jsonify({
        "id": internship.id,
        "employer_id": internship.employer_id,
        "title": internship.title,
        "description": internship.description,
        "domain": internship.domain,
        "location": internship.location,
        "duration_months": internship.duration_months,
        "stipend": internship.stipend,
        "eligibility": internship.eligibility,
        "application_deadline": (
            internship.application_deadline.isoformat()
            if internship.application_deadline
            else None
        ),
        "status": internship.status
    }), 200


# --------------------------------------------------
# UPDATE INTERNSHIP
# --------------------------------------------------

@internships_bp.route("/<int:internship_id>", methods=["PUT"])
@role_required("EMPLOYER")
def update_internship(internship_id):

    user_id = int(get_jwt_identity())

    employer = EmployerProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not employer:
        return jsonify({
            "error": "Employer profile not found"
        }), 404

    internship = Internship.query.get(internship_id)

    if not internship:
        return jsonify({
            "error": "Internship not found"
        }), 404

    if internship.employer_id != employer.id:
        return jsonify({
            "error": "You can only update your own internships"
        }), 403

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if "title" in data:
        internship.title = data["title"]

    if "description" in data:
        internship.description = data["description"]

    if "domain" in data:
        internship.domain = data["domain"]

    if "location" in data:
        internship.location = data["location"]

    if "duration_months" in data:
        internship.duration_months = data["duration_months"]

    if "stipend" in data:
        internship.stipend = data["stipend"]

    if "eligibility" in data:
        internship.eligibility = data["eligibility"]

    if "status" in data:
        internship.status = data["status"]

    if "application_deadline" in data:

        if data["application_deadline"]:
            try:
                internship.application_deadline = datetime.fromisoformat(
                    data["application_deadline"]
                )
            except ValueError:
                return jsonify({
                    "error": "Invalid application_deadline format"
                }), 400
        else:
            internship.application_deadline = None

    db.session.commit()

    return jsonify({
        "message": "Internship updated successfully"
    }), 200


# --------------------------------------------------
# DELETE INTERNSHIP
# --------------------------------------------------

@internships_bp.route("/<int:internship_id>", methods=["DELETE"])
@role_required("EMPLOYER")
def delete_internship(internship_id):

    user_id = int(get_jwt_identity())

    employer = EmployerProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not employer:
        return jsonify({
            "error": "Employer profile not found"
        }), 404

    internship = Internship.query.get(internship_id)

    if not internship:
        return jsonify({
            "error": "Internship not found"
        }), 404

    if internship.employer_id != employer.id:
        return jsonify({
            "error": "You can only delete your own internships"
        }), 403

    db.session.delete(internship)
    db.session.commit()

    return jsonify({
        "message": "Internship deleted successfully"
    }), 200