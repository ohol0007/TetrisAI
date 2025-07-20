import numpy as np
from game import Game

class TetrisEnv:
    def __init__(self):
        self.game = Game()
    
    def reset(self):
        self.game = Game()
        return self.get_state()
    
    def step(self, action):
        if action ==0:
            self.game.move_current_piece(-1)
        elif action ==1:
            self.game.move_current_piece(1)
        elif action ==2:
            self.game.rotate_current_piece()
        elif action ==3:
            while not self.game.game_over:
                prev_y = self.game.current_piece.y
                self.game.update()
                if self.game.current_piece.y ==prev_y:
                    break
        self.game.update()
        next_state = self.get_state()
        get_reward = self.get_reward()