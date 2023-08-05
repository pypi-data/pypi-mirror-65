import os
import requests

class Sdk:
    def  __init__(self, token):
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(token)
        }
    def send(self, recipient, message):
        pl = {
            "recipient": recipient,
            "message"  : message
        }
        url = 'https://api.notimation.com/api/v1/sms'
        response = requests.request("POST", url, json=pl, headers=self.headers)
        return response.json()

    def get_message(self, sms_id=None):
        url = 'https://api.notimation.com/api/v1/sms'
        if sms_id:
            url = url+'/{}'.format(sms_id)
        response = requests.request("GET", url, headers=self.headers)
        return response.json()
    
    def get_phone(self, number, country_code='ar'):
        url = 'https://api.notimation.com/api/v1/phone_number/{}/{}'.format(country_code, number)
        response = requests.request("GET", url, headers=self.headers)
        return response.json()
