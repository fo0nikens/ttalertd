#! /usr/bin/python3
# James Loye Colley
from twilio.rest import Client
from utils.read_write import read_data
from utils.log import log
from sys import exit


class Alert:
    def __init__(self, messages):
        self.messages = ' '.join(messages)
        self.credentials = []
        self.log = log()

    def read_credentials(self):
        try:
            self.credentials = read_data('utils/credentials.yml')
        except Exception as error:
            m = 'Ensure credentials.yml is filled out correctly'
            self.log.log_critical(m)
            self.log.log_error(error)
            exit(1)

    def send_sms(self):
        account_sid, auth_token, home, twilio = self.credentials
        client = Client(account_sid, auth_token)
        try:
            client.messages.create(to=home, from_=twilio, body=self.messages)
        except Exception as e:
            m = 'Unable to send SMS message'
            self.log.log_error(m)
            self.log.log_error(e)
            exit(1)
