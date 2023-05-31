#-*- coding: utf-8 -*-

class Cards:
    def __init__(self, text, pay_money=0, get_money=0, jail=0, go_to=None):
        if pay_money < 0 or get_money < 0 or jail < 0:
            raise ValueError("Podana liczba musi być nieujemna. ")
        if go_to is not None:
            if go_to < 0:
                raise ValueError("Podana liczba musi być nieujemna. ")
        self.text = text
        self.pay_money = pay_money
        self.get_money = get_money
        self.jail = jail
        self.go_to = go_to

    def get_pay_money(self):
        return self.pay_money

    def get_get_money(self):
        return self.get_money

    def get_jail(self):
        return self.jail

    def get_go_to(self):
        return self.go_to

    def __str__(self):
        x = ''
        if self.pay_money:
            x = f' Zapłać do banku {self.pay_money} zł.'
        if self.get_money:
            x = f' Pobierz od banku {self.get_money} zł.'
        if self.jail == 1:
            x = f' Idź do więznienia na {self.jail} kolejke.'
        if self.jail > 1:
            x = f' Idź do więznienia na {self.jail} kolejki.'
        if self.go_to:
            x = ''

        return f'Wylosowana karta: \n{self.text}' + x
