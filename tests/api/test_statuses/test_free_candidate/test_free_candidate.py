import copy
import allure
import pytest

from data_structures import BASE_PAYLOAD_CANDIDATE_HISTORIES, STATUS_FREE_CANDIDATE, STATUS_BLACK_LIST
from tests.schemas.candidate_scheme import FeedResponse, CandidateHistory

@allure.feature('Назначение свободного кандидата')

def generate_payload_free_candidate(job_id, candidate_id):
    payload = {
        **copy.deepcopy(BASE_PAYLOAD_CANDIDATE_HISTORIES),
        'jobId': job_id,
        "candidateId": candidate_id,
        "accountId": 22014,
        "statusId": STATUS_FREE_CANDIDATE,
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

@allure.story('Назначение свободного кандидата с одной активной связкой и не финальной группой')
@pytest.mark.parametrize('candidate_job_histories', [28797, 28806, {'statusId': 28813, 'ReasonId': 1304}], indirect=True)
def test_set_free_candidate_with_one_link_not_final(candidate_api_auth, candidate_job_histories):
    candidate_id, job_id, ch_id = candidate_job_histories
    with allure.step('Запрос, на получение связок К-В до назначения свободного кандидата'):
        _, data_feed_before = candidate_api_auth.get_feed(candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_before = FeedResponse.model_validate(data_feed_before)
    with allure.step('Проверка, что связка К-В не закрыта'):
        assert valid_feed_before.activeCandidateHistories[0].candidateId == candidate_id
        assert valid_feed_before.activeCandidateHistories[0].jobId == job_id
        assert valid_feed_before.activeCandidateHistories[0].candidateHistoryId == ch_id
        assert valid_feed_before.activeCandidateHistories[0].closedAt is None

    with allure.step('Запрос на назначение свободного кандидата'):
        payload = generate_payload_free_candidate(job_id, candidate_id)
        resp, data = candidate_api_auth.set_free_candidate(json=payload)
    with allure.step('Проверка, что свободный кандидат назначился успешно'):
        assert resp.status_code == 200
        CandidateHistory.model_validate(data)

    with allure.step('Запрос, на получение связок К-В после назначения свободного кандидата'):
        _, data_feed_after = candidate_api_auth.get_feed(candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_after = FeedResponse.model_validate(data_feed_after)
    with allure.step('Проверка, что связка К-В закрыта'):
        assert valid_feed_after.activeCandidateHistories[0].candidateId == candidate_id
        assert valid_feed_after.activeCandidateHistories[0].jobId == job_id
        assert valid_feed_after.activeCandidateHistories[0].candidateHistoryId == ch_id
        assert isinstance(valid_feed_after.activeCandidateHistories[0].closedAt, int)

    with allure.step('Проверка, что свободный кандидат - последний статус'):
        assert valid_feed_after.candidateHistories[0].statusId == STATUS_FREE_CANDIDATE

@allure.story('Назначение свободного кандидата с одной активной связкой и финальной группой')
@pytest.mark.parametrize('candidate_job_histories', [
    28814,
    {'statusId': 28817, 'ReasonId': 1304},
    28927
], indirect=True)
def test_set_free_candidate_with_one_link_is_final(candidate_api_auth, candidate_job_histories):
    candidate_id, job_id, ch_id = candidate_job_histories
    with allure.step('Запрос, на получение связок К-В до назначения свободного кандидата'):
        _, data_feed_before = candidate_api_auth.get_feed(candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_before = FeedResponse.model_validate(data_feed_before)
    with allure.step('Проверка, что связка К-В открыта'):
        assert valid_feed_before.activeCandidateHistories[0].candidateId == candidate_id
        assert valid_feed_before.activeCandidateHistories[0].jobId == job_id
        assert valid_feed_before.activeCandidateHistories[0].candidateHistoryId == ch_id
        assert valid_feed_before.activeCandidateHistories[0].closedAt is None

    with allure.step('Запрос на назначение свободного кандидата'):
        payload = generate_payload_free_candidate(job_id, candidate_id)
        resp, data = candidate_api_auth.set_free_candidate(json=payload, is_raise= False)
    with allure.step('Проверка, что свободный кандидат не назначился'):
        assert resp.status_code == 400
        assert 'message' in data
        assert data['message'].lower() == 'нельзя прекратить активность по данной вакансии, кандидат находится на финальном статусе.'

    with allure.step('Запрос, на получение связок К-В после назначения свободного кандидата'):
        _, data_feed_after = candidate_api_auth.get_feed(candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_after = FeedResponse.model_validate(data_feed_after)
    with allure.step('Проверка, что связка К-В не закрылась'):
        assert valid_feed_after.activeCandidateHistories[0].candidateId == candidate_id
        assert valid_feed_after.activeCandidateHistories[0].jobId == job_id
        assert valid_feed_after.activeCandidateHistories[0].candidateHistoryId == ch_id
        assert valid_feed_after.activeCandidateHistories[0].closedAt is None

    with allure.step('Проверка, что свободный кандидат - не назначился'):
        assert valid_feed_after.candidateHistories[0].statusId != STATUS_FREE_CANDIDATE

@allure.story('Назначение свободного кандидата с двумя активными связками и не финальной группой')
@pytest.mark.parametrize('candidate_job_histories, status',[
    (28778, {'statusId': 28788}),
    (28809, {'statusId': 28913}),
    ({'statusId': 28810, 'ReasonId': 1304}, {'statusId': 28813, 'ReasonId': 1304}),
], indirect=['candidate_job_histories'])
def test_set_free_candidate_with_two_link_not_final(candidate_api_auth, new_job, candidate_job_histories, status):
    candidate_id, job_id, ch_id = candidate_job_histories
    with allure.step('Запрос, на создание еще одной связки К-В'):
        payload = generate_payload_candidate_history(candidate_id, new_job, status)
        resp_new_ch, data_new_ch = candidate_api_auth.create_candidate_histories(json=payload)
    with allure.step('Проверка, что новая связь создана успешно'):
        assert resp_new_ch.status_code == 201

    new_ch_id = data_new_ch['candidateHistoryId']

    with allure.step('Запрос, на получение связок К-В до назначения свободного кандидата'):
        _, data_feed_before = candidate_api_auth.get_feed(candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_before = FeedResponse.model_validate(data_feed_before)
    with allure.step('Проверка, что новая связка К-В не закрыта'):
        assert valid_feed_before.activeCandidateHistories[0].candidateId == candidate_id
        assert valid_feed_before.activeCandidateHistories[0].jobId == new_job
        assert valid_feed_before.activeCandidateHistories[0].candidateHistoryId == new_ch_id
        assert valid_feed_before.activeCandidateHistories[0].closedAt is None
    with allure.step('Проверка, что старая связка К-В не закрыта'):
        assert valid_feed_before.activeCandidateHistories[1].candidateId == candidate_id
        assert valid_feed_before.activeCandidateHistories[1].jobId == job_id
        assert valid_feed_before.activeCandidateHistories[1].candidateHistoryId == ch_id
        assert valid_feed_before.activeCandidateHistories[1].closedAt is None

    with allure.step('Запрос на назначение свободного кандидата по первой вакансии'):
        payload = generate_payload_free_candidate(job_id, candidate_id)
        resp, _ = candidate_api_auth.set_free_candidate(json=payload)
    with allure.step('Проверка, что свободный кандидат назначился успешно'):
        assert resp.status_code == 200

    with allure.step('Запрос, на получение связок К-В после назначения свободного кандидата'):
        _, data_feed_after = candidate_api_auth.get_feed(candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_after = FeedResponse.model_validate(data_feed_after)
    with allure.step('Проверка, что новая связка К-В осталась открыта'):
        assert valid_feed_after.activeCandidateHistories[0].candidateId == candidate_id
        assert valid_feed_after.activeCandidateHistories[0].jobId == new_job
        assert valid_feed_after.activeCandidateHistories[0].candidateHistoryId == new_ch_id
        assert valid_feed_after.activeCandidateHistories[0].closedAt is None
    with allure.step('Проверка, что старая связка К-В закрылась'):
        assert valid_feed_after.activeCandidateHistories[1].candidateId == candidate_id
        assert valid_feed_after.activeCandidateHistories[1].jobId == job_id
        assert valid_feed_after.activeCandidateHistories[1].candidateHistoryId == ch_id
        assert isinstance(valid_feed_after.activeCandidateHistories[1].closedAt, int)

    with allure.step('Проверка, что свободный кандидат - не назначился'):
        assert valid_feed_after.candidateHistories[0].statusId != STATUS_FREE_CANDIDATE

@allure.story('Назначение свободного кандидата с двумя активными связками и финальной группой')
@pytest.mark.parametrize('candidate_job_histories, status',
                         [(28778, {'statusId': 28815})],
                         indirect=['candidate_job_histories'])
def test_set_free_candidate_with_two_link_is_final(candidate_api_auth, new_job, candidate_job_histories, status):
    candidate_id, job_id, ch_id = candidate_job_histories
    with allure.step('Запрос, на создание еще одной связки К-В'):
        payload = generate_payload_candidate_history(candidate_id, new_job, status)
        resp_new_ch, data_new_ch = candidate_api_auth.create_candidate_histories(json=payload)
    with allure.step('Проверка, что новая связь создана успешно'):
        assert resp_new_ch.status_code == 201

    new_ch_id = data_new_ch['candidateHistoryId']

    with allure.step('Запрос, на получение связок К-В до назначения свободного кандидата'):
        _, data_feed_before = candidate_api_auth.get_feed(candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_before = FeedResponse.model_validate(data_feed_before)
    with allure.step('Проверка, что новая связка К-В не закрыта'):
        assert valid_feed_before.activeCandidateHistories[0].candidateId == candidate_id
        assert valid_feed_before.activeCandidateHistories[0].jobId == new_job
        assert valid_feed_before.activeCandidateHistories[0].candidateHistoryId == new_ch_id
        assert valid_feed_before.activeCandidateHistories[0].closedAt is None
    with allure.step('Проверка, что старая связка К-В не закрыта'):
        assert valid_feed_before.activeCandidateHistories[1].candidateId == candidate_id
        assert valid_feed_before.activeCandidateHistories[1].jobId == job_id
        assert valid_feed_before.activeCandidateHistories[1].candidateHistoryId == ch_id
        assert valid_feed_before.activeCandidateHistories[1].closedAt is None

    with allure.step('Запрос на назначение свободного кандидата по новой вакансии'):
        payload = generate_payload_free_candidate(new_job, candidate_id)
        resp, data = candidate_api_auth.set_free_candidate(json=payload, is_raise=False)
    with allure.step('Проверка, что свободный кандидат не назначился'):
        assert resp.status_code == 400
        assert 'message' in data
        assert data['message'].lower() == 'нельзя прекратить активность по данной вакансии, кандидат находится на финальном статусе.'

    with allure.step('Запрос, на получение связок К-В после назначения свободного кандидата'):
        _, data_feed_after = candidate_api_auth.get_feed(candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_after = FeedResponse.model_validate(data_feed_after)
    with allure.step('Проверка, что новая связка К-В осталась открыта'):
        assert valid_feed_after.activeCandidateHistories[0].candidateId == candidate_id
        assert valid_feed_after.activeCandidateHistories[0].jobId == new_job
        assert valid_feed_after.activeCandidateHistories[0].candidateHistoryId == new_ch_id
        assert valid_feed_after.activeCandidateHistories[0].closedAt is None
    with allure.step('Проверка, что старая связка К-В осталась открытой'):
        assert valid_feed_after.activeCandidateHistories[1].candidateId == candidate_id
        assert valid_feed_after.activeCandidateHistories[1].jobId == job_id
        assert valid_feed_after.activeCandidateHistories[1].candidateHistoryId == ch_id
        assert valid_feed_after.activeCandidateHistories[1].closedAt is None

    with allure.step('Проверка, что свободный кандидат - не назначился'):
        assert valid_feed_after.candidateHistories[0].statusId != STATUS_FREE_CANDIDATE

@allure.story('Назначение свободного кандидата на закрытую вакансию')
@pytest.mark.parametrize('candidate_job_histories',[{'statusId': 28816,'HireTermId': 1203}],indirect=True)
def test_set_free_candidate_on_closed_job(candidate_api_auth, candidate_job_histories):
    candidate_id, job_id, ch_id = candidate_job_histories

    with allure.step('Запрос, на получение связок К-В до назначения свободного кандидата'):
        _, data_feed_before = candidate_api_auth.get_feed(candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_before = FeedResponse.model_validate(data_feed_before)
    with allure.step('Проверка, что связка К-В не существует'):
        assert valid_feed_before.activeCandidateHistories[0].candidateId == candidate_id
        assert valid_feed_before.activeCandidateHistories[0].jobId == job_id
        assert valid_feed_before.activeCandidateHistories[0].candidateHistoryId == ch_id

    with allure.step('Запрос на назначение свободного кандидата по новой вакансии'):
        payload = generate_payload_free_candidate(job_id, candidate_id)
        resp, data = candidate_api_auth.set_free_candidate(json=payload, is_raise=False)
    with allure.step('Проверка, что свободный кандидат не назначился'):
        assert resp.status_code == 400
        assert 'message' in data
        assert data['message'].lower() == 'статус не был добавлен'

    with allure.step('Запрос, на получение связок после назначения свободного кандидата'):
        _, data_feed_after = candidate_api_auth.get_feed(candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_after = FeedResponse.model_validate(data_feed_after)
    with allure.step('Проверка, что связка К-В не пропала'):
        assert valid_feed_before.activeCandidateHistories[0].candidateId == candidate_id
        assert valid_feed_before.activeCandidateHistories[0].jobId == job_id
        assert valid_feed_before.activeCandidateHistories[0].candidateHistoryId == ch_id

    with allure.step('Проверка, что свободный кандидат - не назначился'):
        assert valid_feed_after.candidateHistories[0].statusId != STATUS_FREE_CANDIDATE

@allure.story('Назначение свободного кандидата при черном списке')
def test_set_free_candidate_on_black_list(candidate_api_auth, black_list_candidate):
    with allure.step('Проверяем, что Черный список - последний статус'):
        _, data_feed_before = candidate_api_auth.get_feed(black_list_candidate)
        valid_feed_before = FeedResponse.model_validate(data_feed_before)
        assert valid_feed_before.candidateHistories[0].statusId == STATUS_BLACK_LIST
    with allure.step('Проверяем, что все связки К-В закрыты'):
        assert all(isinstance(ach.closedAt, int) for ach in valid_feed_before.activeCandidateHistories)

    with allure.step('Запрос на назначение свободного кандидата'):
        payload = generate_payload_free_candidate(job_id='', candidate_id=black_list_candidate)
        response, data = candidate_api_auth.set_free_candidate(json=payload)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_free_candidate = CandidateHistory.model_validate(data)
    with allure.step('Проверка успешности назначения свободного кандидата'):
        assert response.status_code == 200
        assert valid_free_candidate.candidateId == black_list_candidate
        assert valid_free_candidate.statusId == STATUS_FREE_CANDIDATE

    with allure.step('Проверяем, что свободный кандидат - последний статус'):
        _, data_feed_after = candidate_api_auth.get_feed(black_list_candidate)
        valid_feed_after = FeedResponse.model_validate(data_feed_after)
        assert valid_feed_after.candidateHistories[0].statusId == STATUS_FREE_CANDIDATE

@allure.story('Снятие свободного кандидата назначением группы статусов')
@pytest.mark.parametrize('status', [
    {'statusId': 28814},
    {'statusId': 28810, 'ReasonId': 1304},
    {'statusId': 28807}])
def test_delete_free_candidate_set_other_status(candidate_api_auth, free_candidate, new_job, status):
    with allure.step('Проверяем, что Свободный кандидат - последний статус'):
        _, data_feed_before = candidate_api_auth.get_feed(free_candidate)
        valid_feed_before = FeedResponse.model_validate(data_feed_before)
        assert valid_feed_before.candidateHistories[0].statusId == STATUS_FREE_CANDIDATE

    with allure.step('Запрос на открытие новой группы статусов'):
        payload = generate_payload_candidate_history(free_candidate, new_job, status)
        response, data = candidate_api_auth.create_candidate_histories(json=payload)
    with allure.step('Проверка, что новая группа успешно создана'):
        assert response.status_code == 201
        new_ch_id = data['candidateHistoryId']

    with allure.step('Запрос, на получение связок К-В после снятия свободного кандидата'):
        _, data_feed_after = candidate_api_auth.get_feed(free_candidate)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_feed_after = FeedResponse.model_validate(data_feed_after)
    with allure.step('Проверка, что новая связка К-В открыта'):
        assert valid_feed_after.activeCandidateHistories[0].jobId == new_job
        assert valid_feed_after.activeCandidateHistories[0].candidateHistoryId == new_ch_id
        assert valid_feed_after.activeCandidateHistories[0].candidateStatusId == status['statusId']
    with allure.step('Проверка, что свободный кандидат не последний статус'):
        assert valid_feed_after.candidateHistories[0].statusId != STATUS_FREE_CANDIDATE