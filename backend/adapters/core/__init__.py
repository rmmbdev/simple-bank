import requests


class Core:
    def __init__(self, base_url):
        self.base_url = base_url

    def validate_token(self, token):
        url = self.base_url + "/api/token/verify/"
        payload = {
            "token": token.split(' ')[1],
        }
        response = requests.post(url=url, data=payload)
        if response.ok:
            return True
        return False
