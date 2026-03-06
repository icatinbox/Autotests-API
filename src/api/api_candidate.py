
class CandidateApi:
    def __init__(self, client):
        self.client = client

    def create_candidate(self, **kwargs):
        return self.client.request_json(method='POST', path='/api/Candidates/Create', **kwargs)

    def delete_candidate(self, id_candidate):
        return self.client.request(method='DELETE', path=f'/api/Candidates/{id_candidate}')

    def create_candidate_histories(self, **kwargs):
        return self.client.request_json(method='POST', path='/api/Candidates/CandidateHistories', **kwargs)\

    def set_black_list(self, **kwargs):
        return self.client.request_json(method='POST', path='/api/Candidates/SetBlackList', **kwargs)

    def get_feed(self, id_candidate):
        return self.client.request_json(method='GET', path=f'/api/Candidates/{id_candidate}/Feed')

    def set_free_candidate(self, **kwargs):
        return self.client.request_json(method='POST', path='/api/Candidates/CloseVacancyLink', **kwargs)