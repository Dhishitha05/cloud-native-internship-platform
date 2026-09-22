from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models import (
    Skill,
    StudentProfile,
    StudentSkill,
    Internship,
    InternshipSkill
)
from app.decorators import role_required


skills_bp = Blueprint("skills", __name__)


# ==================================================
# CREATE SKILL
# ==================================================

@skills_bp.route("/", methods=["POST"])
@role_required("STUDENT", "EMPLOYER", "ADMIN")
def create_skill():

    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({
            "error": "Skill name is required"
        }), 400

    existing_skill = Skill.query.filter_by(
        name=data["name"]
    ).first()

    if existing_skill:
        return jsonify({
            "error": "Skill already exists",
            "skill_id": existing_skill.id
        }), 409

    skill = Skill(
        name=data["name"],
        category=data.get("category")
    )

    db.session.add(skill)
    db.session.commit()

    return jsonify({
        "message": "Skill created successfully",
        "skill": {
            "id": skill.id,
            "name": skill.name,
            "category": skill.category
        }
    }), 201


# ==================================================
# GET ALL SKILLS
# ==================================================

@skills_bp.route("/", methods=["GET"])
@role_required("STUDENT", "EMPLOYER", "ADMIN")
def get_skills():

    skills = Skill.query.order_by(
        Skill.name.asc()
    ).all()

    return jsonify([
        {
            "id": skill.id,
            "name": skill.name,
            "category": skill.category
        }
        for skill in skills
    ]), 200
@skills_bp.route("/student", methods=["POST"])
@role_required("STUDENT")
def add_student_skill():

    user_id = int(get_jwt_identity())

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not student:
        return jsonify({
            "error": "Student profile not found"
        }), 404

    data = request.get_json()

    if not data or not data.get("skill_id"):
        return jsonify({
            "error": "skill_id is required"
        }), 400

    skill = Skill.query.get(data["skill_id"])

    if not skill:
        return jsonify({
            "error": "Skill not found"
        }), 404

    existing = StudentSkill.query.filter_by(
        student_id=student.id,
        skill_id=skill.id
    ).first()

    if existing:
        return jsonify({
            "error": "Student already has this skill"
        }), 409

    student_skill = StudentSkill(
        student_id=student.id,
        skill_id=skill.id,
        proficiency=data.get("proficiency"),
        years_experience=data.get("years_experience")
    )

    db.session.add(student_skill)
    db.session.commit()

    return jsonify({
        "message": "Skill added to student profile successfully",
        "skill": {
            "id": skill.id,
            "name": skill.name,
            "proficiency": student_skill.proficiency,
            "years_experience": student_skill.years_experience
        }
    }), 201
@skills_bp.route("/student", methods=["GET"])
@role_required("STUDENT")
def get_student_skills():

    user_id = int(get_jwt_identity())

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not student:
        return jsonify({
            "error": "Student profile not found"
        }), 404

    student_skills = StudentSkill.query.filter_by(
        student_id=student.id
    ).all()

    return jsonify([
        {
            "skill_id": item.skill_id,
            "name": item.skill.name,
            "category": item.skill.category,
            "proficiency": item.proficiency,
            "years_experience": item.years_experience
        }
        for item in student_skills
    ]), 200
@skills_bp.route("/internship/<int:internship_id>", methods=["POST"])
@role_required("EMPLOYER")
def add_internship_skill(internship_id):

    user_id = int(get_jwt_identity())

    internship = Internship.query.get(internship_id)

    if not internship:
        return jsonify({
            "error": "Internship not found"
        }), 404

    if internship.employer.user_id != user_id:
        return jsonify({
            "error": "You can only modify your own internships"
        }), 403

    data = request.get_json()

    if not data or not data.get("skill_id"):
        return jsonify({
            "error": "skill_id is required"
        }), 400

    skill = Skill.query.get(data["skill_id"])

    if not skill:
        return jsonify({
            "error": "Skill not found"
        }), 404

    skill_type = data.get(
        "skill_type",
        "REQUIRED"
    ).upper()

    if skill_type not in ["REQUIRED", "PREFERRED"]:
        return jsonify({
            "error": "skill_type must be REQUIRED or PREFERRED"
        }), 400

    existing = InternshipSkill.query.filter_by(
        internship_id=internship.id,
        skill_id=skill.id
    ).first()

    if existing:
        return jsonify({
            "error": "Skill already added to this internship"
        }), 409

    internship_skill = InternshipSkill(
        internship_id=internship.id,
        skill_id=skill.id,
        skill_type=skill_type,
        weight=data.get("weight", 1.0)
    )

    db.session.add(internship_skill)
    db.session.commit()

    return jsonify({
        "message": "Skill added to internship successfully",
        "skill": {
            "id": skill.id,
            "name": skill.name,
            "skill_type": internship_skill.skill_type,
            "weight": internship_skill.weight
        }
    }), 201
