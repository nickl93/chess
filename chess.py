from abc import ABCMeta, abstractmethod
#from crayon import *


class Board:
    size = None
    places = list()
    game = None

    def __init__(self, parent_game):
        self.sizeX = 8
        self.sizeY = 8
        self.populate_board()
        self.game = parent_game

    def populate_board(self):
        for x in range(self.sizeX):
            self.places.append(list())
            for y in range(self.sizeY):
                self.places[x].append(None)
        # Pawns
        for x in range(self.sizeX):
            self.places[x][1] = Pawn(x, 1, 1, 0)
            self.places[x][6] = Pawn(x, 6, 0, 1)

        # Kings
        self.places[3][0] = King(3, 0, 1, 0)
        self.places[4][7] = King(4, 7, 0, 1)

        # Queens
        self.places[4][0] = Queen(4, 0, 1, 0)
        self.places[3][7] = Queen(3, 7, 0, 1)

        # Bishops
        self.places[2][0] = Bishop(2, 0, 1, 0)
        self.places[5][0] = Bishop(5, 0, 1, 0)
        self.places[2][7] = Bishop(2, 7, 0, 1)
        self.places[5][7] = Bishop(5, 7, 0, 1)

        # Knights
        self.places[1][0] = Knight(1, 0, 1, 0)
        self.places[6][0] = Knight(6, 0, 1, 0)
        self.places[1][7] = Knight(1, 7, 0, 1)
        self.places[6][7] = Knight(6, 7, 0, 1)

        # Rooks
        self.places[0][0] = Rook(0, 0, 1, 0)
        self.places[7][0] = Rook(7, 0, 1, 0)
        self.places[0][7] = Rook(0, 7, 0, 1)
        self.places[7][7] = Rook(7, 7, 0, 1)

    def display(self):
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                if x != self.sizeX-1:
                    print(self.stringify(self.places[x][y])+"|", end="")
                else:
                    print(self.stringify(self.places[x][y]), end="")
            print("")

    def stringify(self, value):
        if value is None:
            return "_"
        else:
            return str(value)

    def get_piece(self, x, y):
        return self.places[x][y]

    """
    Assumes coordinates have already been verified.
    """
    def attempt_move(self, coordinates):
        piece_x = coordinates[0]
        piece_y = coordinates[1]
        target_x = coordinates[2]
        target_y = coordinates[3]
        piece_to_move = self.get_piece(piece_x, piece_y)
        if piece_to_move is not None:
            if piece_to_move.valid_move(target_x, target_y, game.current_player):
                if self.get_piece(target_x, target_y) is not None:
                    game.players[game.current_player].captured_pieces.append(self.get_piece(target_x, target_y))
                self.places[target_x][target_y] = piece_to_move
                self.places[piece_x][piece_y] = None
                return True
            else:
                print("Is that your piece?")
        return False


class Piece(metaclass=ABCMeta):
    def __init__(self, x, y, owner):
        self.in_play = True
        self.type = None
        self.x = x
        self.y = y
        self.owner = owner

    def __str__(self):
        return self.type+": "+self.in_play

    @abstractmethod
    def valid_move(self, target_x, target_y, current_player):
        return None


class Player:
    def __init__(self, colour):
        self.color = None
        self.captured_pieces = list()


class Pawn(Piece):
    def __init__(self, x, y, direction, owner):
        self.x = x
        self.y = y
        self.type = "Pawn"
        self.direction = direction
        self.owner = owner

    def valid_move(self, target_x, target_y, current_player):
        return current_player == self.owner

    def __str__(self):
        return "P"


class King(Piece):
    def __init__(self, x, y, direction, owner):
        self.x = x
        self.y = y
        self.type = "King"
        self.direction = direction
        self.owner = owner

    def valid_move(self, target_x, target_y, current_player):
        return current_player == self.owner

    def __str__(self):
        return "K"


class Queen(Piece):
    def __init__(self, x, y, direction, owner):
        self.x = x
        self.y = y
        self.type = "Queen"
        self.direction = direction
        self.owner = owner

    def valid_move(self, target_x, target_y, current_player):
        return current_player == self.owner

    def __str__(self):
        return "Q"


class Bishop(Piece):
    def __init__(self, x, y, direction, owner):
        self.x = x
        self.y = y
        self.type = "Bishop"
        self.direction = direction
        self.owner = owner

    def valid_move(self, target_x, target_y, current_player):
        return current_player == self.owner

    def __str__(self):
        return "B"


class Knight(Piece):
    def __init__(self, x, y, direction, owner):
        self.x = x
        self.y = y
        self.type = "Knight"
        self.direction = direction
        self.owner = owner

    def valid_move(self, target_x, target_y, current_player):
        return current_player == self.owner

    def __str__(self):
        return "H"


class Rook(Piece):
    def __init__(self, x, y, direction, owner):
        self.x = x
        self.y = y
        self.type = "Rook"
        self.direction = direction
        self.owner = owner

    def valid_move(self, target_x, target_y, current_player):
        return current_player == self.owner

    def __str__(self):
        return "R"


class Game:
    def __init__(self):
        self.board = Board(self)
        self.current_player = 0
        self.is_over = False
        player1 = Player("White")
        player2 = Player("Black")
        self.players = [player1, player2]

    def move(self):
        instruction = input("Player {} to Move: ".format(self.current_player))
        if instruction == 'q':
            exit(0)
        if len(instruction) == 7:
            # okay to parse
            try:
                coordinates = [int(x) for x in instruction.split(" ")]
            except ValueError:
                return False
            if len(coordinates) == 4 and self.coordinates_okay(coordinates):
                move_result = self.board.attempt_move(coordinates)
                if move_result is True:
                    self.current_player = (self.current_player + 1) % 2
                    return coordinates
        print("Invalid Move")
        return None

    def coordinates_okay(self, coordinates):
        for i in coordinates:
            if i < 0 or i > self.board.sizeX-1:
                return False
        return True


if __name__ == "__main__":
    game = Game()
    game.board.display()
    while game.is_over is not True:
        move = game.move()
        game.board.display()

