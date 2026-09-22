from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models import (
    Application,
    StudentProfile,
    Internship,
    EmployerProfile
)
from app.decorators import role_required


applications_bp = Blueprint("applications", __name__)


# ==================================================
# STUDENT — APPLY FOR INTERNSHIP
# ==================================================

@applications_bp.route("/", methods=["POST"])
@role_required("STUDENT")
def apply_for_internship():

    user_id = int(get_jwt_identity())

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not student:
        return jsonify({
            "error": "Student profile not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    internship_id = data.get("internship_id")

    if not internship_id:
        return jsonify({
            "error": "internship_id is required"
        }), 400

    internship = Internship.query.get(internship_id)

    if not internship:
        return jsonify({
            "error": "Internship not found"
        }), 404

    if internship.status != "OPEN":
        return jsonify({
            "error": "This internship is not open for applications"
        }), 400

    existing_application = Application.query.filter_by(
        student_id=student.id,
        internship_id=internship.id
    ).first()

    if existing_application:
        return jsonify({
            "error": "You have already applied for this internship"
        }), 409

    application = Application(
        student_id=student.id,
        internship_id=internship.id,
        cover_letter=data.get("cover_letter"),
        resume_url=data.get("resume_url")
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({
        "message": "Application submitted successfully",
        "application": {
            "id": application.id,
            "student_id": application.student_id,
            "internship_id": application.internship_id,
            "status": application.status,
            "cover_letter": application.cover_letter,
            "resume_url": application.resume_url
        }
    }), 201


# ==================================================
# STUDENT — VIEW MY APPLICATIONS
# ==================================================

@applications_bp.route("/my", methods=["GET"])
@role_required("STUDENT")
def get_my_applications():

    user_id = int(get_jwt_identity())

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not student:
        return jsonify({
            "error": "Student profile not found"
        }), 404

    applications = Application.query.filter_by(
        student_id=student.id
    ).order_by(
        Application.applied_at.desc()
    ).all()

    result = []

    for application in applications:

        result.append({
            "id": application.id,
            "internship_id": application.internship_id,
            "internship_title": application.internship.title,
            "domain": application.internship.domain,
            "location": application.internship.location,
            "status": application.status,
            "cover_letter": application.cover_letter,
            "resume_url": application.resume_url,
            "applied_at": (
                application.applied_at.isoformat()
                if application.applied_at
                else None
            )
        })

    return jsonify(result), 200


# ==================================================
# EMPLOYER — VIEW APPLICATIONS
# ==================================================

@applications_bp.route(
    "/internship/<int:internship_id>",
    methods=["GET"]
)
@role_required("EMPLOYER")
def get_internship_applications(internship_id):

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
            "error": "You can only view applications for your own internships"
        }), 403

    applications = Application.query.filter_by(
        internship_id=internship.id
    ).order_by(
        Application.applied_at.desc()
    ).all()

    result = []

    for application in applications:

        student = application.student

        result.append({
            "application_id": application.id,
            "student_id": student.id,
            "status": application.status,
            "cover_letter": application.cover_letter,
            "resume_url": application.resume_url,
            "applied_at": (
                application.applied_at.isoformat()
                if application.applied_at
                else None
            )
        })

    return jsonify(result), 200


# ==================================================
# EMPLOYER — UPDATE APPLICATION STATUS
# ==================================================

@applications_bp.route(
    "/<int:application_id>/status",
    methods=["PUT"]
)
@role_required("EMPLOYER")
def update_application_status(application_id):

    user_id = int(get_jwt_identity())

    employer = EmployerProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not employer:
        return jsonify({
            "error": "Employer profile not found"
        }), 404

    application = Application.query.get(application_id)

    if not application:
        return jsonify({
            "error": "Application not found"
        }), 404

    internship = Internship.query.get(
        application.internship_id
    )

    if internship.employer_id != employer.id:
        return jsonify({
            "error": "You can only update applications for your own internships"
        }), 403

    data = request.get_json()

    if not data or not data.get("status"):
        return jsonify({
            "error": "status is required"
        }), 400

    allowed_statuses = [
        "APPLIED",
        "SHORTLISTED",
        "INTERVIEW",
        "OFFER",
        "REJECTED"
    ]

    new_status = data["status"].upper()

    if new_status not in allowed_statuses:
        return jsonify({
            "error": "Invalid application status"
        }), 400

    application.status = new_status

    db.session.commit()

    return jsonify({
        "message": "Application status updated successfully",
        "application_id": application.id,
        "status": application.status
    }), 200