from abc import ABCMeta, abstractmethod
import crayons


class Piece(metaclass=ABCMeta):
    def __init__(self, x, y, direction, owner):
        self.in_play = True
        self.type = None
        self.repr = None
        self.x = x
        self.y = y
        self.owner = owner
        self.direction = direction
        self.moves = 0

    def colored_str(self):
        if self.owner == 1:
            return crayons.white(self.repr, bold=True)  # White is black?
        else:
            return crayons.black(self.repr, bold=True)  # Black is white?

    @abstractmethod
    def valid_move(self, target_x, target_y, current_player):
        if current_player != self.owner:
            print("Is that your piece?")
            return False
        if self.x == target_x and self.y == target_y:
            return False


class Player:
    def __init__(self, colour):
        self.colour = colour
        self.captured_pieces = list()


class Pawn(Piece):
    def __init__(self, x, y, direction, owner):
        super().__init__(x, y, direction, owner)
        self.type = "Pawn"
        self.repr = "P"

    def valid_move(self, target_x, target_y, current_player):
        super().valid_move(target_x, target_y, current_player)
        if target_y != self.y + self.direction and \
                (target_y != self.y + 2 * self.direction and self.moves == 0):
            return False
        if target_x > self.x + 1 or target_x < self.x - 1:
            return False
        # Straight move
        return True


class King(Piece):
    def __init__(self, x, y, direction, owner):
        super().__init__(x, y, direction, owner)
        self.type = "King"
        self.repr = "K"

    def valid_move(self, target_x, target_y, current_player):
        super().valid_move(target_x, target_y, current_player)
        if self.x - 1 <= target_x <= self.x + 1 and self.y - 1 <= target_y <= self.y + 1:
            return True
        else:
            # Check for castling
            return False


class Queen(Piece):
    def __init__(self, x, y, direction, owner):
        super().__init__(x, y, direction, owner)
        self.type = "Queen"
        self.repr = "Q"

    def valid_move(self, target_x, target_y, current_player):
        super().valid_move(target_x, target_y, current_player)
        if (target_x - self.x) % (target_y - self.y) == 0 or \
            target_y == self.y or \
                target_x == self.x:
            return True
        else:
            return False


class Bishop(Piece):
    def __init__(self, x, y, direction, owner):
        super().__init__(x, y, direction, owner)
        self.type = "Bishop"
        self.repr = 'B'

    def valid_move(self, target_x, target_y, current_player):
        super().valid_move(target_x, target_y, current_player)
        if (target_x - self.x) % (target_y - self.y) == 0:
            return True
        else:
            return False


class Knight(Piece):
    def __init__(self, x, y, direction, owner):
        super().__init__(x, y, direction, owner)
        self.type = "Knight"
        self.repr = "K"

    def valid_move(self, target_x, target_y, current_player):
        super().valid_move(target_x, target_y, current_player)
        if (abs(target_x - self.x) == 2 and abs(target_y - self.y) == 3) or \
                (abs(target_x - self.x) == 3 and abs(target_y - self.y) == 3):
            return True
        else:
            return False


class Rook(Piece):
    def __init__(self, x, y, direction, owner):
        super().__init__(x, y, direction, owner)
        self.type = "Rook"
        self.repr = "R"

    def valid_move(self, target_x, target_y, current_player):
        super().valid_move(target_x, target_y, current_player)
        if target_y == self.y or target_x == self.x:
            return True
        else:
            return False


class Board:

    def __init__(self, parent_game):
        self.places = list()
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
            self.places[x][6] = Pawn(x, 6, -1, 1)

        # Kings
        self.places[3][0] = King(3, 0, 1, 0)
        self.places[4][7] = King(4, 7, -1, 1)

        # Queens
        self.places[4][0] = Queen(4, 0, 1, 0)
        self.places[3][7] = Queen(3, 7, -1, 1)

        # Bishops
        self.places[2][0] = Bishop(2, 0, 1, 0)
        self.places[5][0] = Bishop(5, 0, 1, 0)
        self.places[2][7] = Bishop(2, 7, -1, 1)
        self.places[5][7] = Bishop(5, 7, -1, 1)

        # Knights
        self.places[1][0] = Knight(1, 0, 1, 0)
        self.places[6][0] = Knight(6, 0, 1, 0)
        self.places[1][7] = Knight(1, 7, -1, 1)
        self.places[6][7] = Knight(6, 7, -1, 1)

        # Rooks
        self.places[0][0] = Rook(0, 0, 1, 0)
        self.places[7][0] = Rook(7, 0, 1, 0)
        self.places[0][7] = Rook(0, 7, -1, 1)
        self.places[7][7] = Rook(7, 7, -1, 1)

    def display(self):
        print("  ", end="")
        for w in range(self.sizeX):
            print(str(w) + " ", end="")
        print()
        for y in range(self.sizeY):
            print(str(y) + " ", end="")
            for x in range(self.sizeX):
                if x == self.sizeX - 1:
                    print(self.stringify(self.places[x][y]), end="")
                else:
                    print(self.stringify(self.places[x][y]), end="")
                    print('|', end="")
            print("")

    @staticmethod
    def stringify(value):
        if value is None:
            return "_"
        else:
            return value.colored_str()

    def get_piece(self, x, y):
        return self.places[x][y]

    def attempt_move(self, coordinates):
        piece_x = coordinates[0]
        piece_y = coordinates[1]
        target_x = coordinates[2]
        target_y = coordinates[3]
        piece_to_move = self.get_piece(piece_x, piece_y)
        if piece_to_move is not None:
            if piece_to_move.valid_move(target_x, target_y, self.game.current_player):
                captured_piece = self.get_piece(target_x, target_y)
                if captured_piece is not None and captured_piece.owner != game.current_player:
                    captured_piece.in_play = False
                    game.players[game.current_player].captured_pieces.append(captured_piece)
                    print("Player {} captured Player {}'s {} at ({}, {})".format(game.current_player,
                                                                                 game.current_player,
                                                                                 captured_piece.type,
                                                                                 target_x,
                                                                                 target_y))
                    if self.get_piece(target_x, target_y).type == "King":
                        self.game.is_over = True
                    self.places[target_x][target_y] = piece_to_move
                    self.places[target_x][target_y].moves += 1
                    self.places[piece_x][piece_y] = None
                    return True
        return False


class Game:
    def __init__(self):
        self.board = Board(self)
        self.current_player = 0
        self.is_over = False
        player1 = Player("White")
        player2 = Player("Black")
        self.players = [player1, player2]

    def move(self):
        instruction = input("{} to Move: ".format(self.players[self.current_player].colour))
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
        print("Invalid Move - Usage: <Current X> <Current Y> <Target X> <Target Y>")
        return None

    def coordinates_okay(self, coordinates):
        for i in coordinates:
            if i < 0 or i > self.board.sizeX - 1:
                return False
        return True


if __name__ == "__main__":
    game = Game()
    game.board.display()
    while game.is_over is not True:
        move = game.move()
        game.board.display()
