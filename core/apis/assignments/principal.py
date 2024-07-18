from flask import Flask, request, jsonify
from core import db
from core.models.assignments import Assignment
from core.libs.auth import verify_principal_header

app = Flask(__name__)

@app.route('/principal/assignments', methods=['GET'])
def get_principal_assignments():
    principal_id = request.headers.get('X-Principal')
    if not verify_principal_header(principal_id):
        return jsonify({"error": "Unauthorized"}), 401

    # Query assignments submitted and graded
    assignments = Assignment.query.filter_by(state='SUBMITTED') \
                                  .filter(Assignment.grade != None) \
                                  .all()

    # Prepare response
    assignments_list = []
    for assignment in assignments:
        assignments_list.append({
            "id": assignment.id,
            "content": assignment.content,
            "created_at": assignment.created_at.isoformat(),
            "updated_at": assignment.updated_at.isoformat(),
            "state": assignment.state,
            "student_id": assignment.student_id,
            "teacher_id": assignment.teacher_id,
            "grade": assignment.grade
        })

    return jsonify({"data": assignments_list})


@app.route('/principal/teachers', methods=['GET'])
def get_principal_teachers():
    principal_id = request.headers.get('X-Principal')
    if not verify_principal_header(principal_id):
        return jsonify({"error": "Unauthorized"}), 401

    # Query teachers
    teachers = teacher.query.all()

    # Prepare response
    teachers_list = []
    for teacher in teachers:
        teachers_list.append({
            "id": teacher.id,
            "user_id": teacher.user_id,
            "created_at": teacher.created_at.isoformat(),
            "updated_at": teacher.updated_at.isoformat()
        })

    return jsonify({"data": teachers_list})

@app.route('/principal/assignments/grade', methods=['POST'])
def grade_assignment():
    principal_id = request.headers.get('X-Principal')
    if not verify_principal_header(principal_id):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    assignment_id = data.get('id')
    grade = data.get('grade')

    # Retrieve assignment from database
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"error": "Assignment not found"}), 404

    # Update assignment grade
    assignment.grade = grade
    assignment.state = 'GRADED'
    db.session.commit()

    # Prepare response
    response_data = {
        "id": assignment.id,
        "content": assignment.content,
        "created_at": assignment.created_at.isoformat(),
        "updated_at": assignment.updated_at.isoformat(),
        "state": assignment.state,
        "student_id": assignment.student_id,
        "teacher_id": assignment.teacher_id,
        "grade": assignment.grade
    }

    return jsonify({"data": response_data})


if __name__ == '__main__':
    app.run(debug=True)
