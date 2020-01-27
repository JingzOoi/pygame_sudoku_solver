class Grid:
    """A space on a Sudoku board. Holds a value unique to row, column, and box."""

    def __init__(self, pos: tuple, value: int = None):
        self.col, self.row = pos
        self.position = (self.col, self.row)
        self.box = self.parse_box()
        self.value = value

    def __repr__(self) -> str:
        return f"Grid(position={self.position}, box={self.box}, value={self.value})"

    def parse_box(self) -> tuple:
        """Returns box (3 grid by 3 grid section) based on the position on board."""
        box_h = self.col // 3 if self.col % 3 == 0 else self.col // 3 + 1
        box_v = self.row // 3 if self.row % 3 == 0 else self.row // 3 + 1
        return (box_h, box_v)


class Board:
    """A collection of arranged Grids."""

    def __init__(self, grids: list):
        self.grids = grids

    def __getitem__(self, num) -> Grid:
        """Allows slicing."""
        return self.grids[num]


class Game:
    """An instance of a Sudoku game. Holds the logic to solving the game."""

    def __init__(self, board: Board):
        self.board = board

    def check_empty(self):
        """Looks for the next empty grid in the board, starting from row."""
        empty_grids = [grid for grid in self.board if grid.value is None]
        return empty_grids[0] if len(empty_grids) > 0 else None

    def check_valid(self, grid: Grid, num) -> bool:
        """Checks if a number can be fit into a grid without collision."""
        if not grid.value:
            same_row = [g.value for g in self.board if g.row == grid.row]
            if num in same_row:
                return False
            same_column = [g.value for g in self.board if g.col == grid.col]
            if num in same_column:
                return False
            same_box = [g.value for g in self.board if g.box == grid.box]
            if num in same_box:
                return False
            return True
        return False

    def solve(self) -> bool:
        """Solves the game."""
        # looks for the next empty grid on the board.
        next_empty = self.check_empty()
        if not next_empty:
            # no empty grid is found == board is completed.
            return True
        else:
            # there is an empty grid found. Try for numbers.
            for i in range(1, 10):
                if self.check_valid(next_empty, i) is True:
                    # if number can be placed in grid, solve the grid using current settings.
                    next_empty.value = i
                    if self.solve():
                        return True
                    else:
                        # some sort of collision is found. Revert to None and continue with for loop.
                        next_empty.value = None
            else:
                # Exhausted all numbers == some error in the previous grids.
                return False
