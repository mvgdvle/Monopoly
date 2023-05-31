#-*- coding: utf-8 -*-
from property import Property


class PublicTransport(Property):
    @staticmethod
    def count_tax(n, roll):
        if n <= 3:
            t = 4*roll
        else:
            t = 8*roll
        return t

    def __str__(self):
        if self.owner:
            return f'Stoisz na polu: {self.name}. \nWłaścicielem tego pola jest {self.owner.get_nick()}.'
        else:
            return f'Stoisz na polu: {self.name}. \nTo pole nie ma właściciela. ' \
                   f'Koszt zakupu działki wynosi {self.price_field}. '
