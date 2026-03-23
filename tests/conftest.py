import copy
import pyodbc

import pytest
from dotenv import load_dotenv
import os
from data_structures import (BASE_PAYLOAD_CANDIDATE, BASE_PAYLOAD_VACANCY, BASE_PAYLOAD_CANDIDATE_HISTORIES,
                             DEFAULT_STATUS_ID)
from src.sql.sql_delete import sql_delete_by_id, sql_clean_full_history_by_job_id, sql_clean_full_history_by_candidate_id
from src.sql.sql_insert import (SQL_INSERT_CANDIDATE, sql_insert_candidate_history,
                                sql_insert_active_candidate_status, sql_insert_vacancy)
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

# Создание новой свзяки(candidate history) через БД
@pytest.fixture
def candidate_job_histories_db(db_connection, request):
    param = getattr(request, "param", DEFAULT_STATUS_ID)
    overrides = {"statusId": param} if isinstance(param, int) else dict(param)

    # Создание нового кандидата
    cursor = db_connection.cursor()
    cursor.execute(SQL_INSERT_CANDIDATE)
    candidate_id = cursor.fetchone()[0]

    # Создание новой вакансии
    job_id = sql_insert_vacancy(cursor)

    # Открытие группы статусов для созданных кандидата и вакансии
    ch_id = sql_insert_candidate_history(
        cursor,
        overrides['statusId'],
        job_id,
        candidate_id,
        overrides.get('reasonId', None)
    )
    acs_id = sql_insert_active_candidate_status(
        cursor,
        overrides['statusId'],
        job_id,
        candidate_id,
        ch_id
    )
    # Сохранение данных в БД
    db_connection.commit()

    yield candidate_id, job_id, ch_id

    # Удаляем созданные сущности из БД
    sql_delete_by_id(cursor, 'ActiveCandidateStatus', acs_id)
    sql_delete_by_id(cursor, 'CandidateHistories', ch_id)
    sql_delete_by_id(cursor, 'Candidates', candidate_id)
    sql_delete_by_id(cursor, 'Jobs', job_id)
    db_connection.commit()

# Создание новой свзяки(candidate history) через API
@pytest.fixture
def candidate_job_histories(candidate_api_auth, vacancy_api_auth, db_connection, request):
    param = getattr(request, "param", DEFAULT_STATUS_ID)
    overrides = {"statusId": param} if isinstance(param, int) else dict(param)

    # Создание нового кандидата
    _, c = candidate_api_auth.create_candidate(json=BASE_PAYLOAD_CANDIDATE)
    candidate_id = c['candidateId']

    # Создание новой вакансии
    _, v = vacancy_api_auth.create_vacancy(BASE_PAYLOAD_VACANCY)
    job_id = v['jobId']

    # Открытие группы статусов для созданных кандидата и вакансии
    # В payload необходимо передать созданные: candidateId, jobId, statusId(overrides)
    payload ={
        **copy.deepcopy(BASE_PAYLOAD_CANDIDATE_HISTORIES),
        'candidateId': candidate_id,
        'jobId': job_id,
        **overrides
    }
    _, ch = candidate_api_auth.create_candidate_histories(json=payload)
    ch_id = ch['candidateHistoryId']
    yield candidate_id, job_id, ch_id
    cursor = db_connection.cursor()
    sql_clean_full_history_by_job_id(cursor, job_id)
    sql_clean_full_history_by_candidate_id(cursor, candidate_id)
    db_connection.commit()

# Создание новой вакансии через БД
@pytest.fixture
def new_job_db(db_connection):
    cursor = db_connection.cursor()
    job_id = sql_insert_vacancy(cursor)
    db_connection.commit()
    yield job_id
    sql_clean_full_history_by_job_id(cursor, job_id)
    db_connection.commit()

# Создание новой вакансии через API
@pytest.fixture
def new_job(vacancy_api_auth):
    _, v = vacancy_api_auth.create_vacancy(BASE_PAYLOAD_VACANCY)
    yield v['jobId']
    vacancy_api_auth.delete_vacancy(v['jobId'])

# Создание нового кандидата через БД
@pytest.fixture
def new_candidate_db(db_connection):
    cursor = db_connection.cursor()
    cursor.execute(SQL_INSERT_CANDIDATE)
    candidate_id = cursor.fetchone()[0]
    db_connection.commit()
    yield candidate_id
    sql_clean_full_history_by_candidate_id(cursor, candidate_id)
    db_connection.commit()

# Создание нового кандидата через API
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
    yield connection
    connection.commit()
    connection.close()