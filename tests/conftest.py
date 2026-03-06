import copy
import random

import pytest

from data import PAYLOAD_TEST_GRADE, PAYLOAD_TEST_MANAGE, PAYLOAD_FULL_PERMISSIONS, BASE_PAYLOAD_CANDIDATE, \
    BASE_PAYLOAD_VACANCY, BASE_PAYLOAD_CANDIDATE_HISTORIES, DEFAULT_STATUS_ID, BASE_PAYLOAD_TEST, PAYLOAD_ROLE_ADMIN, \
    PAYLOAD_BASE_ROLE, STATUS_FREE_CANDIDATE, PAYLOAD_BLACK_LIST, LOGIN, PASSWORD, BASEURL
from src.api.api_candidate import CandidateApi
from src.api.api_client import ClientApi
from src.api.api_settings import SettingsApi
from src.api.api_tests import TestApi
from src.api.api_vacancy import VacancyApi

def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action = "store",
        default = BASEURL,
        help = "base url"
    )

@pytest.fixture
def api_client(request):
    base_url = request.config.getoption("--url")
    return ClientApi(base_url, verify=False)

@pytest.fixture
def auth_api_client(api_client):
    payload = {
        "username": LOGIN,
        "password": PASSWORD
    }
    api_client.request_auth(payload=payload)
    return api_client

@pytest.fixture
def settings_api_auth(auth_api_client):
    return SettingsApi(auth_api_client)

@pytest.fixture
def test_api_auth(auth_api_client):
    return TestApi(auth_api_client)

@pytest.fixture
def candidate_api_auth(auth_api_client):
    return CandidateApi(auth_api_client)

@pytest.fixture
def vacancy_api_auth(auth_api_client):
    return VacancyApi(auth_api_client)

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
def candidate_job_histories(candidate_api_auth, vacancy_api_auth, request):
    param = getattr(request, "param", DEFAULT_STATUS_ID)
    overrides = {"statusId": param} if isinstance(param, int) else dict(param)

    # Создание нового кандидата
    _, c = candidate_api_auth.create_candidate(json=BASE_PAYLOAD_CANDIDATE)
    candidate_id = c['candidateId']

    # Создание новой вакансии
    _, v = vacancy_api_auth.create_vacancy(BASE_PAYLOAD_VACANCY)
    job_id = v['jobId']

    # Открытие для созданных кандидата и вакансии группы
    # В payload необходимо передать созданные: candidateId, jobId, statusId(overrides)
    payload ={
        **copy.deepcopy(BASE_PAYLOAD_CANDIDATE_HISTORIES),
        'candidateId': candidate_id,
        'jobId': job_id,
        **overrides
    }
    _, ch = candidate_api_auth.create_candidate_histories(json=payload)
    candidate_history_id = ch['candidateHistoryId']
    yield candidate_id, job_id, candidate_history_id

    # удаляем созданные сущности
    candidate_api_auth.delete_candidate(candidate_id)
    vacancy_api_auth.delete_vacancy(job_id)

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

@pytest.fixture
def grade(test_api_auth):
    _, data = test_api_auth.get_grades()
    random_grade = random.choice(data)
    return random_grade['gradeId'], random_grade['name']

@pytest.fixture
def permission_full_admin(settings_api_auth):
    settings_api_auth.change_role(json=PAYLOAD_ROLE_ADMIN)
    yield settings_api_auth
    settings_api_auth.change_role(json=PAYLOAD_BASE_ROLE)

@pytest.fixture
def new_job(vacancy_api_auth):
    _, v = vacancy_api_auth.create_vacancy(BASE_PAYLOAD_VACANCY)
    yield v['jobId']
    vacancy_api_auth.delete_vacancy(v['jobId'])

@pytest.fixture
def free_candidate(candidate_api_auth, candidate_job_histories):
    candidate_id, job_id, candidate_history_id = candidate_job_histories
    payload = {
        **copy.deepcopy(BASE_PAYLOAD_CANDIDATE_HISTORIES),
        'jobId': job_id,
        "candidateId": candidate_id,
        "accountId": 22014,
        "statusId": STATUS_FREE_CANDIDATE,
    }
    _, data = candidate_api_auth.set_free_candidate(json=payload)
    return candidate_id

@pytest.fixture
def new_candidate(candidate_api_auth):
    _, c = candidate_api_auth.create_candidate(json=BASE_PAYLOAD_CANDIDATE)
    yield c['candidateId']
    candidate_api_auth.delete_candidate(c['candidateId'])

@pytest.fixture
def black_list_candidate(candidate_api_auth, candidate_job_histories):
    candidate_id, job_id, candidate_history_id = candidate_job_histories
    payload = {
        **copy.deepcopy(PAYLOAD_BLACK_LIST),
        'candidateId': candidate_id
    }
    _, data = candidate_api_auth.set_black_list(json=payload)
    return candidate_id
