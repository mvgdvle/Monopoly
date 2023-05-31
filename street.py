#-*- coding: utf-8 -*-
from property import Property


class Street(Property):
    def __init__(self, name, position, color, owner=None, price_field=0, tax=0, price_house=0):
        super().__init__(name, position, owner, price_field, tax)
        self.color = color
        self.price_house = price_house
        self.houses = 0
        self.hotels = 0

    def get_price_house(self):
        return self.price_house

    def get_color(self):
        return self.color

    def get_houses(self):
        return self.houses

    def get_hotels(self):
        return self.hotels

    def build_house(self):
        self.houses += 1

    def build_hotel(self):
        self.houses = 0
        self.hotels = 1

    def count_tax(self, full):
        t = self.tax
        if full:
            t += 20

        if self.hotels == 1:
            n = 5
        else:
            n = self.houses

        if self.color == 'pink' or self.color == 'red':
            t = 5*n + t
        elif self.color == 'green' or self.color == 'lime':
            t = 10*n + t
        elif self.color == 'purple' or self.color == 'blue':
            t = 15*n + t
        elif self.color == 'orange' or self.color == 'yellow':
            t = 20*n + t

        return t

    def print_buildings(self):
        x = ''
        if self.houses == 0 and self.hotels == 0:
            x = f'nie stoją żadne budynki. '
        elif self.houses == 1:
            x = f'stoi {self.houses} dom. '
        elif self.houses > 1:
            x = f'stoją {self.houses} domy. '
        elif self.hotels == 1:
            x = f'stoi {self.hotels} hotel. '

        return f'Na tym polu ' + x

    def __str__(self):
        if self.owner:
            x = ''
            if self.houses == 1:
                x = f'Stoi tutaj {self.houses} dom. '
            elif self.houses > 1 or self.houses == 0:
                x = f'Stoi tutaj {self.houses} domów. '
            elif self.hotels == 1:
                x = f'Stoi tutaj {self.hotels} hotel. '
            return f'Stoisz na polu: {self.name}. \nWłaścicielem tego pola jest {self.owner.nick}. ' + x
        else:
            return f'Stoisz na polu: {self.name}. \nTo pole nie ma właściciela. ' \
                   f'Koszt zakupu działki wynosi {self.price_field}. '

    @staticmethod
    def print_color(col):
        if col == 'pink':
            return 'rozowy'
        if col == 'red':
            return 'czerwony'
        if col == 'orange':
            return 'pomaranczowy'
        if col == 'green':
            return 'zielony'
        if col == 'lime':
            return 'limonkowy'
        if col == 'blue':
            return 'niebieski'
        if col == 'purple':
            return 'fioletowy'
