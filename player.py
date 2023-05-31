#-*- coding: utf-8 -*-
from street import Street
from public_transport import PublicTransport


class Player:
    def __init__(self, nick, money=1500, current_position=0):
        self.nick = nick
        self.money = money
        self.current_position = current_position
        self.bankrupt = False
        self.jail_sentence = 0
        self.public_transport = []
        self.streets = {}

    def get_nick(self):
        return self.nick

    def get_money(self):
        return self.money

    def pay(self, amount):
        self.money -= amount
        print(f'Gracz {self.get_nick()} wydał {amount} zł. Aktualny stan konta: {self.get_money()} zł. ')

    def earn(self, amount):
        self.money += amount
        print(f'Gracz {self.get_nick()} zarobił {amount} zł. Aktualny stan konta: {self.get_money()} zł. ')

    def move(self, steps):
        new_position = (self.current_position + steps) % 40
        if new_position < self.current_position:
            print('Przechodzisz przez pole Start.')
            self.earn(200)
        self.current_position = new_position

    def go_to_field(self, position):
        self.current_position = position

    def get_position(self):
        return self.current_position

    def get_streets(self):
        return self.streets

    def get_jail_sentence(self):
        return self.jail_sentence

    def take_jail_sentence(self):
        self.jail_sentence -= 1

    def go_to_jail(self, time):
        self.jail_sentence += time+1
        self.go_to_field(30)

    def is_bankrupt(self):
        return self.bankrupt

    def go_bankrupt(self):
        self.bankrupt = True
        self.money = 0
        self.streets = {}
        self.public_transport = []
        print(f'Gracz {self.nick} zbankrutował i kończy grę. ')

    def get_tax_pt(self, field, roll):
        n = len(self.public_transport)
        return field.count_tax(n, roll)

    def get_tax_st(self, field):
        full = False
        if len(self.streets[field.get_color()]) == 3:
            full = True
        return field.count_tax(full)

    def add_public_transport(self, field):
        self.public_transport.append(field)

    def add_street(self, field):
        color = field.get_color()
        if self.streets.get(color):
            self.streets[color].append(field)
        else:
            self.streets[color] = [field]

    def change_owner_street(self, new_owner):
        if new_owner:
            if self.streets == {}:
                return
            print(f'Pola: {self.print_streets()} teraz należą do {new_owner.get_nick()}. ')
            for lst in self.streets.values():
                for i in lst:
                    new_owner.add_street(i)
                    i.change_owner(None)
            self.streets = {}
        else:
            for lst in self.streets.values():
                for i in lst:
                    i.change_owner(None)

    def change_owner_public_transport(self, new_owner):
        if new_owner:
            if not self.public_transport:
                return
            print(f'Pola: \n{self.print_transport()} teraz należą do {new_owner.get_nick()}. ')
            for i in self.public_transport:
                new_owner.add_public_transport(i)
                i.change_owner(None)
            self.public_transport = []
        else:
            for i in self.public_transport:
                i.change_owner(None)

    def buy_property(self, field):
        price = field.get_price_field()
        if self.money < price:
            raise ValueError('Niewystarczająca ilość środków na koncie.')
        self.pay(price)
        field.change_owner(self)

        if isinstance(field, Street):
            color = field.get_color()
            if self.streets.get(color):
                self.streets[color].append(field)
            else:
                self.streets[color] = [field]
        if isinstance(field, PublicTransport):
            self.public_transport.append(field)

        print(f'Gratulacje! Kupiłeś nowe pole: {field.get_name()}. ')

    def build_house(self, street):
        price = street.get_price_house()
        houses = street.get_houses()
        if self.money < price:
            raise ValueError('Niewystarczająca ilość środków na koncie.')
        if houses > 4:
            raise ValueError('Nie można wybudować kolejnego domu. Limit domów na tej ulicy został osiągnięty.')

        self.pay(price)
        street.build_house()
        print(f'Wybudowałeś dom na ulicy {street.get_name()}. Gratulacje! ')

    def build_hotel(self, street):
        price = street.get_price_house()
        houses = street.get_houses()
        if houses != 4:
            raise ValueError('Nie mozna wybudowac hotelu. Niewystarczajca ilosc wybudowanych domow.')
        if self.money < price:
            raise ValueError('Niewystarczajaca ilosc srodkow na koncie.')

        self.money -= price
        street.build_hotel()
        print(f'Wybudowałeś hotel na ulicy {street.get_name()}. Gratulacje! ')

    def print_transport(self):
        if len(self.public_transport) == 0:
            return 0
        else:
            t = ''
            for i in self.public_transport:
                t = t + i.get_name() + ', '
            return t[:-2]

    def print_streets(self):
        if len(self.streets) == 0:
            return 0
        else:
            x = ''
            for street, lst in self.streets.items():
                buildings = ''
                for i in lst:
                    buildings = buildings + i.get_name() + ', '
                buildings = buildings[:-2]
                x = f'\nW mieście o kolorze {Street.print_color(street)}: {buildings}. '
            return x

    def __str__(self):
        return f'\nGracz: {self.nick} \nIlość posiadanych pieniedzy: {self.money} zł ' \
               f'\nPosiadane pola kompanii transportowych: {self.print_transport()} ' \
               f'\nPosiadane ulice: {self.print_streets()} '
