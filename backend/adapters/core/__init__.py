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

    def increase(self, account_id, amount, token):
        url = self.base_url + f"/api/accounts/{account_id}/increase-balance/"
        payload = {
            "amount": amount,
        }
        headers = {
            "authorization": token,
        }
        response = requests.post(url=url, data=payload, headers=headers)
        return response
