#-*- coding: utf-8 -*-


class Field:
    def __init__(self, name, position, is_chance=False, is_jail=False, is_parking=False):
        self.name = name
        self.position = position
        self.is_chance = is_chance
        self.is_jail = is_jail
        self.is_parking = is_parking

    def get_position(self):
        return self.position

    def get_name(self):
        return self.name

    def get_is_chance(self):
        return self.is_chance

    def get_is_jail(self):
        return self.is_jail

    def get_is_parking(self):
        return self.is_parking

    def __str__(self):
        if self.is_chance:
            return 'Stoisz na polu: Szansa. '
        if self.is_jail:
            return 'Stoisz na polu: Więzienie. '
        if self.is_parking:
            return 'Stoisz na polu: Parking. '
        if self.position == 0:
            return 'Stoisz na polu: Start. '
