Description
===========

Модуль для удобной работы с API сайта "random.protasevich.su".
Написал Bauka Alimgazy.

Главный класс Session хранит в себе данные о аккаунте: баланс, общий выигрыш, логин, пароль, айди, токен и другие и имеет методы как начать игру, ходить, узнать информацию о профиле.

Атрибуты:
str login
str password
str token
int balance
int id
int winnings
dict finished
bool activeGame
dict game
dict headers

Методы:
def __init__(self, login='', password='', token='')
def auth(self)
def profile(self)
def last(self):
def line(self)
def send(self, login="Bauka Alimgazy", amount=1000)
def start(self, bet=100)
def action(self, step=1)
def take(self)
