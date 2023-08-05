import logging
import requests
import json


class TelegramLogger(logging.Filter):
    def __init__(self, bot_url, token, name=""):
        self.bot_url = bot_url
        self.token = token

        super(TelegramLogger, self).__init__(name)

    def filter(self, record: logging.LogRecord) -> int:
        self.send_message(record)
        return True

    def send_message(self, record):
        headers = {'Content-type': 'application/json',  # Определение типа данных
                   'Accept': 'text/plain',
                   'Content-Encoding': 'utf-8'}
        body = {
            "token": self.token,
            "message": {
                "type": record.levelname.lower(),
                "content": record.msg
            }
        }

        r = requests.post(self.bot_url, data=json.dumps(body), headers=headers)






