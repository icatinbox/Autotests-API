import copy

import pytest
import allure
from data_structures import BASE_PAYLOAD_TEST, BASE_PAYLOAD_CANDIDATE_HISTORIES, STATUS_ASSIGN_TEST
from tests.schemas.assignment_test_scheme import DirectoryTest, DirectoryGrade, TestAssignment
from pydantic import TypeAdapter
from datetime import datetime, timedelta

from tests.utils.utils import random_datetime_between, date_to_iso, textb64, content_from_sql_binary


@allure.feature("Тестирование. Группа статусов 06")

def generate_payload_candidate_history(candidate_id, job_id, status):
    payload = {
        **copy.deepcopy(BASE_PAYLOAD_CANDIDATE_HISTORIES),
        "CandidateId": candidate_id,
        "JobId": job_id,
        **status
    }
    return payload

def generate_payload_grade(grade_id, test_id):
    payload = {
        "testAssignmentId": test_id,
        "gradedAt": date_to_iso(datetime.now()),
        "gradeId": grade_id
    }
    return payload

def generate_payload_test_update(test_id, **change):
    payload = {
        "assignedAt": date_to_iso(datetime.now()),
        "files": [],
        'testAssignmentId': test_id,
        'comment': 'test base edit test',
        **change
    }
    return payload

def generate_payload_test_add(job_id, candidate_id, ch_id, test_id, **change):
    payload = {
        **copy.deepcopy(BASE_PAYLOAD_TEST),
        "jobId": job_id,
        "candidateId": candidate_id,
        "testId": test_id,
        "testHistoryId": ch_id,
        **change
    }
    return payload


@allure.story("Получение справочника всех тестов")
def test_get_all_tests(test_api_auth):
    with allure.step('Отправка запроса'):
        response, data = test_api_auth.get_all_directory_tests()
    with allure.step('Валидация ответа с помощью pydantic'):
        result = TypeAdapter(list[DirectoryTest]).validate_python(data)
    with allure.step('Проверка, что каждый id уникален'):
        ids = [t.testId for t in result]
        assert len(ids) == len(set(ids))

@allure.story("Получение справочника оценок")
def test_get_grades(test_api_auth):
    with allure.step('Отправка запроса'):
        response, data = test_api_auth.get_grades()
    with allure.step('Валидация ответа с помощью pydantic'):
        result = TypeAdapter(list[DirectoryGrade]).validate_python(data)
    with allure.step('Проверка, что каждый id уникален'):
        ids = [g.gradeId for g in result]
        assert len(ids) == len(set(ids))
    with allure.step('Проверка, что список отсортирован по order'):
        orders = [g.order for g in result]
        assert orders == sorted(orders)

@allure.story("Добавление теста к связке Кандидат-Вакансия со всеми заполненными полями")
@pytest.mark.parametrize('candidate_job_histories', [STATUS_ASSIGN_TEST], indirect=True)
def test_add_test_all_field(test_api_auth, candidate_job_histories, test):
    with allure.step('Подготовка payload для запроса прикрепления теста'):
        candidate_id, job_id, ch_id = candidate_job_histories
        test_id, test_name = test
        payload_add_test = generate_payload_test_add(job_id=job_id, candidate_id=candidate_id, ch_id=ch_id, test_id=test_id)

    with allure.step('Отправка запроса на прикрепление теста'):
        response, data = test_api_auth.attach_test(json=payload_add_test)
    with allure.step('Валидация ответа с помощью pydantic'):
        result = TestAssignment.model_validate(data)
    with allure.step('Проверка что поля в ответе соответствуют данным отправленным в payload'):
        assert result.jobId == job_id
        assert result.testHistoryId == ch_id
        assert result.testName == test_name

    with allure.step('Запрос на получение теста по id'):
        _, after_data_id = test_api_auth.get_test_by_id(result.testAssignmentId)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_after_id = TestAssignment.model_validate(after_data_id)
    with allure.step('Проверка что поля в ответе соответствуют данным отправленным в payload'):
        assert valid_after_id.jobId == job_id
        assert valid_after_id.testHistoryId == ch_id
        assert valid_after_id.testName == test_name

    with allure.step('Запрос на получение теста по jobId и CandidateId'):
        _, after_data_group = test_api_auth.get_tests_by_job_and_candidate(job_id, candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_after_group = TypeAdapter(list[TestAssignment]).validate_python(after_data_group)
    with allure.step('Проверка что поля в ответе соответствуют данным отправленным в payload'):
        assert valid_after_group[0].testAssignmentId == result.testAssignmentId
        assert valid_after_group[0].jobId == job_id
        assert valid_after_group[0].testHistoryId == ch_id
        assert valid_after_group[0].testName == test_name

@allure.story("Добавление теста к связке Кандидат-Вакансия без комментария")
@pytest.mark.parametrize('candidate_job_histories', [STATUS_ASSIGN_TEST], indirect=True)
def test_add_test_without_comment(test_api_auth, candidate_job_histories, test):
    with allure.step('Подготовка payload для запроса прикрепления теста'):
        candidate_id, job_id, ch_id = candidate_job_histories
        test_id, test_name = test
        payload_add_test = generate_payload_test_add(job_id=job_id, candidate_id=candidate_id, ch_id=ch_id, test_id=test_id, comment='')
    with allure.step('Отправка запроса на прикрепление теста'):
        response, data = test_api_auth.attach_test(json=payload_add_test)
    with allure.step('Валидация ответа с помощью pydantic'):
        result = TestAssignment.model_validate(data)
    with allure.step('Проверка что поля в ответе соответствуют данным отправленным в payload'):
        assert result.jobId == job_id
        assert result.testHistoryId == ch_id
        assert result.testName == test_name
        assert result.comment == ''

    with allure.step('Запрос на получение теста по id'):
        _, after_data_id = test_api_auth.get_test_by_id(result.testAssignmentId)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_after_id = TestAssignment.model_validate(after_data_id)
    with allure.step('Проверка что поля в ответе соответствуют данным отправленным в payload'):
        assert valid_after_id.jobId == job_id
        assert valid_after_id.testHistoryId == ch_id
        assert valid_after_id.testName == test_name
        assert valid_after_id.comment == ''

    with allure.step('Запрос на получение теста по jobId и CandidateId'):
        _, after_data_group = test_api_auth.get_tests_by_job_and_candidate(job_id, candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_after_group = TypeAdapter(list[TestAssignment]).validate_python(after_data_group)
    with allure.step('Проверка что поля в ответе соответствуют данным отправленным в payload'):
        assert valid_after_group[0].testAssignmentId == result.testAssignmentId
        assert valid_after_group[0].jobId == job_id
        assert valid_after_group[0].testHistoryId == ch_id
        assert valid_after_group[0].testName == test_name
        assert valid_after_group[0].comment == ''

@allure.story("Добавление теста к связке Кандидат-Вакансия без файлов")
@pytest.mark.parametrize('candidate_job_histories', [STATUS_ASSIGN_TEST], indirect=True)
def test_add_test_without_files(test_api_auth, candidate_job_histories, test):
    with allure.step('Подготовка payload для запроса прикрепления теста'):
        candidate_id, job_id, ch_id = candidate_job_histories
        test_id, test_name = test
        payload_add_test = generate_payload_test_add(job_id=job_id, candidate_id=candidate_id, ch_id=ch_id, test_id=test_id, files=[])

    with allure.step('Отправка запроса на прикрепление теста'):
        response, data = test_api_auth.attach_test(json=payload_add_test)
    with allure.step('Валидация ответа с помощью pydantic'):
        result = TestAssignment.model_validate(data)
    with allure.step('Проверка что поля в ответе соответствуют данным отправленным в payload'):
        assert result.jobId == job_id
        assert result.testHistoryId == ch_id
        assert result.testName == test_name
        assert len(result.files) == 0

    with allure.step('Запрос на получение теста по id'):
        _, after_data_id = test_api_auth.get_test_by_id(result.testAssignmentId)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_after_id = TestAssignment.model_validate(after_data_id)
    with allure.step('Проверка что поля в ответе соответствуют данным отправленным в payload'):
        assert valid_after_id.jobId == job_id
        assert valid_after_id.testHistoryId == ch_id
        assert valid_after_id.testName == test_name
        assert len(result.files) == 0

    with allure.step('Запрос на получение теста по jobId и CandidateId'):
        _, after_data_group = test_api_auth.get_tests_by_job_and_candidate(job_id, candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_after_group = TypeAdapter(list[TestAssignment]).validate_python(after_data_group)
    with allure.step('Проверка что поля в ответе соответствуют данным отправленным в payload'):
        assert valid_after_group[0].testAssignmentId == result.testAssignmentId
        assert valid_after_group[0].jobId == job_id
        assert valid_after_group[0].testHistoryId == ch_id
        assert valid_after_group[0].testName == test_name
        assert len(result.files) == 0

@allure.story("Негативная проверка. Добавление тестирования на закрытой группе 06.2, 06.3, 06.4")
@pytest.mark.parametrize('candidate_job_histories', [{'statusId': 28804, 'ReasonId': 1304}, 28803, 28859], indirect=True)
def test_negative_add_test_on_closed_testing_group(test_api_auth, candidate_job_histories, test):
    with allure.step('Подготовка payload для запроса прикрепления теста'):
        candidate_id, job_id, ch_id = candidate_job_histories
        test_id, _ = test
        payload_add_test = generate_payload_test_add(job_id=job_id, candidate_id=candidate_id, ch_id=ch_id,
                                                     test_id=test_id)
    with allure.step('Запрос на получение списка тестов до добавления нового'):
        _, before_data = test_api_auth.get_tests_by_job_and_candidate(job_id, candidate_id)

    with allure.step('Отправка запроса на прикрепление теста'):
        response, data = test_api_auth.attach_test(json=payload_add_test, is_raise=False)
    with allure.step('Проверка, что запрос завершился с ошибкой'):
        assert response.status_code == 400
        assert 'message' in data
        assert data['message'].lower() == 'нельзя добавить тестирование к закрытой группе.'

    with allure.step('Запрос на получение списка тестов после добавления нового'):
        _, after_data = test_api_auth.get_tests_by_job_and_candidate(job_id, candidate_id)
    with allure.step('Проверка, что новый тест не появился'):
        assert [t.id for t in after_data] == [t.id for t in before_data]

@allure.story("Негативная проверка. Добавление тестирования без права TEST_MANAGE")
@pytest.mark.parametrize('candidate_job_histories', [STATUS_ASSIGN_TEST], indirect=True)
def test_negative_add_test_without_rule(test_api_auth, candidate_job_histories, test, remove_permission_test_manage):
    with allure.step('Подготовка payload для запроса прикрепления теста'):
        candidate_id, job_id, ch_id = candidate_job_histories
        test_id, _ = test
        payload_add_test = generate_payload_test_add(job_id=job_id, candidate_id=candidate_id, ch_id=ch_id,
                                                     test_id=test_id)

    with allure.step('Запрос на получение списка тестов до добавления нового'):
        _, before_data = test_api_auth.get_tests_by_job_and_candidate(job_id, candidate_id)

    with allure.step('Отправка запроса на прикрепление теста'):
        response, data = test_api_auth.attach_test(json=payload_add_test, is_raise=False)
    with allure.step('Проверка, что запрос завершился с ошибкой'):
        assert response.status_code == 400
        assert 'message' in data
        assert data['message'].lower() == 'нет доступа для добавления назначенного тестирования.'

    with allure.step('Запрос на получение списка тестов после добавления нового'):
        _, after_data = test_api_auth.get_tests_by_job_and_candidate(job_id, candidate_id)
    with allure.step('Проверка, что новый тест не появился'):
        assert [t.id for t in after_data] == [t.id for t in before_data]

@allure.story("Изменение поля комментарий в тесте")
@pytest.mark.parametrize('candidate_job_histories, comment', (
    (STATUS_ASSIGN_TEST, 'success test edit comment'),
    (STATUS_ASSIGN_TEST, '129845!@@##@!'),
    (STATUS_ASSIGN_TEST, '')
), indirect=['candidate_job_histories'])
def test_edit_field_comment(test_api_auth, new_test_id_db, candidate_job_histories, comment):
    with allure.step('Запрос на получение теста до обновления'):
        _, before_data = test_api_auth.get_test_by_id(new_test_id_db)

    with allure.step('Подготовка payload для запроса обновления теста'):
        ids_tests = [dict(fileId=f['fileId']) for f in before_data["files"]]
        payload_update_test = generate_payload_test_update(
            test_id = new_test_id_db,
            assignedAt = before_data["assignedAt"],
            files = ids_tests,
            comment = comment
        )
    with allure.step('Отправка запроса на обновление теста'):
        _, data = test_api_auth.update_test(json=payload_update_test)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_data = TestAssignment.model_validate(data)
    with allure.step('Проверка, что изменилось только поле "Комментарий"'):
        assert valid_data.testAssignmentId == new_test_id_db
        assert valid_data.comment == comment
        assert data['assignedAt'] == before_data["assignedAt"]
        assert [f.fileId for f in valid_data.files] == [f['fileId'] for f in before_data["files"]]

    with allure.step('Запрос на получение теста после обновления'):
        _, after_data = test_api_auth.get_test_by_id(new_test_id_db)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_after_data = TestAssignment.model_validate(after_data)
    with allure.step('Проверка, что изменилось только поле "Комментарий"'):
        assert valid_after_data.testAssignmentId == new_test_id_db
        assert valid_after_data.comment == comment
        assert after_data['assignedAt'] == before_data["assignedAt"]
        assert [f.fileId for f in valid_after_data.files] == [f['fileId'] for f in before_data["files"]]

@allure.story("Изменение даты назначения тестирования в тесте")
@pytest.mark.parametrize('candidate_job_histories, assigned', (
        (STATUS_ASSIGN_TEST, date_to_iso(datetime.now())),
        (STATUS_ASSIGN_TEST, random_datetime_between(datetime.now(), datetime.now() + timedelta(days=30))),
        (STATUS_ASSIGN_TEST, random_datetime_between(datetime.now() - timedelta(days=30), datetime.now())),
), indirect=['candidate_job_histories'])
def test_edit_field_assigned_at(test_api_auth, new_test_id_db, candidate_job_histories, assigned):
    with allure.step('Запрос на получение теста до обновления'):
        _, before_data = test_api_auth.get_test_by_id(new_test_id_db)

    with allure.step('Подготовка payload для запроса обновления теста'):
        ids_tests = [dict(fileId=f['fileId']) for f in before_data["files"]]
        print(before_data)
        payload_update_test = generate_payload_test_update(
            test_id = new_test_id_db,
            assignedAt = assigned,
            files = ids_tests,
            comment = content_from_sql_binary(before_data["comment"])
        )

    with allure.step('Отправка запроса на обновление теста'):
        _, data = test_api_auth.update_test(json=payload_update_test)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_data = TestAssignment.model_validate(data)
    with allure.step('Проверка, что изменилось только поле "Дата прикрепления"'):
        assert valid_data.testAssignmentId == new_test_id_db
        assert valid_data.comment == before_data["comment"]
        assert date_to_iso(valid_data.assignedAt) == assigned
        assert [f.fileId for f in valid_data.files] == [f['fileId'] for f in before_data["files"]]

    with allure.step('Запрос на получение теста после обновления'):
        _, after_data = test_api_auth.get_test_by_id(new_test_id_db)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_after_data = TestAssignment.model_validate(after_data)
    with allure.step('Проверка, что изменилось только поле "Дата прикрепления"'):
        assert valid_after_data.testAssignmentId == new_test_id_db
        assert valid_after_data.comment == before_data["comment"]
        assert date_to_iso(valid_after_data.assignedAt) == assigned
        assert [f.fileId for f in valid_after_data.files] == [f['fileId'] for f in before_data["files"]]

@allure.story("Изменение файлов теста")
@pytest.mark.parametrize('candidate_job_histories, file', (
        (STATUS_ASSIGN_TEST, [{'fileName': 'test.pdf', 'content': textb64('Я изменяю текст комментария')}]),
        (STATUS_ASSIGN_TEST, [{'fileName': 'test.txt', 'content': textb64('1020304110102";!"№@')}, {'fileName': 'test1.pdf', 'content': textb64('New текст комментария очень преисполненного кандидата')}]),
        (STATUS_ASSIGN_TEST, [{'fileName': 'test.img', 'content': textb64('Это картинка разрешения img 0011')}]),
        (STATUS_ASSIGN_TEST, [{'fileName': 'test.docx', 'content': textb64('Это file с расширением docx, он открывается в программе_word')}]),
), indirect=['candidate_job_histories'])
def test_edit_field_file(test_api_auth, new_test_id_db, candidate_job_histories, file):
    with allure.step('Запрос на получение теста до обновления'):
        _, before_data = test_api_auth.get_test_by_id(new_test_id_db)

    with allure.step('Подготовка payload для запроса обновления теста'):
        payload_update_test = generate_payload_test_update(
            test_id = new_test_id_db,
            assignedAt = before_data["assignedAt"],
            files = file,
            comment = before_data["comment"]
        )

    with allure.step('Отправка запроса на обновление теста'):
        _, data = test_api_auth.update_test(json=payload_update_test)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_data = TestAssignment.model_validate(data)
    with allure.step('Проверка, что изменились только прикрепленные файлы'):
        assert valid_data.testAssignmentId == new_test_id_db
        assert valid_data.comment == before_data["comment"]
        assert date_to_iso(valid_data.assignedAt) == before_data["assignedAt"]
        assert [f.fileId for f in valid_data.files] != [f['fileId'] for f in before_data["files"]]
        assert [f.fileName for f in valid_data.files] == [f['fileName'] for f in file]

    with allure.step('Запрос на получение теста после обновления'):
        _, after_data = test_api_auth.get_test_by_id(new_test_id_db)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_after_data = TestAssignment.model_validate(after_data)
    with allure.step('Проверка, что изменились только прикрепленные файлы'):
        assert valid_after_data.testAssignmentId == new_test_id_db
        assert valid_after_data.comment == before_data["comment"]
        assert date_to_iso(valid_after_data.assignedAt) == before_data["assignedAt"]
        assert [f.fileId for f in valid_after_data.files] != [f['fileId'] for f in before_data["files"]]
        assert [f.fileName for f in valid_data.files] == [f['fileName'] for f in file]

@allure.story("Негативная проверка. Добавление тестирования без права TEST_MANAGE")
@pytest.mark.parametrize('candidate_job_histories', [STATUS_ASSIGN_TEST], indirect=True)
def test_negative_update_without_permission(test_api_auth, new_test_id_db, remove_permission_test_manage, candidate_job_histories):
    with allure.step('Запрос на получение теста до обновления'):
        _, before_data = test_api_auth.get_test_by_id(new_test_id_db)

    with allure.step('Подготовка payload для запроса обновления теста'):
        payload_update_test = generate_payload_test_update(test_id=new_test_id_db, comment='test edit without permission')

    with allure.step('Отправка запроса на обновление теста'):
        response, data = test_api_auth.update_test(json=payload_update_test, is_raise=False)
    with allure.step('Проверка, что запрос завершился с ошибкой'):
        assert response.status_code == 400
        assert 'message' in data
        assert data['message'].lower() == 'нет доступа для редактирования назначенного тестирования.'

    with allure.step('Запрос на получение теста после обновления'):
        _, after_data = test_api_auth.get_test_by_id(new_test_id_db)
    with allure.step('Проверка, что данные не изменились'):
        assert after_data['isEditable'] == False
        assert before_data == after_data

@allure.story("Негативная проверка. Изменения тестирования на статусах отличных от 6.1")
@pytest.mark.parametrize('candidate_job_histories, status',
    (
        (STATUS_ASSIGN_TEST, {'statusId': 28803}),
        (STATUS_ASSIGN_TEST, {'statusId': 28804, "ReasonId": 1304}),
        (STATUS_ASSIGN_TEST, {'statusId': 28859})
    ),
                         indirect=['candidate_job_histories'])
def test_negative_update_other_status(test_api_auth, new_test_id_db, candidate_api_auth, candidate_job_histories, status):
    with allure.step('Запрос на получение теста до обновления'):
        _, before_data = test_api_auth.get_test_by_id(new_test_id_db)

    with allure.step('Перевод группы 06 на другой подстатус(06.1, 06.2, 06.3'):
        candidate_id, job_id, _ = candidate_job_histories
        resp, _ = candidate_api_auth.create_candidate_histories(
            json=generate_payload_candidate_history(candidate_id, job_id, status)
        )
    with allure.step('Проверка, что подстатус изменен успешно'):
        assert resp.status_code == 201

    with allure.step('Отправка запроса на обновление теста'):
        payload_update_test = generate_payload_test_update(test_id=new_test_id_db, comment='update test on other status 6.1')
        response, data = test_api_auth.update_test(json=payload_update_test, is_raise=False)
    with allure.step('Проверка, что запрос завершился с ошибкой'):
        assert response.status_code == 400
        assert 'message' in data
        assert data['message'].lower() == 'нельзя добавить тестирование к закрытой группе.'

    with allure.step('Запрос на получение теста после обновления'):
        _, after_data = test_api_auth.get_test_by_id(new_test_id_db)
    with allure.step('Проверка, что данные не изменились'):
        assert after_data['isEditable'] == False
        assert before_data['comment'] == after_data['comment']

@allure.story("Удаление тестирования")
@pytest.mark.parametrize('candidate_job_histories', [STATUS_ASSIGN_TEST], indirect=True)
def test_delete_test(test_api_auth, new_test_id_db, candidate_job_histories):
    with allure.step('Запрос на получение теста до удаления'):
        response_before, _ = test_api_auth.get_test_by_id(new_test_id_db)
    with allure.step('Проверка, что получение теста до удаления успешно'):
        assert response_before.status_code == 200

    with allure.step('Запрос на удаление теста'):
        response, _ = test_api_auth.delete_test(new_test_id_db)
    with allure.step('Проверка, что удаление теста успешно'):
        assert response.status_code == 200

    with allure.step('Запрос на получение теста после удаления'):
        response_after, _ = test_api_auth.get_test_by_id(new_test_id_db, is_raise=False)
    with allure.step('Проверка, что после удаления теста 404, теста не существует'):
        assert response_after.status_code == 404

@allure.story("Негативная проверка. Удаление тестирования без права TEST_MANAGE")
@pytest.mark.parametrize('candidate_job_histories', [STATUS_ASSIGN_TEST], indirect=True)
def test_negative_delete_test_without_permission(test_api_auth, new_test_id_db, candidate_job_histories, remove_permission_test_manage):
    with allure.step('Запрос на получение теста до удаления'):
        response_before, data_before = test_api_auth.get_test_by_id(new_test_id_db)
    with allure.step('Проверка, что получение теста до удаления успешно'):
        assert response_before.status_code == 200

    with allure.step('Запрос на удаление теста'):
        response, data = test_api_auth.delete_test(new_test_id_db, is_raise=False)
    with allure.step('Проверка, что запрос завершился с ошибкой'):
        assert response.status_code == 400
        assert 'message' in data
        assert data['message'].lower() == 'нет доступа для удаления назначенного тестирования.'

    with allure.step('Запрос на получение теста после удаления'):
        response_after, data_after = test_api_auth.get_test_by_id(new_test_id_db)
    with allure.step('Проверка, что после неуспешногшо удаления теста - тест существует и не изменился'):
        assert response_after.status_code == 200
        assert data_before == data_after

@allure.story("Выставление оценки тестирования")
@pytest.mark.parametrize('candidate_job_histories, status',
    (
        (STATUS_ASSIGN_TEST, {'statusId': 28803}),
        (STATUS_ASSIGN_TEST, {'statusId': 28804, "ReasonId": 1304}),
        (STATUS_ASSIGN_TEST, {'statusId': 28859})
    ),
                         indirect=['candidate_job_histories'])
def test_edit_grade(test_api_auth, new_test_id_db, grade, candidate_api_auth, candidate_job_histories, status):
    with allure.step('Подготовка и запрос на изменение подстатуса группы'):
        candidate_id, job_id, _ = candidate_job_histories
        grade_id, grade_name = grade
        resp_ch, _ =candidate_api_auth.create_candidate_histories(
            json=generate_payload_candidate_history(candidate_id, job_id, status)
        )
    with allure.step('Проверка, что запрос на изменение подстатуса завершился успешно'):
        assert resp_ch.status_code == 201

    with allure.step('Подготовка и запрос на выставление оценки тестирования'):
        payload_grade = generate_payload_grade(grade_id, new_test_id_db)
        _, data = test_api_auth.give_grade(json=payload_grade)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_data = TestAssignment.model_validate(data)
    with allure.step('Проверка, что в ответе поля оценки и даты оценки изменились'):
        assert date_to_iso(valid_data.gradeAt) == payload_grade['gradedAt']
        assert valid_data.gradeName == grade_name

    with allure.step('Получение теста по id'):
        _, after_data_id = test_api_auth.get_test_by_id(new_test_id_db)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_after_data_id = TestAssignment.model_validate(after_data_id)
    with allure.step('Проверка, что поля оценки и даты оценки изменились'):
        assert date_to_iso(valid_after_data_id.gradeAt) == payload_grade['gradedAt']
        assert valid_after_data_id.gradeName == grade_name

    with allure.step('Получение теста по candidateId и jobId'):
        _, after_data_group = test_api_auth.get_tests_by_job_and_candidate(job_id, candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_after_data_group = TypeAdapter(list[TestAssignment]).validate_python(after_data_group)
    with allure.step('Проверка, что поля оценки и даты оценки изменились'):
        assert valid_after_data_group[0].gradeName == grade_name
        assert date_to_iso(valid_after_data_group[0].gradeAt) == payload_grade['gradedAt']

@allure.story("Негативный кейс. Выставление оценки тестирования без права TEST_GRADE")
@pytest.mark.parametrize('candidate_job_histories, status',
    (
        (STATUS_ASSIGN_TEST, {'statusId': 28803}),
        (STATUS_ASSIGN_TEST, {'statusId': 28804, "ReasonId": 1304}),
        (STATUS_ASSIGN_TEST, {'statusId': 28859})
    ),
                         indirect=['candidate_job_histories'])
def test_negative_grade_without_permission(
        test_api_auth,
        new_test_id_db,
        grade,
        remove_permission_test_grade,
        candidate_api_auth,
        candidate_job_histories,
        status
):
    with allure.step('Подготовка и запрос на изменение подстатуса группы'):
        candidate_id, job_id, _ = candidate_job_histories
        grade_id, grade_name = grade
        resp_ch, _ =candidate_api_auth.create_candidate_histories(
            json=generate_payload_candidate_history(candidate_id, job_id, status)
        )
    with allure.step('Проверка, что запрос на изменение подстатуса завершился успешно'):
        assert resp_ch.status_code == 201

    with allure.step('Подготовка и запрос на выставление оценки тестирования'):
        payload_grade = generate_payload_grade(grade_id, new_test_id_db)
        response, data = test_api_auth.give_grade(json=payload_grade, is_raise=False)
    with allure.step('Проверка, что запрос завершился с ошибкой'):
        assert response.status_code == 400
        assert 'message' in data
        assert data['message'].lower() == 'нет доступа к выставлению оценки тестирования.'

    with allure.step('Получение теста по id'):
        _, after_data_id = test_api_auth.get_test_by_id(new_test_id_db)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_after_data_id = TestAssignment.model_validate(after_data_id)
    with allure.step('Проверка, что поля оценки и даты оценки не изменились'):
        assert valid_after_data_id.gradeAt is None
        assert valid_after_data_id.gradeName is None

    with allure.step('Получение теста по candidateId и jobId'):
        _, after_data_group = test_api_auth.get_tests_by_job_and_candidate(job_id, candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_after_data_group = TypeAdapter(list[TestAssignment]).validate_python(after_data_group)
    with allure.step('Проверка, что поля оценки и даты оценки не изменились'):
        assert valid_after_data_group[0].gradeAt is None
        assert valid_after_data_group[0].gradeName is None

@allure.story("Негативный кейс. Выставление оценки тестирования на статусах отличных от 06.2, 06.3, 06.4")
@pytest.mark.parametrize('candidate_job_histories', [STATUS_ASSIGN_TEST], indirect=True)
def test_negative_grade_other_status(
        test_api_auth,
        new_test_id_db,
        grade,
        candidate_job_histories
):
    with allure.step('Подготовка и запрос на выставление оценки на статусе 06.1'):
        candidate_id, job_id, _ = candidate_job_histories
        grade_id, grade_name = grade
        payload_grade = generate_payload_grade(grade_id, new_test_id_db)
        response, data = test_api_auth.give_grade(json=payload_grade, is_raise=False)
    with allure.step('Проверка, что запрос завершился с ошибкой'):
        assert response.status_code == 400
        assert 'message' in data
        assert data['message'].lower() == 'на данном этапе редактирование тестирования недоступно.'

    with allure.step('Получение теста по id'):
        _, after_data_id = test_api_auth.get_test_by_id(new_test_id_db)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_after_data_id = TestAssignment.model_validate(after_data_id)
    with allure.step('Проверка, что поля оценки и даты оценки не изменились'):
        assert valid_after_data_id.gradeAt is None
        assert valid_after_data_id.gradeName is None

    with allure.step('Получение теста по candidateId и jobId'):
        _, after_data_group = test_api_auth.get_tests_by_job_and_candidate(job_id, candidate_id)
    with allure.step('Валидация ответа с помощью pydantic'):
        valid_after_data_group = TypeAdapter(list[TestAssignment]).validate_python(after_data_group)
    with allure.step('Проверка, что поля оценки и даты оценки не изменились'):
        assert valid_after_data_group[0].gradeAt is None
        assert valid_after_data_group[0].gradeName is None

@allure.story("Кастомное создание теста")
def test_create_custom_test(test_api_auth, permission_full_admin):
    with allure.step('Запрос список тестов до создания нового'):
        _, before_data = test_api_auth.get_all_directory_tests()

    ids_before = {t['testId'] for t in before_data}

    with allure.step('Подготовка и запрос на создание кастомного теста'):
        payload = {'name': 'create new custom test'}
        response, data = test_api_auth.create_custom_test(json=payload)
    with allure.step('Проверка, что новый кастомный тест создан'):
        assert response.status_code == 200
        assert data['statusCode'] == 200
        assert data['isSuccessful'] == True
        assert data['responseObject']['isCustom'] == True
        assert data['responseObject']['name'] == payload['name']

    test_id = data['responseObject']['testId']

    with allure.step('Запрос список тестов после создания нового'):
        _, after_data = test_api_auth.get_all_directory_tests()
    with allure.step('Проверка, что в списке тестирований появился новый тест'):
        ids_after = {t['testId'] for t in after_data}
        dif_ids = ids_after.difference(ids_before)
        assert test_id in dif_ids

@allure.story("Негативный кейс. Кастомное создание теста без прав")
def test_negative_create_custom_test_without_permission(test_api_auth):
    with allure.step('Запрос список тестов до создания нового'):
        _, before_data = test_api_auth.get_all_directory_tests()

    with allure.step('Подготовка и запрос на создание кастомного теста'):
        payload = {'name': 'create new custom test'}
        response, data = test_api_auth.create_custom_test(json=payload, is_raise=False)
    with allure.step('Проверка, что запрос завершился с ошибкой'):
        assert response.status_code == 400
        assert 'message' in data
        assert data['message'].lower() == 'нет доступа для создания нового описания тестирования.'

    with allure.step('Запрос список тестов до создания нового'):
        _, after_data = test_api_auth.get_all_directory_tests()
    with allure.step('Проверка, что в списке тестирований не появился новый тест'):
        assert sorted([t['testId'] for t in before_data]) == sorted([t['testId'] for t in after_data])
