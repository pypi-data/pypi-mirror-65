import requests

class InvalidTokenError(Exception):
    def __init__(self, token):
        self.token = token
    
class Pingmeen:
    def __init__(self, token):
        self.token = token
        response = self.__server_query('validate_token')
        if response != 'true':
            print('"' + self.token + '" is not valid token. You can get new valid token by sending message to Pingmeen bot in Telegram ( https://t.me/PingmeenBot )')
            raise InvalidTokenError(self.token)
        
    def finish(self):
        self.__server_query('send_message')
        
    def __server_query(self, method):
        url = 'http://2kolobka.pro/nikita/pingmeen/'
        return requests.get(url + method + '.php?token=' + self.token).text