import random
from grid import Grid
from pieces import Piece, tetrominos

class Game:
    def __init__(self):
        self.grid = Grid(width=10, height= 20)
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.score = 0
        self.game_over = False
    
    def get_new_piece(self):
        return Piece(random.choice(list(tetrominos.keys())))
    
    def spawn_piece(self):
        self.current_piece = self.next_piece
        self.next_piece= self.get_new_piece()
        if not self.grid.is_valid_position(self.current_piece):
            self.game_over = True
    
    def update(self):
        """Moves piece down. Locks and spawns new one if it hits."""
        self.current_piece.move(0, 1)
        if not self.grid.is_valid_position(self.current_piece):
            self.current_piece.move(0, -1)
            self.grid.lock_position(self.current_piece)
            lines = self.grid.clear_line()
            self.score += lines * 100
            self.spawn_piece()
    
    def move_current_piece(self, dx):
        self.current_piece.move(dx, 0)
        if not self.grid.is_valid_position(self.current_piece):
            self.current_piece.move(-dx, 0)
    
    def rotate_current_piece(self):
        self.current_piece.rotate()
        if not self.grid.is_valid_position(self.current_piece):
            self.current_piece.rotate(-1)