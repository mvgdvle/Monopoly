#-*- coding: utf-8 -*-
from board import Board
from queue import Queue
from player import Player
from cards import Cards
from dice import Dice
from random import choice
from public_transport import PublicTransport
from street import Street
from property import Property


class Game:
    def __init__(self):
        self.board = Board()
        self.players = {}
        self.queue = Queue()
        self.pile = self.create_pile()
        self.dice = Dice()
        self.winner = None

    def add_players(self):
        t = True
        number = 0
        while t:
            number = int(input('Podaj liczbę graczy (od 2 do 6): '))
            if 2 > number or number > 6:
                print('Nieprawidłowa liczba graczy. Podaj cyfrę od 2 do 6. ')
            else:
                t = False

        for i in range(number):
            is_different = True
            while is_different:
                nick = input(f"Podaj nick gracza {i+1}: ")
                if nick in self.players:
                    print('Gracz o takim nicku już istnieje. Proszę podać inny nick.')
                else:
                    is_different = False
                    new_player = Player(nick)
                    self.players[nick] = new_player
                    self.queue.put(new_player)

    def next_player(self, player=None):
        if player:
            if player.is_bankrupt() is False:
                self.queue.put(player)

            next_player = self.queue.get()
            if self.queue.empty():
                self.winner = next_player
                return next_player
            else:
                check = True
                while check:
                    x = str(input('\nKliknij "c" aby podać kostkę dalej: '))
                    if x == 'c':
                        check = False
                return next_player
        else:
            return self.queue.get()

    def get_winner(self):
        return self.winner

    def create_board(self):
        self.board.create()

    def get_field(self, position):
        return self.board.get_field(position)

    def get_card(self):
        n = len(self.pile)
        if n == 0:
            self.create_pile()
        return choice(self.pile)

    def turn(self, player):
        print(f'\n------------------------------------------------------------\n \nKostką rzuca: {str(player)}')
        self.roll(player, 1)
        self.dice.clean()
        if player.get_jail_sentence() == 0 and player.is_bankrupt() is False:
            self.build(player)
        if player.get_jail_sentence() > 0:
            player.take_jail_sentence()

    def roll(self, player, n):
        if player.get_jail_sentence() == 0:
            steps = self.dice.roll()
            d = self.dice.get_count_double()
            if d == n and d < 3:
                player.move(steps)
                self.visit_field(player, steps, n)
                n += 1
                if player.is_bankrupt() is False:
                    self.roll(player, n)
            elif d != n and d < 3:
                player.move(steps)
                self.visit_field(player, steps, n)
            elif d == 3:
                print('Wyrzuciłeś dublet po raz trzeci. Idziesz do więzienia na jedną kolejkę. ')
                player.go_to_jail(1)

        else:
            s = player.get_jail_sentence()
            x = ''
            if s == 1:
                x = 'kolejkę'
            elif s > 1:
                x = 'kolejki'
            print(f'\nJesteś w więzieniu na {s} {x}. Nie możesz wykonać rzutu. ')

    def visit_field(self, player, steps=0, n=1):
        i = player.get_position()
        current_field = self.get_field(i)
        budget = player.get_money()
        print(current_field)
        if isinstance(current_field, Property):
            owner = current_field.get_owner()
            if owner is None:
                price = current_field.get_price_field()
                if price <= budget:
                    print('\nTwoje możliwe ruchy: \n1. Kupuję to pole. \n2. Nie kupuję tego pola. ')
                    check = True
                    while check:
                        option = int(input('Jaki ruch chcesz wykonać? (podaj odpowiednią cyfrę): '))
                        if option == 1:
                            player.buy_property(current_field)
                            check = False
                        elif option == 2:
                            check = False
                        else:
                            print('Nieprawidłowy wybór. Podaj odpowidnią cyfrę jeszcze raz. ')
                else:
                    print('\nBrak możliwych ruchów. ')
            elif owner == player:
                return
            else:
                if owner.get_jail_sentence() > 0:
                    print('Właściciel tego pola jest w więzieniu, więc jesteś zwolniony z opłaty. ')
                else:
                    tax = 0
                    if isinstance(current_field, Street):
                        tax = owner.get_tax_st(current_field)
                    elif isinstance(current_field, PublicTransport):
                        tax = owner.get_tax_pt(current_field, steps)
                    print(f'\nMusisz zapłacić właścicielowi czynsz w wysokości {tax} zł. ')
                    if tax > budget:
                        print('\nTwój budżet nie wystarcza na opłacenie czynszu. Oddajesz wszystkie swoje '
                              'nieruchomości właścicielowi pola. ')
                        player.change_owner_street(owner)
                        player.go_bankrupt()
                    else:
                        player.pay(tax)
                        owner.earn(tax)

        elif current_field.get_is_jail():
            player.go_to_jail(1)
            print('\nTrafiłeś do więzienia na jedną kolejkę. ')

        elif current_field.get_is_parking():
            print('\nMożesz tu bezpiecznie odpocząć bez uszczerbku na działalności. ')

        elif current_field.get_is_chance():
            print('\nLosujesz kartę szans. ')
            chance = self.get_card()
            print(chance)
            if chance.get_pay_money() > 0:
                x = chance.get_pay_money()
                if x > budget:
                    print('\nMasz za mało środków na koncie, nie jesteś w stanie zapłacić takiej sumy. '
                          'Oddajesz wszystkie nieruchomości do banku.')
                    player.change_owner_street(None)
                    player.change_owner_public_transport(None)
                    player.go_bankrupt()
                else:
                    player.pay(x)
            elif chance.get_get_money() > 0:
                x = chance.get_get_money()
                player.earn(x)
            elif chance.get_jail() > 0:
                x = chance.get_jail()
                player.go_to_jail(x)
            elif chance.get_go_to():
                x = chance.get_go_to()
                player.go_to_field(x)
                self.visit_field(player, steps, n)
                if x == 0:
                    player.earn(200)

    @staticmethod
    def build(player):
        again = True
        while again:
            properties1 = []
            properties2 = []
            for lst in player.get_streets().values():
                for street in lst:
                    price = street.get_price_house()
                    budget = player.get_money()
                    houses = street.get_houses()
                    hotels = street.get_hotels()
                    if price <= budget and houses < 4 and hotels == 0:
                        properties1.append(street)
                    elif price <= budget and houses == 4 and hotels == 0:
                        properties2.append(street)

            if len(properties1) == 0 and len(properties2) == 0:
                again = False
            else:
                print('\nMożesz wybudować: ')
                i = 0
                if len(properties1) > 0:
                    for st in properties1:
                        i += 1
                        print(f'{i}. Dom na polu {st.get_name()} za {st.get_price_house()} zł. {st.print_buildings()}')
                if len(properties2) > 0:
                    for st in properties2:
                        i += 1
                        print(
                            f'{i}. Hotel na polu {st.get_name()} za {st.get_price_house()} zł. {st.print_buildings()}')

                print(
                    f'\nTwój budżet wynosi {player.get_money()}. Chcesz postawić któryś z budynków? \n1. Tak \n2. Nie')
                check = True
                while check:
                    o = int(input('Wybierz odpowiednią cyfrę: '))
                    if o == 1:
                        check2 = True
                        while check2:
                            option = int(input('Na którym polu chesz wybudować budynek? Wybierz odpowiednią cyfrę: '))
                            if 1 <= option <= len(properties1) + len(properties2):
                                if option <= len(properties1):
                                    field = properties1[option - 1]
                                    player.build_house(field)
                                else:
                                    field = properties2[option - len(properties1) - 1]
                                    player.build_hotel(field)
                                check2 = False
                            else:
                                print('Nieprawidłowy wybór. Podaj odpowidnią cyfrę jeszcze raz. ')
                        check = False
                    elif o == 2:
                        again = False
                        check = False
                    else:
                        print('Nieprawidłowy wybór. Podaj odpowidnią cyfrę jeszcze raz. ')

    @staticmethod
    def create_pile():
        pile = list()
        pile.append(Cards('Postanowiłeś zainwestować w akcje spółki lokalnego Monopolisty. ', get_money=25))
        pile.append(Cards('Dostosowując się do oferty konkurencji, wyremontowałeś wynajomwane lokale. '
                          'Teraz będziesz mógł zwiększyć czynsz. ', get_money=50))
        pile.append(Cards('Niektórym spanie na pieniądzach juą nie wystarcza - '
                          'Twój biznes rozwija się tak prężnie, że możesz się w nich kąpać! ', get_money=50))
        pile.append(Cards('Idź na pole Baldachówka (Rzeszów). ', go_to=3))
        pile.append(Cards('Wyrokiem sądu zostałeś ukarany grzywną za ujawnienie powiązań biznesowych '
                          'z firmą Twojego brata blizniaka.', pay_money=25))
        pile.append(Cards('Kto bogatemu zabroni? Tylko urząd skarbowy! '
                          'Uchylanie się od płacenia podatków będzie Cię teraz sporo kosztowało! ', pay_money=75))
        pile.append(Cards('Idź na pole Nożownicza (Wrocław). ', go_to=27))
        pile.append(Cards('Idź na pole start. ', go_to=0))
        pile.append(Cards('Idź na pole start. ', go_to=0))
        pile.append(Cards('Idź na pole start. ', go_to=0))
        pile.append(Cards('Idź na pole start. ', go_to=0))
        pile.append(Cards('W poszukiwaniu dodatkowych źródeł dochodu próbowałeś zmonopolizować Słońce jako '
                          'źrodło energii. Niestety projekt ten okazał się być tylko snem. ', pay_money=50))
        pile.append(Cards('Dostałeś cynk, że inwestycja w składaowanie odpadów może się bardzo opłacić. '
                          'No cóż... pieniądze przecież nie śmierdzą. ', get_money=75))
        pile.append(Cards('Innowacyjne rozwiązanie konkurencji mogło realnie wpłynąć na zmniejszenie Twoich dochodów. '
                          'Nie pozostało Ci nic innego jak wykupić patent i definitywnie pogrzebać pomysł. ',
                          get_money=75))
        pile.append(Cards('Cudze chwalicie, swego nie znacie - pojawienie się na rynku zagranicznego kapitału znacząco '
                          'zmniejszyło Twoje zyski. ', pay_money=25))
        pile.append(Cards('Pieniądz nie jest dobrym doradcą! Zawyżenie czynszu w nieruchomościach nie uszło uwadze '
                          'urzędowi antymonopolowemu. ', jail=1))
        pile.append(Cards('Gdy nie wiadomo, o co chodzi, to chodzi o pieniądze! Dzięki Twoim znajomościom '
                          'udało Ci się uniknąć zapłacenia podatku od nieruchomości. ', get_money=25))
        pile.append(Cards('Idź na pole Port ', go_to=12))
        pile.append(Cards('Idź na Dworzec Kolejowy ', go_to=5))
        pile.append(Cards('Chytry dwa razy płaci! Chcąc zaoszczędzić probowałeś przekupić urzędnika - '
                          'niestety nieskutecznie! ', jail=2))
        pile.append(Cards('Trzeba byc mądrym, żeby robić pieniądze - zamiast do urzędu skarbowego, '
                          'wysłałeś niedopłatę do urzędu antymonopolowego. Posądzenie o przekupstwa '
                          'będzie Cię dużo kosztować! ', pay_money=50))
        pile.append(Cards('Co za dużo, to niezdrowo! Próba wygrania wszystkich okolicznych przetargów '
                          'skończyła się kontrolą z urzędu.', pay_money=75))
        pile.append(Cards('Złożony przez Ciebie wniosek o dofinansowanie został rozpatrzony pozytywnie. '
                          'Twój biznes nabiera rozpędu! ', get_money=25))
        pile.append(Cards('Czas to pieniądz - okazało się jednak, ze poświęciłeś go zbyt mało na prawidłowe '
                          'przygotowanie zeznania podatkowego. Urząd znalazł kilka uchybień, które znacząco '
                          'odchudzą Twój portfel. ', pay_money=75))
        pile.append(Cards('Idż na pole Dworzec Autobusowy', go_to=15))
        pile.append(Cards('Wygrałeś rozprawe sądowa! Otrzymane odszkodowanie znacznie polepszy funkcjonowanie '
                          'Twojego biznesu. ', get_money=75))
        pile.append(Cards('Grosz do grosza, a będzie kokosza. Czynione na terenie całego kraju inwestycje '
                          'zaczynają przynosić realne zyski. ', get_money=50))
        pile.append(Cards('Podobno pieniądze nie leżą na ulicy... chyba tak, gdyż znalezli się najemcy '
                          'na wszystkie posiadane przez Ciebie nieruchomości. ', get_money=50))
        pile.append(Cards('Biednemu zawsze wiatr w oczy - dziłający w Twojej okolicy monopoliści '
                          'sztucznie zaniżają ceny, powodując u Ciebie realne straty. ', pay_money=50))
        return pile
