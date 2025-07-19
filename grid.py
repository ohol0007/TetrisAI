class Grid:
    def __init__(self, width = 10, height =10):
        self.width = width
        self.height = self.height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
    
    def is_valid_position(self,piece):
        for row, col in piece.get_cells():
           if row >=self.height or col <0 or col >=self.width:
               return False
           if row >=0 and self.grid[row][col] is not None:
               return False
        return True

    def lock_position(self, piece):
        for row, col in piece.get_cells():
            if row >=0: 
                self.grid[row][col] = piece.colour
    
    def clear_line(self):
        new_grid = [row for row in self.grid if not all(row)]
        lines_cleared = self.height -len(new_grid)
        while new_grid < self.height:
            new_grid.insert(0, [None]*self.grid)
        self.grid = new_grid
        return lines_cleared