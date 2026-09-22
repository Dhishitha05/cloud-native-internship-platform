import json

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models import (
    StudentProfile,
    Internship,
    StudentSkill,
    InternshipSkill,
    MatchScore
)
from app.decorators import role_required


matching_bp = Blueprint("matching", __name__)


@matching_bp.route(
    "/internship/<int:internship_id>",
    methods=["GET"]
)
@role_required("STUDENT")
def calculate_match(internship_id):

    user_id = int(get_jwt_identity())

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not student:
        return jsonify({
            "error": "Student profile not found"
        }), 404

    internship = Internship.query.get(internship_id)

    if not internship:
        return jsonify({
            "error": "Internship not found"
        }), 404

    student_skills = StudentSkill.query.filter_by(
        student_id=student.id
    ).all()

    internship_skills = InternshipSkill.query.filter_by(
        internship_id=internship.id
    ).all()

    student_skill_ids = {
        item.skill_id
        for item in student_skills
    }

    if not internship_skills:
        return jsonify({
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "message": "No skills defined for this internship"
        }), 200

    total_weight = 0
    matched_weight = 0

    matched_skills = []
    missing_skills = []

    for internship_skill in internship_skills:

        weight = internship_skill.weight or 1.0

        if internship_skill.skill_type == "PREFERRED":
            weight *= 0.5

        total_weight += weight

        skill_name = internship_skill.skill.name

        if internship_skill.skill_id in student_skill_ids:

            matched_weight += weight

            matched_skills.append(skill_name)

        else:

            missing_skills.append(skill_name)

    score = (
        matched_weight / total_weight * 100
        if total_weight > 0
        else 0
    )

    score = round(score, 2)

    existing_score = MatchScore.query.filter_by(
        student_id=student.id,
        internship_id=internship.id
    ).first()

    if existing_score:

        existing_score.score = score
        existing_score.matched_skills = json.dumps(
            matched_skills
        )
        existing_score.missing_skills = json.dumps(
            missing_skills
        )

    else:

        existing_score = MatchScore(
            student_id=student.id,
            internship_id=internship.id,
            score=score,
            matched_skills=json.dumps(
                matched_skills
            ),
            missing_skills=json.dumps(
                missing_skills
            )
        )

        db.session.add(existing_score)

    db.session.commit()

    return jsonify({
        "internship_id": internship.id,
        "student_id": student.id,
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }), 200