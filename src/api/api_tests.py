class TestApi:
    def __init__(self, client):
        self.client = client

    def get_all_directory_tests(self):
         return self.client.request_json(method="GET", path="/api/TestAssignments/definitions")

    def get_test_by_id(self, test_id, **kwargs):
        return self.client.request_json(method="GET", path=f"/api/TestAssignments/{test_id}", **kwargs)

    def get_tests_by_job_and_candidate(self, job_id, candidate_id):
        return self.client.request_json(method="GET", path=f"/api/TestAssignments/groups/{job_id}/{candidate_id}")

    def get_grades(self):
        return self.client.request_json(method="GET", path="/api/TestAssignments/grades")

    def attach_test(self, **kwargs):
        return self.client.request_json(method="POST", path="/api/TestAssignments", **kwargs)

    def update_test(self, **kwargs):
        return self.client.request_json(method="PUT", path=f"/api/TestAssignments", **kwargs)

    def delete_test(self, test_id, **kwargs):
        return self.client.request_json(method="DELETE", path=f"/api/TestAssignments/{test_id}", **kwargs)

    def give_grade(self, **kwargs):
        return self.client.request_json(method="POST", path="/api/TestAssignments/grade", **kwargs)

    def create_custom_test(self, **kwargs):
        return self.client.request_json(method="POST", path="/api/TestAssignments/definitions", **kwargs)
