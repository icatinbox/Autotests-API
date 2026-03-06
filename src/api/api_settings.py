class SettingsApi:
    def __init__(self, client):
        self.client = client

    def change_permission(self, **kwargs):
        return self.client.request(method='PATCH', path='/api/Roles/', **kwargs)

    def change_role(self, **kwargs):
        return self.client.request(method='PUT', path='/api/Accounts', **kwargs)
