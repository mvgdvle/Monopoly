import unittest

from game import Game
from board import Board
from player import Player
from public_transport import PublicTransport
from street import Street


class Test(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = Board()
        self.street = Street('BIAŁYSTOK ul.Rynek Kościuszki', 9, 'red', price_field=120, price_house=50, tax=12)
        self.public_transport = PublicTransport('Dworzec Autobusowy', 15, price_field=200)
        self.player = Player('Asia')

    def test_fields(self):
        self.board.create()
        self.game.create_board()
        a = self.board.get_field(9)
        b = self.game.get_field(9)
        c = self.board.get_field(15)
        d = self.game.get_field(15)
        self.assertEqual('BIAŁYSTOK ul.Rynek Kościuszki', a.get_name())
        self.assertEqual('BIAŁYSTOK ul.Rynek Kościuszki', b.get_name())
        self.assertEqual(120, a.get_price_field())
        self.assertEqual(120, b.get_price_field())
        self.assertEqual(32, b.count_tax(True))

        self.assertEqual('Dworzec Autobusowy', c.get_name())
        self.assertEqual('Dworzec Autobusowy', d.get_name())
        self.assertEqual(200, c.get_price_field())
        self.assertEqual(200, d.get_price_field())
        self.assertEqual(20, d.count_tax(3, 5))

    def test_player(self):
        self.player.pay(100)
        self.assertEqual(1400, self.player.get_money())

        self.player.earn(200)
        self.assertEqual(1600, self.player.get_money())

        self.player.go_to_field(37)
        self.assertEqual(37, self.player.get_position())

        self.player.move(10)
        self.assertEqual(7, self.player.get_position())
        self.assertEqual(1800, self.player.get_money())

        self.player.go_to_jail(2)
        self.assertEqual(3, self.player.get_jail_sentence())

        self.assertEqual(False, self.player.is_bankrupt())


if __name__ == "__main__":
    unittest.main()
