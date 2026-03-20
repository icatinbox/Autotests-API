import copy
import pytest
from data_structures import BASE_PAYLOAD_CANDIDATE_HISTORIES, PAYLOAD_BLACK_LIST, STATUS_FREE_CANDIDATE


@pytest.fixture
def black_list_candidate(candidate_api_auth, candidate_job_histories):
    candidate_id, job_id, candidate_history_id = candidate_job_histories
    payload = {
        **copy.deepcopy(PAYLOAD_BLACK_LIST),
        'candidateId': candidate_id
    }
    _, data = candidate_api_auth.set_black_list(json=payload)
    return candidate_id

@pytest.fixture
def free_candidate(candidate_api_auth, candidate_job_histories):
    candidate_id, job_id, candidate_history_id = candidate_job_histories
    payload = {
        **copy.deepcopy(BASE_PAYLOAD_CANDIDATE_HISTORIES),
        'jobId': job_id,
        "candidateId": candidate_id,
        "statusId": STATUS_FREE_CANDIDATE,
    }
    _, data = candidate_api_auth.set_free_candidate(json=payload)
    return candidate_id