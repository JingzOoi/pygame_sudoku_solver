import pygame
import sudoku


class Grid(sudoku.Grid):
    """A space on a Sudoku board. Holds a value unique to row, column, and box."""

    SIZE = 50
    COLOR_BACKGROUND = (255, 255, 255)
    COLOR_TEXT = (0, 0, 0)

    def __init__(self, pos: tuple, value: int = None):
        super().__init__(pos, value)
        self.SURFACE = pygame.Surface((self.SIZE, self.SIZE))
        self.coordinates = ((self.col-1)*self.SIZE, (self.row-1)*self.SIZE)

    def draw(self, surface: pygame.Surface):
        """Blits value onto self, then is blitted to surface (Board)"""
        font = pygame.font.SysFont('Consolas', Grid.SIZE // 2)
        text = font.render(f"{self.value if self.value else ' '}", True, self.COLOR_TEXT)
        text_rect = text.get_rect()
        text_rect.centerx = self.SURFACE.get_rect().centerx
        text_rect.centery = self.SURFACE.get_rect().centery
        self.SURFACE.fill(self.COLOR_BACKGROUND)
        self.SURFACE.blit(text, text_rect)
        surface.blit(self.SURFACE, self.coordinates)


class Board(sudoku.Board):
    """A collection of arranged Grids."""

    WIDTH, HEIGHT = Grid.SIZE * 9, Grid.SIZE * 9
    SIZE = (WIDTH, HEIGHT)
    COORDINATES = (Grid.SIZE, Grid.SIZE)
    TOP = Grid.SIZE
    LEFT = Grid.SIZE
    BOTTOM = TOP + HEIGHT
    RIGHT = LEFT + WIDTH
    WIDTH_LINE = 2
    COLOR_LINE = (0, 0, 0)

    def __init__(self):
        super().__init__([Grid((i, j)) for j in range(1, 10) for i in range(1, 10)])
        self.SURFACE = pygame.Surface((self.WIDTH + self.WIDTH_LINE, self.HEIGHT + self.WIDTH_LINE))
        self.vertical_lines = [((i * Grid.SIZE, 0), (i * Grid.SIZE, self.HEIGHT)) for i in range(10)]
        self.horizontal_lines = [((0, i * Grid.SIZE), (self.WIDTH, i * Grid.SIZE)) for i in range(10)]

    def collide(self, pos: tuple) -> bool:
        """Checks if coordinates (from window) given is within the board."""
        x, y = pos
        return self.LEFT <= x <= self.RIGHT and self.TOP <= y <= self.BOTTOM

    def collide_grid(self, pos: tuple) -> Grid:
        """Returns the grid placed in the coordinates given."""
        x, y = pos
        board_pos = (x // Grid.SIZE, y // Grid.SIZE)
        for grid in self.grids:
            if grid.position == board_pos:
                return grid
        else:
            raise GridNotFoundError("No grid found in specified mouse position!")

    def draw(self, surface: pygame.Surface):
        """Blits grids onto self, then is blitted to surface (Window)"""
        for grid in self.grids:
            grid.draw(self.SURFACE)

        # basic lines between grids
        for vertical_line, horizontal_line in zip(self.vertical_lines, self.horizontal_lines):
            pygame.draw.line(self.SURFACE, self.COLOR_LINE, vertical_line[0], vertical_line[1], self.WIDTH_LINE)
            pygame.draw.line(self.SURFACE, self.COLOR_LINE, horizontal_line[0], horizontal_line[1], self.WIDTH_LINE)

        # thicker lines between boxes
        for vertical_line in self.vertical_lines[::3]:
            pygame.draw.line(self.SURFACE, self.COLOR_LINE, vertical_line[0], vertical_line[1], 2 * self.WIDTH_LINE)

        for horizontal_line in self.horizontal_lines[::3]:
            pygame.draw.line(self.SURFACE, self.COLOR_LINE, horizontal_line[0], horizontal_line[1], 2 * self.WIDTH_LINE)

        surface.blit(self.SURFACE, self.COORDINATES)


class Game(sudoku.Game):
    """An instance of a Sudoku game. Holds the logic to solving the game."""

    def __init__(self):
        super().__init__(Board())
        self.current_value = 1

    @property
    def candidates(self):
        candidate_dict = {}
        for i in range(1, 10):
            candidate_dict[i] = Grid((0, 0), i)
            candidate_dict[i].coordinates = (candidate_dict[i].value * Grid.SIZE, self.board.BOTTOM + Grid.SIZE // 2)
        return candidate_dict

    def change_current_value(self, num: int):
        """Changes the current value held by the mouse button."""
        self.current_value = num if 0 < num < 10 else 1

    def clear_grid(self):
        """Clears all grids on the board."""
        for grid in self.board:
            grid.value = None

    def draw(self, surface: pygame.Surface):
        """Draws game elements and board."""
        self.board.draw(surface)
        for g_index in list(self.candidates):
            g = self.candidates[g_index]
            g.draw(surface)
        c_value_grid = self.candidates[self.current_value]
        rect = pygame.Rect(c_value_grid.coordinates[0], c_value_grid.coordinates[1], Grid.SIZE, Grid.SIZE)
        pygame.draw.rect(surface, Board.COLOR_LINE, rect, 3)


class Window:
    """An instance of a running application. Handles events."""

    FPS = 30
    FPSCLOCK = pygame.time.Clock()
    WIDTH, HEIGHT = Board.WIDTH + 2 * Grid.SIZE, Board.HEIGHT + 3 * Grid.SIZE

    def __init__(self):
        pygame.init()
        self.SIZE = (self.WIDTH, self.HEIGHT)
        self.RENDERER = Renderer(self.SIZE)
        self.game = Game()

    def handle_events(self) -> bool:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                return False

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                # checks if mouse clicked in board area
                if self.game.board.collide(mouse_pos):
                    grid = self.game.board.collide_grid(mouse_pos)
                    if event.button == 1:
                        grid.value = self.game.current_value
                    elif event.button == 3:
                        grid.value = None

            if keys[pygame.K_SPACE]:
                self.game.clear_grid()

            if keys[pygame.K_RETURN]:
                self.game.solve()

            if keys[pygame.K_0]:
                self.game.current_value = None
            elif keys[pygame.K_1]:
                self.game.current_value = 1
            elif keys[pygame.K_2]:
                self.game.current_value = 2
            elif keys[pygame.K_3]:
                self.game.current_value = 3
            elif keys[pygame.K_4]:
                self.game.current_value = 4
            elif keys[pygame.K_5]:
                self.game.current_value = 5
            elif keys[pygame.K_6]:
                self.game.current_value = 6
            elif keys[pygame.K_7]:
                self.game.current_value = 7
            elif keys[pygame.K_8]:
                self.game.current_value = 8
            elif keys[pygame.K_9]:
                self.game.current_value = 9

        return True

    def update(self) -> bool:
        with self.RENDERER:
            self.RENDERER.draw_game(self.game)
            return self.handle_events()


class Renderer:
    """An instance of a renderer. Draws everything on the Window."""

    COLOR_BACKGROUND = (180, 180, 180)

    def __init__(self, size: tuple):
        self.SIZE = size
        self.WIDTH, self.HEIGHT = self.SIZE
        self.DISPLAY = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Sudoku w/Pygame by JZ")

    def __enter__(self):
        self.DISPLAY.fill(self.COLOR_BACKGROUND)

    def __exit__(self, exc_type, exc_value, exc_trace):
        pygame.display.update()

    def draw_game(self, game):
        game.draw(self.DISPLAY)


if __name__ == "__main__":
    win = Window()
    while win.update():
        win.FPSCLOCK.tick(win.FPS)


class GridNotFoundError(Exception):
    """Called when grid is not found in the board."""
