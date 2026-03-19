import copy
import pyodbc

import pytest
from dotenv import load_dotenv
import os
from data_structures import (BASE_PAYLOAD_CANDIDATE, BASE_PAYLOAD_VACANCY, BASE_PAYLOAD_CANDIDATE_HISTORIES,
                             DEFAULT_STATUS_ID, SQL_INSERT_CANDIDATE, SQL_INSERT_VACANCY,
                             SQL_INSERT_CANDIDATE_HISTORY)
from src.api.api_candidate import CandidateApi
from src.api.api_client import ClientApi
from src.api.api_settings import SettingsApi
from src.api.api_tests import TestApi
from src.api.api_vacancy import VacancyApi

@pytest.fixture
def api_client(request):
    load_dotenv()
    base_url = os.getenv("API_BASE_URL")
    return ClientApi(base_url, verify=False)

@pytest.fixture
def auth_api_client(api_client):
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    payload = {
        "username": login,
        "password": password
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
def candidate_job_histories(candidate_api_auth, vacancy_api_auth, db_connection, request):
    param = getattr(request, "param", DEFAULT_STATUS_ID)
    overrides = {"statusId": param} if isinstance(param, int) else dict(param)

    cursor = db_connection.cursor()

    # Создание нового кандидата через БД
    cursor.execute(SQL_INSERT_CANDIDATE)
    candidate_id = cursor.fetchone()[0]
    # Создание нового кандидата через API(Необходимо передать фикстуру candidate_api_auth)
    # _, c = candidate_api_auth.create_candidate(json=BASE_PAYLOAD_CANDIDATE)
    # candidate_id = c['candidateId']

    # Создание новой вакансии через БД
    cursor.execute(SQL_INSERT_VACANCY)
    job_id = cursor.fetchone()[0]
    # Создание новой вакансии через API(Необходимо передать фикстуру vacancy_api_auth)
    # _, v = vacancy_api_auth.create_vacancy(BASE_PAYLOAD_VACANCY)
    # job_id = v['jobId']

    # Открытие группы статусов для созданных кандидата и вакансии через БД
    cursor.execute(SQL_INSERT_CANDIDATE_HISTORY,
                   overrides['statusId'],
                   job_id,
                   candidate_id,
                   overrides.get('reasonId',None))
    ch_id = cursor.fetchone()[0]
    # Открытие группы статусов через api для созданных кандидата и вакансии
    # В payload необходимо передать созданные: candidateId, jobId, statusId(overrides)
    # payload ={
    #     **copy.deepcopy(BASE_PAYLOAD_CANDIDATE_HISTORIES),
    #     'candidateId': candidate_id,
    #     'jobId': job_id,
    #     **overrides
    # }
    # _, ch = candidate_api_auth.create_candidate_histories(json=payload)
    # candidate_history_id = ch['candidateHistoryId']
    yield candidate_id, job_id, ch_id

    # удаляем созданные сущности(нужно при создании через api)
    # candidate_api_auth.delete_candidate(candidate_id)
    # vacancy_api_auth.delete_vacancy(job_id)

@pytest.fixture
def new_job(vacancy_api_auth):
    _, v = vacancy_api_auth.create_vacancy(BASE_PAYLOAD_VACANCY)
    yield v['jobId']
    vacancy_api_auth.delete_vacancy(v['jobId'])

@pytest.fixture
def new_candidate(candidate_api_auth):
    _, c = candidate_api_auth.create_candidate(json=BASE_PAYLOAD_CANDIDATE)
    yield c['candidateId']
    candidate_api_auth.delete_candidate(c['candidateId'])

@pytest.fixture
def db_connection():
    load_dotenv()
    connection = pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server={os.getenv('DB_SERVER')},{os.getenv('DB_PORT')};"
        f"Database={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )
    connection.autocommit = False
    yield connection
    connection.rollback()
    connection.close()