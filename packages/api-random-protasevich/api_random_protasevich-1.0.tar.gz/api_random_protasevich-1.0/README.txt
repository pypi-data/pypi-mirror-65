Description
===========

������ ��� ������� ������ � API ����� "random.protasevich.su".
������� Bauka Alimgazy.

������� ����� Session ������ � ���� ������ � ��������: ������, ����� �������, �����, ������, ����, ����� � ������ � ����� ������ ��� ������ ����, ������, ������ ���������� � �������.

��������:
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

������:
def __init__(self, login='', password='', token='')
def auth(self)
def profile(self)
def last(self):
def line(self)
def send(self, login="Bauka Alimgazy", amount=1000)
def start(self, bet=100)
def action(self, step=1)
def take(self)
