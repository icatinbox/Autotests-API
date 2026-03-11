import copy
import random

import pytest

from data_structures import PAYLOAD_TEST_MANAGE, PAYLOAD_FULL_PERMISSIONS, PAYLOAD_TEST_GRADE, BASE_PAYLOAD_TEST, \
    PAYLOAD_BASE_ROLE, PAYLOAD_ROLE_ADMIN


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
def grade(test_api_auth):
    _, data = test_api_auth.get_grades()
    random_grade = random.choice(data)
    return random_grade['gradeId'], random_grade['name']

@pytest.fixture
def test(test_api_auth):
    _, data = test_api_auth.get_all_directory_tests()
    random_test = random.choice(data)
    return random_test['testId'], random_test['name']

@pytest.fixture
def new_test_id(test_api_auth, candidate_job_histories, test, request):
    is_delete = getattr(request, "param", True)
    candidate_id, job_id, candidate_history_id = candidate_job_histories
    test_id, _ = test
    payload ={
        **copy.deepcopy(BASE_PAYLOAD_TEST),
        "jobId": job_id,
        "candidateId": candidate_id,
        "testHistoryId": candidate_history_id,
        "testId": test_id
    }
    _, data = test_api_auth.attach_test(json=payload)
    new_test_id = data['testAssignmentId']
    yield new_test_id

    # Удаляем созданный тест, если is_delete = True(т.к. тест можно удалить не всегда)
    if is_delete:
        test_api_auth.delete_test(new_test_id)