import copy

import allure
import pytest

from data_structures import PAYLOAD_BLACK_LIST, STATUS_BLACK_LIST, BASE_PAYLOAD_CANDIDATE_HISTORIES, STATUS_FREE_CANDIDATE
from tests.schemas.candidate_scheme import FeedResponse, CandidateHistory

@allure.feature('Назначение черного списка')
def generate_payload_black_list(candidate_id):
    payload = {
        **copy.deepcopy(PAYLOAD_BLACK_LIST),
        'candidateId': candidate_id
    }
    return payload

def generate_payload_candidate_history(candidate_id, job_id, status):
    payload = {
        **copy.deepcopy(BASE_PAYLOAD_CANDIDATE_HISTORIES),
        "candidateId": candidate_id,
        "jobId": job_id,
        **status
    }
    return payload

@allure.story('Назначение черного списка при одной связи К-В')
@pytest.mark.parametrize('candidate_job_histories', [
    28913, 28840, {'statusId': 28807, 'ReasonId': 1304},
    28812, 28814, 28927, {'statusId': 28816, 'HireTermId': 1203},
    {'statusId': 28817, 'ReasonId': 1304}
], indirect=True)
def test_set_black_list_with_one_link(candidate_job_histories, candidate_api_auth):
    candidate_id, job_id, ch_id = candidate_job_histories
    with allure.step('Запрос, на получение связок К-В до назначения черного списка'):
        _, data_feed_before = candidate_api_auth.get_feed(candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_before = FeedResponse.model_validate(data_feed_before)
    with allure.step('Проверка, что связка К-В не закрыта'):
        assert valid_feed_before.activeCandidateHistories[0].candidateId == candidate_id
        assert valid_feed_before.activeCandidateHistories[0].jobId == job_id
        assert valid_feed_before.activeCandidateHistories[0].candidateHistoryId == ch_id
        assert valid_feed_before.activeCandidateHistories[0].closedAt is None

    with allure.step('Запрос на назначение черного списка'):
        response, data = candidate_api_auth.set_black_list(json=generate_payload_black_list(candidate_id))
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_black_list = CandidateHistory.model_validate(data)
    with allure.step('Проверка успешности назначения черного списка'):
        assert response.status_code == 200
        assert valid_black_list.candidateId == candidate_id
        assert valid_black_list.statusId == STATUS_BLACK_LIST

    with allure.step('Запрос, на получение связок К-В после назначения черного списка'):
        _, data_feed_after = candidate_api_auth.get_feed(candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_after = FeedResponse.model_validate(data_feed_after)
    with allure.step('Проверка, что связка К-В закрыта'):
        assert valid_feed_after.activeCandidateHistories[0].candidateId == candidate_id
        assert valid_feed_after.activeCandidateHistories[0].jobId == job_id
        assert valid_feed_after.activeCandidateHistories[0].candidateHistoryId == ch_id
        assert isinstance(valid_feed_after.activeCandidateHistories[0].closedAt, int)

    with allure.step('Проверка, что черный список появился в ленте'):
        assert valid_feed_after.candidateHistories[0].statusId == STATUS_BLACK_LIST

@allure.story('Назначение черного списка при двух связях К-В')
@pytest.mark.parametrize('candidate_job_histories, status', (
    (28913, {'statusId': 28807, 'ReasonId': 1304}),
    ({'statusId': 28816, 'HireTermId': 1203}, {'statusId':28792}),
    ({'statusId': 28817, 'ReasonId': 1304}, {'statusId': 28816, 'HireTermId': 1203})
), indirect=['candidate_job_histories'])
def test_set_black_list_with_two_link(candidate_job_histories, candidate_api_auth, new_job_db, status):
    candidate_id, job_id, ch_id = candidate_job_histories
    with allure.step('Создание еще одной связки К-В'):
        payload = generate_payload_candidate_history(candidate_id, new_job_db, status)
        resp_new_ch, new_ch = candidate_api_auth.create_candidate_histories(json=payload)
        new_ch_id = new_ch['candidateHistoryId']
    with allure.step('Проверка, успешности создания новой связки К-В'):
        assert resp_new_ch.status_code == 201

    with allure.step('Запрос, на получение связок К-В до назначения черного списка'):
        _, data_feed_before = candidate_api_auth.get_feed(candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_before = FeedResponse.model_validate(data_feed_before)
    with allure.step('Проверка, что первая связка К-В не закрыта'):
        assert valid_feed_before.activeCandidateHistories[0].closedAt is None
        assert valid_feed_before.activeCandidateHistories[0].jobId == new_job_db
        assert valid_feed_before.activeCandidateHistories[0].candidateHistoryId == new_ch_id
    with allure.step('Проверка, что вторая связка К-В не закрыта'):
        assert valid_feed_before.activeCandidateHistories[1].closedAt is None
        assert valid_feed_before.activeCandidateHistories[1].jobId == job_id
        assert valid_feed_before.activeCandidateHistories[1].candidateHistoryId == ch_id

    with allure.step('Запрос на назначение черного списка'):
        response, data = candidate_api_auth.set_black_list(json=generate_payload_black_list(candidate_id))
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_black_list = CandidateHistory.model_validate(data)
    with allure.step('Проверка успешности назначения черного списка'):
        assert response.status_code == 200
        assert valid_black_list.candidateId == candidate_id
        assert valid_black_list.statusId == STATUS_BLACK_LIST

    with allure.step('Запрос, на получение связок К-В после назначения черного списка'):
        _, data_feed_after = candidate_api_auth.get_feed(candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_after = FeedResponse.model_validate(data_feed_after)

    # Обе проверки имеют место быть, т.к. в каждом тесте идет создание новых сущностей,
    # у нас в тесте всегда будет только 2 вакансии. Данные проверки более стабильны
    with allure.step('Проверка, что первая связка К-В закрыта'):
        assert valid_feed_after.activeCandidateHistories[0].candidateHistoryId == new_ch_id
        assert valid_feed_after.activeCandidateHistories[0].jobId == new_job_db
        assert isinstance(valid_feed_after.activeCandidateHistories[0].closedAt, int)
    with allure.step('Проверка, что вторая связка К-В закрыта'):
        assert valid_feed_after.activeCandidateHistories[1].candidateHistoryId == ch_id
        assert valid_feed_after.activeCandidateHistories[1].jobId == job_id
        assert isinstance(valid_feed_after.activeCandidateHistories[1].closedAt, int)

    # Проверка, что все вакансии закрыты, но т.к. у нас всегда 2 вакансии
    # и новые не появятся сами собой - первый тест стабильнее, хоть и обращается к обьектам по статичным индексам
    # with allure.step('Проверка, что все связки К-В закрыты'):
    #     assert all(isinstance(ach.closedAt, int) for ach in valid_feed_after.activeCandidateHistories)

    with allure.step('Проверка, что черный список появился в ленте'):
        assert valid_feed_after.candidateHistories[0].statusId == STATUS_BLACK_LIST

@allure.story('Назначение черного списка при свободном кандидате')
def test_set_black_list_on_free_candidate(candidate_api_auth, free_candidate):
    with allure.step('Проверяем, что Свободный кандидат - последний статус'):
        _, data_feed_before = candidate_api_auth.get_feed(free_candidate)
        valid_feed_before = FeedResponse.model_validate(data_feed_before)
        assert valid_feed_before.candidateHistories[0].statusId == STATUS_FREE_CANDIDATE

    with allure.step('Запрос на назначение черного списка'):
        payload = generate_payload_black_list(free_candidate)
        response, data = candidate_api_auth.set_black_list(json=payload)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_black_list = CandidateHistory.model_validate(data)
    with allure.step('Проверка успешности назначения черного списка'):
        assert response.status_code == 200
        assert valid_black_list.candidateId == free_candidate
        assert valid_black_list.statusId == STATUS_BLACK_LIST

    with allure.step('Проверяем, что Черный список - последний статус'):
        _, data_feed_after= candidate_api_auth.get_feed(free_candidate)
        valid_feed_after = FeedResponse.model_validate(data_feed_after)
        assert valid_feed_after.candidateHistories[0].statusId == STATUS_BLACK_LIST
    with allure.step('Проверяем, что все связки К-В закрыты'):
        assert all(isinstance(ach.closedAt, int) for ach in valid_feed_after.activeCandidateHistories)

@allure.story('Назначение черного списка у нового кандидата без единой связи')
def test_black_list_on_new_candidate(candidate_api_auth, new_candidate_db):
    with allure.step('Запрос на назначение черного списка'):
        payload = generate_payload_black_list(new_candidate_db)
        response, data = candidate_api_auth.set_black_list(json=payload)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_black_list = CandidateHistory.model_validate(data)
    with allure.step('Проверка успешности назначения черного списка'):
        assert response.status_code == 200
        assert valid_black_list.candidateId == new_candidate_db
        assert valid_black_list.statusId == STATUS_BLACK_LIST
    with allure.step('Проверяем, что Черный список - последний статус'):
        _, data_feed_after= candidate_api_auth.get_feed(new_candidate_db)
        valid_feed_after = FeedResponse.model_validate(data_feed_after)
        assert valid_feed_after.candidateHistories[0].statusId == STATUS_BLACK_LIST
    with allure.step('Проверяем, что Черный список не появился в связках К-В'):
        assert len(valid_feed_after.activeCandidateHistories) == 0

@allure.story('Снятие черного списка назначением группы статусов')
@pytest.mark.parametrize('status', [
    {'statusId': 28926},
    {'statusId': 28807,'ReasonId': 1301},
    {'statusId': 28816,'HireTermId': 1203}
])
def test_delete_black_list_set_other_status(candidate_api_auth, black_list_candidate, new_job_db, status):
    with allure.step('Запрос, на получение связок К-В до снятия черного списка'):
        _, data_feed_before = candidate_api_auth.get_feed(black_list_candidate)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_before = FeedResponse.model_validate(data_feed_before)
    with allure.step('Проверка, что все связки К-В закрыты'):
        assert all(isinstance(ach.closedAt, int) for ach in valid_feed_before.activeCandidateHistories)
    with allure.step('Проверка, что черный список - последний статус'):
        assert valid_feed_before.candidateHistories[0].statusId == STATUS_BLACK_LIST

    with allure.step('Запрос, открытие новой группы статусов'):
        payload = generate_payload_candidate_history(black_list_candidate, new_job_db, status)
        resp_new_ch, data_new_ch = candidate_api_auth.create_candidate_histories(json=payload)
    with allure.step('Проверка, что новая группа успешно создана'):
        assert resp_new_ch.status_code == 201
        new_ch_id = data_new_ch['candidateHistoryId']

    with allure.step('Запрос, на получение связок К-В после снятия черного списка'):
        _, data_feed_after = candidate_api_auth.get_feed(black_list_candidate)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_after = FeedResponse.model_validate(data_feed_after)
    with allure.step('Проверка, что новая связка К-В открыта'):
        assert valid_feed_after.activeCandidateHistories[0].jobId == new_job_db
        assert valid_feed_after.activeCandidateHistories[0].candidateHistoryId == new_ch_id
        assert valid_feed_after.activeCandidateHistories[0].candidateStatusId == status['statusId']
    with allure.step('Проверка, что черный список не последний статус'):
        assert valid_feed_after.candidateHistories[0].statusId != STATUS_BLACK_LIST
