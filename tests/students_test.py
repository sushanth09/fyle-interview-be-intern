from core.models.assignments import Assignment
from tests.conftest import client


def test_demo(client):
    response = client.get(
        '/'
    )
    assert response.status_code == 200

def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_post_assignment_update_student_1(client, h_student_1):
    content = 'ABCD TESTPOST Update'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 5,
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    assignment = Assignment.query.all()
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': len(assignment) - 1,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2

def test_demo_client(client):
    response = client.get(
        '/client'
    )
    assert response.status_code == 200


def test_get_assignments_student_3(client, h_student_3):
    """failure case: Unauthorized assertion"""
    response = client.get(
        '/student/assignments',
        headers=h_student_3
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2