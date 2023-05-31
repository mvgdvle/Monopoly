#-*- coding: utf-8 -*-
from field import Field
from street import Street
from public_transport import PublicTransport


class Board:
    def __init__(self):
        self.board = []

    def get_field(self, position):
        return self.board[position]

    def create(self):
        self.board.append(Field('Start', 0))
        self.board.append(Street('RZESZÓW ul.Fryderyka Szopena', 1, 'pink', price_field=60, price_house=50, tax=6))
        self.board.append(Field('Karta szans', 2, is_chance=True))
        self.board.append(Street('RZESZÓW ul.Baldachówka', 3, 'pink', price_field=60, price_house=50, tax=6))
        self.board.append(Street('RZESZÓW ul.Hetmańska', 4, 'pink', price_field=65, price_house=50, tax=10))
        self.board.append(PublicTransport('Dworzec Kolejowy', 5, price_field=200))
        self.board.append(Street('BIAŁYSTOK ul.Jana Kiemensa Branickiego', 6, 'red', price_field=100, price_house=50,
                                 tax=10))
        self.board.append(Field('Karta szans', 7, is_chance=True))
        self.board.append(Street('BIAŁYSTOK ul.Legionowa', 8, 'red', price_field=100, price_house=50, tax=10))
        self.board.append(Street('BIAŁYSTOK ul.Rynek Kościuszki', 9, 'red', price_field=120, price_house=50, tax=12))
        self.board.append(Field('Więzienie', 10, is_jail=True))
        self.board.append(Street('SZCZECIN Aleje Papieża Jana Pawła II', 11, 'lime', price_field=140, price_house=100,
                                 tax=14))
        self.board.append(PublicTransport('Port', 12, price_field=150))
        self.board.append(Street('SZCZECIN Aleja Piastów', 13, 'lime', price_field=140, price_house=100, tax=14))
        self.board.append(Street('SZCZECIN ul.Koński Kierat', 14, 'lime', price_field=160, price_house=100, tax=16))
        self.board.append(PublicTransport('Dworzec Autobusowy', 15, price_field=200))
        self.board.append(Street('TRÓJMIASTO ul.Świętojańska (Gdynia)', 16, 'green', price_field=180, price_house=100,
                                 tax=18))
        self.board.append(Field('Karta szans', 17, is_chance=True))
        self.board.append(Street('TRÓJMIASTO ul.Bohaterów Monte Cassino (Sopot)', 18, 'green', price_field=180,
                                 price_house=100, tax=18))
        self.board.append(Street('TRÓJMIASTO ul.Długi Targ (Gdańsk)', 19, 'green', price_field=200, price_house=100,
                                 tax=20))
        self.board.append(Field('Parking', 20, is_parking=True))
        self.board.append(Street('POZNAŃ ul.Garbary', 21, 'blue', price_field=220, price_house=150, tax=22))
        self.board.append(Field('Karta szans', 22, is_chance=True))
        self.board.append(Street('POZNAŃ ul.Święty Marcin', 23, 'blue', price_field=220, price_house=150, tax=22))
        self.board.append(Street('POZNAŃ Stary Rynek', 24, 'blue', price_field=240, price_house=150, tax=24))
        self.board.append(PublicTransport('Lotnisko', 25, price_field=200))
        self.board.append(Street('WROCŁAW ul.Grabiszyńska', 26, 'purple', price_field=260, price_house=150, tax=26))
        self.board.append(Street('WROCŁAW ul.Nożownicza', 27, 'purple', price_field=260, price_house=150, tax=26))
        self.board.append(PublicTransport('Wypożyczalnia aut', 28, price_field=150))
        self.board.append(Street('WROCŁAW Rynek', 29, 'purple', price_field=280, price_house=150, tax=28))
        self.board.append(Field('Więzienie', 30, is_jail=True))
        self.board.append(Street('KRAKÓW ul.Królowej Jadwigi', 31, 'yellow', price_field=300, price_house=200, tax=30))
        self.board.append(Street('KRAKÓW ul.Floriańska', 32, 'yellow', price_field=300, price_house=200, tax=30))
        self.board.append(Field('Karta szans', 33, is_chance=True))
        self.board.append(Street('KRAKÓW Rynek Główny', 34, 'yellow', price_field=320, price_house=200, tax=32))
        self.board.append(PublicTransport('Zajezdnia Tramwajowa', 35, price_field=200))
        self.board.append(Field('Karta szans', 33, is_chance=True))
        self.board.append(Street('WARSZAWA Aleje Jerozolimskie', 37, 'orange', price_field=350, price_house=200,
                                 tax=35))
        self.board.append(Street('WARSZAWA ul.Marszałkowska', 38, 'orange', price_field=350, price_house=200, tax=35))
        self.board.append(Street('WARSZAWA Krakowskie Przedmieścia', 39, 'orange', price_field=400, price_house=200,
                                 tax=40))
