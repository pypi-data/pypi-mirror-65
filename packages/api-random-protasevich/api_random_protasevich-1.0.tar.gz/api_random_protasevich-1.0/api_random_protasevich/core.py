import requests

URL_ACTION = "http://math-random-api.protasevich.su/api/game/action"
URL_START = "http://math-random-api.protasevich.su/api/game/start"
URL_TAKE = "http://math-random-api.protasevich.su/api/game/take"
URL_LINE = "http://math-random-api.protasevich.su/api/game/line"
URL_LAST = "http://math-random-api.protasevich.su/api/game/last"
URL_LOGIN = "http://math-random-api.protasevich.su/api/login"
URL_USER = "http://math-random-api.protasevich.su/api/user"
URL_SEND = "http://math-random-api.protasevich.su/api/coins/send"

class Session:
    
    def __init__(self, login='', password='', token=''):
        self.login = login
        self.password = password
        self.token = token
        self.balance = 0
        self.winnings = 0
        self.id = 0
        self.finished = {}
        self.activeGame = False
        self.game = {}
        self.headers = {
            "Authorization": "Bearer " + self.token
        }

    def auth(self):  
        self.token = requests.post(url=URL_LOGIN, params={"login": self.login, "password": self.password}).json()["token"]
        self.headers = {
            "Authorization": "Bearer " + self.token
        }

    def profile(self):
        response = requests.get(url=URL_USER, headers=self.headers).json()
        
        self.balance = response["balance"]
        self.winnings = response["winnings"]
        self.id = response["id"]
        
        return response

    def last(self):
        response = requests.get(url=URL_LAST, headers=self.headers).json()
        
        self.finished = response["finished"]
        
        if response["line"] != False:
            self.activeGame = response["line"]
        
        return response

    def line(self):
        response = requests.get(url=URL_LINE, headers=self.headers).json()
        
        if "status" not in response:
            self.activeGame = True
        else:
            self.activeGame = False
            
        return response

    def send(self, login="Bauka Alimgazy", amount=1000):
        response = requests.post(url=URL_SEND, headers=self.headers, params={"login": login, "coins": amount}).json()
        
        if response["status"] == True:
            self.balance = response["balance"]
            
        return response

    def start(self, bet=100):
        response = requests.post(url=URL_START, headers=self.headers, params={"bet": bet}).json()
        
        if "status" not in response:
            self.balance = response["balance"]
            self.finished = response["finished"]
            self.game = response["line"]
            
        return response

    def action(self, step=1):
        response = requests.post(url=URL_ACTION, headers=self.headers, params={"step": step}).json()
        
        if "status" not in response:
            self.finished = response["finished"]
            self.game = response["line"]
            
        return response

    def take(self):
        response = requests.get(url=URL_TAKE, headers=self.headers).json()
        
        if "status" not in response:
            self.balance = response["balance"]
            self.winnings = response["winnings"]
            
        return response

    

    
        

    

    
        

    












