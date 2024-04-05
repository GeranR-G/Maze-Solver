from cell import Cell
from time import sleep
import random 

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
        
        self._create_cells()

    def _create_cells(self):
        for i in range(self._num_cols):
            cell_row = []
            for j in range(self._num_rows):
                cell_row.append(Cell(self._win))
            self._cells.append(cell_row)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()
    
    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._cell_size_x * i + self._x1
        y1 = self._cell_size_y * j + self._y1
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()
    
    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            direction_list = []
            if i != 0 and not self._cells[i - 1][j].visited:
                direction_list.append("left")
            if i != self._num_cols - 1 and not self._cells[i + 1][j].visited:
                direction_list.append("right")
            if j != 0 and not self._cells[i][j-1].visited:
                direction_list.append("up")
            if j != self._num_rows - 1 and not self._cells[i][j + 1].visited:
                direction_list.append("down")
            if len(direction_list) == 0:
                self._draw_cell(i, j)
                return
            direction = direction_list[random.randrange(len(direction_list))]
            if direction == "right":
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False
                self._break_walls_r(i + 1, j)
            if direction == "left":
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False
                self._break_walls_r(i - 1, j)
            if direction == "down":
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False
                self._break_walls_r(i, j + 1)
            if direction == "up":
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False
                self._break_walls_r(i, j - 1)
    
    def _reset_cells_visited(self): 
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True
        if i == len(self._cells) - 1 and j == len(self._cells[0]) - 1:
            return True
        for direction in range(4):
            if direction == 0 and i > 0 and not self._cells[i - 1][j].visited and not current_cell.has_left_wall:
                current_cell.draw_move(self._cells[i - 1][j])
                backtrack = self._solve_r(i - 1, j)
                if backtrack:
                    return True
                else:
                    current_cell.draw_move(self._cells[i - 1][j], True)
            if direction == 1 and i < len(self._cells) - 1 and not self._cells[i + 1][j].visited and not current_cell.has_right_wall:
                current_cell.draw_move(self._cells[i + 1][j])
                backtrack = self._solve_r(i + 1, j)
                if backtrack:
                    return True
                else:
                    current_cell.draw_move(self._cells[i + 1][j], True)
            if direction == 2 and j > 0 and not self._cells[i][j - 1].visited and not current_cell.has_top_wall:
                current_cell.draw_move(self._cells[i][j - 1])
                backtrack = self._solve_r(i, j - 1)
                if backtrack:
                    return True
                else:
                    current_cell.draw_move(self._cells[i][j - 1], True)
            if direction == 3 and j < len(self._cells[0]) - 1 and not self._cells[i][j + 1].visited and not current_cell.has_bottom_wall:
                current_cell.draw_move(self._cells[i][j + 1])
                backtrack = self._solve_r(i, j + 1)
                if backtrack:
                    return True
                else:
                    current_cell.draw_move(self._cells[i][j + 1], True)
        return False