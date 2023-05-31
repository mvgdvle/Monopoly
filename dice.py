#-*- coding: utf-8 -*-
from random import randint


class Dice:
    def __init__(self):
        self.sum = 0
        self.count_double = 0

    def roll(self):
        if self.count_double < 3:
            x = randint(1, 6)
            y = randint(1, 6)
            self.sum = x + y
            print(f'\nWrzuciłeś {x} i {y}. Suma oczek wynosi {self.sum}.')
            if x == y:
                self.count_double += 1
                print('Wyrzuciłeś dublet! Przysługuje Ci jeszcze jededen rzut.')
        return self.sum

    def get_count_double(self):
        return self.count_double

    def clean(self):
        self.sum = 0
        self.count_double = 0
