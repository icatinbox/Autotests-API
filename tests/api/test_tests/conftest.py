import copy
import random

import pytest

from data_structures import PAYLOAD_TEST_MANAGE, PAYLOAD_FULL_PERMISSIONS, PAYLOAD_TEST_GRADE, BASE_PAYLOAD_TEST, \
    PAYLOAD_BASE_ROLE, PAYLOAD_ROLE_ADMIN
from src.sql.sql_delete import sql_delete_by_id
from src.sql.sql_insert import sql_insert_test, sql_insert_test_file


@pytest.fixture
def remove_permission_test_manage(settings_api_auth):
    settings_api_auth.change_permission(json=PAYLOAD_TEST_MANAGE)
    yield settings_api_auth
    settings_api_auth.change_permission(json=PAYLOAD_FULL_PERMISSIONS)

@pytest.fixture
def remove_permission_test_grade(settings_api_auth):
    settings_api_auth.change_permission(json=PAYLOAD_TEST_GRADE)
    yield settings_api_auth
    settings_api_auth.change_permission(json=PAYLOAD_FULL_PERMISSIONS)

@pytest.fixture
def permission_full_admin(settings_api_auth):
    settings_api_auth.change_role(json=PAYLOAD_ROLE_ADMIN)
    yield settings_api_auth
    settings_api_auth.change_role(json=PAYLOAD_BASE_ROLE)

@pytest.fixture
def grade(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('select Id, Label from lookup.TestAssignmentGrade')
    grade_id, grade_name = random.choice(cursor.fetchall())
    return grade_id, grade_name

@pytest.fixture
def test(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('select Id, Label from lookup.TestAssignmentDefinitions')
    test_id, test_name = random.choice(cursor.fetchall())
    return test_id, test_name

# Создание теста через БД
@pytest.fixture
def new_test_id_db(db_connection, candidate_job_histories, test):
    cursor = db_connection.cursor()
    candidate_id, job_id, ch_id = candidate_job_histories
    test_id, _ = test
    test_assignment_id = sql_insert_test(cursor, candidate_id, job_id, test_id, ch_id)
    file_id = sql_insert_test_file(cursor, test_assignment_id)
    db_connection.commit()

    yield test_assignment_id
    # Удаление созданных сущностей
    sql_delete_by_id(cursor, 'Files', file_id)
    sql_delete_by_id(cursor, 'CandidateTestAssignments', test_assignment_id)
    db_connection.commit()

# Создание теста через API
@pytest.fixture
def new_test_id(test_api_auth, candidate_job_histories, test, db_connection, request):
    is_delete = getattr(request, "param", True)
    candidate_id, job_id, ch_id = candidate_job_histories
    test_id, _ = test

    payload ={
        **copy.deepcopy(BASE_PAYLOAD_TEST),
        "jobId": job_id,
        "candidateId": candidate_id,
        "testHistoryId": ch_id,
        "testId": test_id
    }
    _, data = test_api_auth.attach_test(json=payload)
    new_test_id = data['testAssignmentId']

    yield new_test_id

    # Удаляем созданный тест, если is_delete = True(т.к. тест можно удалить не всегда)
    if is_delete:
        test_api_auth.delete_test(new_test_id)