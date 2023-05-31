#-*- coding: utf-8 -*-
from game import Game


def play():
    print('MONOPOLY \n')
    game = Game()
    game.create_pile()
    game.create_board()
    game.add_players()

    player = game.next_player()

    while game.queue.empty() is False:
        game.turn(player)
        player = game.next_player(player)

    winner = game.get_winner()
    print(f'Gratulacje! Grę wygrywa {winner.get_nick()}! \nKoniec gry!')
    return


if __name__ == "__main__":
    play()
