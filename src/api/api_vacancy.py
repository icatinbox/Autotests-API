
class VacancyApi:
    def __init__(self, client):
        self.client = client

    def create_vacancy(self, payload):
       return self.client.request_json(method='POST', path='/api/Jobs', json=payload)

    def delete_vacancy(self, id_vacancy):
        return self.client.request(method='DELETE', path=f'/api/Jobs/{id_vacancy}')