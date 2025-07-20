import numpy as np
from game import Game
from pieces import tetrominos

class TetrisEnv:
    def __init__(self):
        self.game = Game()
        self.previous_lines_cleared = 0
        self.piece_locked = False

    def reset(self):
        self.game = Game()
        self.previous_lines_cleared = 0
        self.piece_locked = False
        return self.get_state()

    def step(self, action):
        self.piece_locked = False
        prev_score = self.game.score
        prev_board = [row[:] for row in self.game.grid.board]

        if action == 0:
            self.game.move_current_piece(-1)
        elif action == 1:
            self.game.move_current_piece(1)
        elif action == 2:
            self.game.rotate_current_piece()
        elif action == 3:
            # Drop piece
            while not self.game.game_over:
                prev_y = self.game.current_piece.y
                self.game.update()
                if self.game.current_piece.y == prev_y:
                    break
            self.piece_locked = True
        self.game.update()

        reward = self.get_reward(prev_score)
        next_state = self.get_state()
        done = self.game.game_over

        return next_state, reward, done, {}

    def get_reward(self, prev_score):
        reward = 0

        # 1. Lines cleared (based on score diff)
        score_diff = self.game.score - prev_score
        lines_cleared = score_diff // 100
        reward += lines_cleared ** 2  # Encourage Tetris (4 lines at once)

        # 2. Game over penalty
        if self.game.game_over:
            reward -= 20

        # 3. Holes penalty
        holes = self.count_holes(self.game.grid.board)
        reward -= 0.5 * holes

        # 4. Bumpiness penalty
        bumpiness, _ = self.get_bumpiness_and_height(self.game.grid.board)
        reward -= 0.1 * bumpiness

        # 5. Piece lock reward
        if self.piece_locked:
            reward += 0.1

        return reward

    def get_state(self):
        board = np.array(self.game.grid.board).flatten() / 1.0  # normalize to 0 or 1

        # Normalize piece type (0 to 6)
        piece_types = list(tetrominos.keys())
        current_piece_type = piece_types.index(self.game.current_piece.shape) / 6.0
        next_piece_type = piece_types.index(self.game.next_piece.shape) / 6.0

        # Normalize piece position
        x = self.game.current_piece.x / self.game.grid.width
        y = self.game.current_piece.y / self.game.grid.height

        return np.concatenate((board, [current_piece_type, x, y, next_piece_type]))

    def count_holes(self, board):
        holes = 0
        for col in zip(*board):  # Transpose to columns
            filled = False
            for cell in col:
                if cell:
                    filled = True
                elif filled:
                    holes += 1
        return holes

    def get_bumpiness_and_height(self, board):
        heights = []
        for col in zip(*board):
            col_height = 0
            for i, cell in enumerate(col):
                if cell:
                    col_height = len(board) - i
                    break
            heights.append(col_height)

        bumpiness = sum(abs(heights[i] - heights[i + 1]) for i in range(len(heights) - 1))
        total_height = sum(heights)
        return bumpiness, total_height
