from flask import Blueprint
from flask.json import jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignment_submitted_resources = Blueprint(
    'teacher_assignment_submitted_resources', __name__)


@teacher_assignment_submitted_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments submitted to this teacher"""
    students_assignments_to_teacher = Assignment.get_assignments_submitted_to_teacher(
        p.teacher_id)
    students_assignments_to_teacher_dump = AssignmentSchema().dump(
        students_assignments_to_teacher, many=True)
    return APIResponse.respond(data=students_assignments_to_teacher_dump)


@teacher_assignment_submitted_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.grade_assignment(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
