import pygame
import random

class Color(object):
    """ store color values in constants to not use harcoded values later
    """
    GRAY = (155, 155, 155)
    BACKGROUND = (120, 120, 120)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARK_GRAY = (100, 100, 100)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    DARK_BLUE = (0, 0, 139)
    MAROON = (128, 0, 0)
    TURQUOISE = (48, 213, 200)

class GameState(object):
    """ changes the game states which are used in the code to fulfill conditions"""
    def __init__(self):
        """sets the states to their beginning values, which can then be chaged later"""
        
        # sets the beginning state of tutorial
        self.tutorial = True

        # sets the beginning state of game
        self.game = False

        # sets the beginning state of game_over
        self.game_over = False

        # sets the beginning state of game_won
        self.game_won = False
    
    def clear_state(self):
        self.tutorial = False
        self.game = False
        self.game_over = False
        self.game_won = False

    def set_state_tutorial(self):
        self.clear_state()
        self.tutorial = True

    def set_state_game(self):
        self.clear_state()
        self.game = True

    def set_state_game_over(self):
        self.clear_state()
        self.game_over = True
    
    def set_state_game_won(self):
        self.clear_state()
        self.game_won = True

class TutorialScreen(object):
    """ displays a tutorial screen in the beginning of the game
    """
    def __init__(self, game):
        """ initialises the class and contains the information for the text displayed in the tutorial screen using self.message so that we don't need to hard code in the draw function
        """
        self.game = game
        # Font for tutorial text
        self.font = pygame.font.Font(None, 30)
        # Color for tutorial text
        self.text_color = Color.BLACK
        self.message = [
            "Minesweeper Tutorial",
            "",
            "Left-click to uncover a tile.",
            "Right-click to flag a tile as a potential mine.",
            "Uncover all tiles except the mines to win.",
            "If you uncover a mine, you lose the game.",
            "The numbers say how many mines are adjacent to the tile cleared",
            "",
            "Press R to restart",
            "Press ESCAPE to quit"
            "",
            "Press SPACE to start the game.",
        ]

    def draw(self):
        """ draws the tutorial screen using the text information from the init function
        """
        self.game.win.fill(Color.BACKGROUND)
        for i, message in enumerate(self.message):
            x = (self.game.win.get_width() // 2)
            y = ( 100 + i * 30)
            text = self.font.render(message, True, self.text_color)
            text_rect = text.get_rect(center=(x, y))
            self.game.win.blit(text, text_rect)

    def handle_events(self, events):
        """ detects a SPACE press and causes the transition from the tutorial state to the game state
        """
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.game.gamestate.set_state_game()

class GameWonScreen(object):
    """ handles all functions needed for the game won screen to be displayed and function properly
    """
    def __init__(self, game):
        """ contains information about the text so that we don't hardcode in draw and it is used in the draw function to pass information
        """
        self.game = game
        self.font = pygame.font.Font(None, 30)
        self.text_color = Color.BLACK
        self.message = [
            "Congratulations! You win!",
            "Would you like to play again?",
            "",
            "Press R to restart",
            "Press ESCAPE to quit"
        ]

    def draw(self):
        """ draws the game won screen using the information in the init function
        """
        for i, message in enumerate(self.message):
            text = self.font.render(message, True, self.text_color)
            text_rect = text.get_rect(center=(self.game.win.get_width() // 2,100 + i * 30))
            self.game.win.blit(text, text_rect)

    def handle_events(self, events):
        """ restarts the program when R is pressed and quits the program when ESCAPE is pressed
        """
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.game.restart()

class ResetButton(object):
    """ displays an image which calls the reset function when clicked
    """

    def __init__(self, game):
        self.game = game
        x = (self.game.win.get_width() // 2)
        y = (self.game.win.get_height() - 30)
        self.image = pygame.transform.scale(pygame.image.load('reset_button.png'), (Tiles.TILE_SIZE, Tiles.TILE_SIZE))
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self):
        """displays the restart button image
        """
        self.game.win.blit(self.image, self.rect)

    def handle_click(self, pos):
        """ calls the restart function when the image is clicked
        """
        if self.rect.collidepoint(pos):
            game.restart()

class GameClock(object):
    """ creates a clock to display your time
    """
    def __init__(self):

        # sets how much time has passed
        self.time_elapsed = 0

        # sets the time you start with
        self.start_time = 0
    
    def clock(self):

        if self.start_time != 0 and not game.gamestate.game_over and not game.gamestate.game_won:
            self.time_elapsed = (pygame.time.get_ticks() - self.start_time) // 1000

        if not game.gamestate.tutorial:
            font = pygame.font.SysFont(None, 36)
            clock_text = font.render(f"Time: {self.time_elapsed}", True, Color.RED)
            game.win.blit(clock_text, (760, 885))

class GameEventHandler(object):
    """ handles game events, only clicks currently"""

    def click(self, events):

        if not game.gamestate.tutorial:
            mouse_button_events = [event for event in events if event.type == pygame.MOUSEBUTTONUP]
            
            for event in mouse_button_events:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    self.left_click(mouse_pos)
                    self.reset_button_click(mouse_pos)
                
                elif event.button == 3:
                    self.right_click(mouse_pos)

    def left_click(self, mouse_pos):
        if not game.gamestate.game_over and game.tiles.collidepoint(mouse_pos):
            if game.gameclock.start_time == 0:
                game.gameclock.start_time = pygame.time.get_ticks()
            game.tiles.uncover(mouse_pos)

    def right_click(self, mouse_pos):
        if not game.gamestate.game_over and game.tiles.collidepoint(mouse_pos):
            game.tiles.flag(mouse_pos)
    
    def reset_button_click(self, mouse_pos):
        game.reset_button.handle_click(mouse_pos)
        
class Game(object):
    """ manages the main game features such as the restart function and the main game loop"""

    def __init__(self):

        # Create the game window
        self.win = pygame.display.set_mode((888, 938))

        # sets the cursor as visible
        pygame.mouse.set_visible(True)

        # sets the look of the cursor
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)

        self.tutorial_screen = TutorialScreen(self)
        self.game_won_screen = GameWonScreen(self)
        self.reset_button = ResetButton(self)
        self.gamestate = GameState()
        self.gameclock = GameClock()
        self.gameeventhandler = GameEventHandler()
        self.tiles = Tiles(self)

    def handle_game_events(self, events):
        if self.gamestate.tutorial:
            self.tutorial_screen.handle_events(events)

        self.gameeventhandler.click(events)

    def draw(self):
        """calls the draw functions required under certain circumstances
        """
        self.win.fill(Color.BACKGROUND)
        self.tiles.draw()
        self.reset_button.draw()

        if self.gamestate.game_won:
            self.win.fill(Color.BACKGROUND)
            self.game_won_screen.draw()
        
        if self.gamestate.tutorial:
            self.tutorial_screen.draw()
        
        if self.gamestate.game:
            self.tiles.draw()
        
        self.gameclock.clock()

    def count_remaining_flags(self):
        """counts the amount of flags compared to be used in the flag function later
        """
        count = 0
        for row in self.tiles.tile_state:
            for tile in row:
                if tile['flagged'] and tile['covered']:
                    count += 1
        return count

    def loop(self):
        """ handles the main game loop
        """
        run = True
        while run:

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()
                    if event.key == pygame.K_ESCAPE:
                        run = False
            self.handle_game_events(events)
            self.draw()

            pygame.display.flip()

    def restart(self):
        """restarts the game to the tutorial state when triggered
        """
        self.tiles = Tiles(self)
        self.gamestate.set_state_game()
        self.gameclock.start_time = 0
        self.gameclock.time_elapsed = 0 

class Tile(object):
    """handles individual tiles
    """
    def create_initial_state(self):
        """sets the tiles to the base values and can be altered later
        """
        state = []
        for row in range(Tiles.num_rows):
            row_state = []
            for column in range(Tiles.num_columns):
                tile = {
                    'covered': True,
                    'mine': False,
                    'flagged': False,
                    'adjacent_mines': 0
                }
                row_state.append(tile)
            state.append(row_state)

        return state

    def calculate_adjacent_mines(self):
        """Calculate and store the number of adjacent mines for each tile
        """
        for row in range(Tiles.num_rows):
            for column in range(Tiles.num_columns):
                tile = self.tile_state[row][column]
                if not tile['mine']:
                    adjacent_mines = 0
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if dx == 0 and dy == 0:
                                continue
                            new_row = row + dx
                            new_column = column + dy
                            if (
                                new_row >= 0 and new_row < Tiles.num_rows
                                and new_column >= 0 and new_column < Tiles.num_columns
                                and self.tile_state[new_row][new_column]['mine']
                            ):
                                adjacent_mines += 1
                    tile['adjacent_mines'] = adjacent_mines

    def place_mines(self):
        """places mines until it reaches the specified number of mines
        """
        num_mines = 40
        while num_mines >0:
            row = random.randint(0, self.num_rows - 1)
            column = random.randint(0, self.num_columns - 1)
            if not self.tile_state[row][column]['mine']:
                self.tile_state[row][column]['mine'] = True
                num_mines -=1

class Tiles(object):
    """handles the game tiles
    """
    num_rows = 16
    num_columns = 16
    TILE_SIZE = 52
    GAP = 3
    BUFFER = 5

    def __init__(self, game):
        """ initialises the Tiles class and sets variables for use later
        """
        self.game = game
        self.tile_state = Tile.create_initial_state(self)
        Tile.place_mines(self)
        Tile.calculate_adjacent_mines(self)
        self.flag_image = pygame.image.load('flag.png')
        self.flag_image = pygame.transform.scale(pygame.image.load('flag.png'), (self.TILE_SIZE, self.TILE_SIZE))
        self.mine_image = pygame.image.load('mine.png')
        self.mine_image = pygame.transform.scale(pygame.image.load('mine.png'), (self.TILE_SIZE, self.TILE_SIZE))
        self.num_flags = 0

    def uncover(self, pos):
        """ uncovers tiles when they are clicked and check for win or lose conditions when the tiles are uncovered
        """
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                x = column * (self.TILE_SIZE + self.GAP) + self.BUFFER
                y = row * (self.TILE_SIZE + self.GAP)
                rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
                if rect.collidepoint(pos):
                    if self.tile_state[row][column]['flagged']:
                        return
                    tile = self.tile_state[row][column]
                    if tile['covered']:
                        tile['covered'] = False
                        if tile['mine']:
                            game.gamestate.set_state_game_over()
                            self.reveal_board()
                        else:
                            count = 0
                            for r in range(row - 1, row + 2):
                                for c in range(column - 1, column + 2):
                                    if (
                                        0 <= r < self.num_rows
                                        and 0 <= c < self.num_columns
                                        and self.tile_state[r][c]['mine']
                                    ):
                                        count += 1
                            tile['adjacent_mines'] = count

                            num_covered_non_mines = sum(
                                sum(1 for tile in row if tile['covered'] and not tile['mine'])
                                for row in self.tile_state
                            )
                            if num_covered_non_mines == 0:
                                game.gamestate.set_state_game_won()
                                self.draw()
                            if tile['adjacent_mines'] == 0:
                                self.clear_adjacent_tiles(row, column)

    def reveal_board(self):
        """reveals the mines on the board, is called when a mine is clicked and the game is over
        """
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                if self.tile_state[row][column]['mine']:
                    self.tile_state[row][column]['covered'] = False

    def flag(self, pos):
        """places flags, is called on right click"""
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                x = column * (self.TILE_SIZE + self.GAP) + self.BUFFER
                y = row * (self.TILE_SIZE + self.GAP)
                rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
                if rect.collidepoint(pos):
                    tile = self.tile_state[row][column]
                    if tile['flagged']:
                        tile['flagged'] = False 
                        self.num_flags -= 1
                    elif tile['covered']:
                        if self.num_flags < 40:
                            tile['flagged'] = True
                            self.num_flags += 1

    def draw(self):
        """ this draws all of the tiles, also draws the updated versions such as when the uncover or flag funtions are called
        """
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                x = column * (self.TILE_SIZE + self.GAP) + self.BUFFER
                y = row * (self.TILE_SIZE + self.GAP)
                tile = self.tile_state[row][column]

                if tile['covered']:
                    color = Color.GRAY
                else:
                    color = Color.BACKGROUND

                pygame.draw.rect(self.game.win, color, (x, y, self.TILE_SIZE, self.TILE_SIZE))

                if not tile['covered']:
                    border_color = (Color.DARK_GRAY)
                    border_width = 1
                    pygame.draw.rect(self.game.win, border_color, (x, y, self.TILE_SIZE, self.TILE_SIZE), border_width)

                if tile['covered']:
                    border_width = 2
                    if column < self.num_columns - 1:
                        pygame.draw.line(self.game.win, Color.WHITE, (x + self.TILE_SIZE, y), (x + self.TILE_SIZE, y + self.TILE_SIZE), border_width)
                    if row < self.num_rows - 1:
                        pygame.draw.line(self.game.win, Color.WHITE, (x, y + self.TILE_SIZE), (x + self.TILE_SIZE, y + self.TILE_SIZE), border_width)
                    pygame.draw.line(self.game.win, Color.DARK_GRAY, (x, y), (x + self.TILE_SIZE, y), border_width)
                    pygame.draw.line(self.game.win, Color.DARK_GRAY, (x, y), (x, y + self.TILE_SIZE), border_width)

                if not tile['covered'] and tile['mine']:
                    self.draw_mine(x, y)

                if not tile['covered'] and not tile['mine'] and tile['adjacent_mines'] >= 1:
                    adjacent_mines = tile['adjacent_mines']
                    font = pygame.font.Font(None, 30)

                    if adjacent_mines == 1:
                        text_color = Color.BLUE
                    elif adjacent_mines == 2:
                        text_color = Color.GREEN
                    elif adjacent_mines == 3:
                        text_color = Color.RED
                    elif adjacent_mines == 4:
                        text_color = Color.DARK_BLUE
                    elif adjacent_mines == 5:
                        text_color = Color.MAROON
                    elif adjacent_mines == 6:
                        text_color = Color.TURQUOISE
                    elif adjacent_mines == 7:
                        text_color = Color.BLACK
                    elif adjacent_mines == 8:
                        text_color = Color.GRAY

                    text = font.render(str(adjacent_mines), True, text_color)
                    text_rect = text.get_rect(center=(x + self.TILE_SIZE // 2, y + self.TILE_SIZE // 2))
                    self.game.win.blit(text, text_rect)

                if tile['flagged']:
                    self.draw_flag(x, y)

        font = pygame.font.SysFont(None, 36)
        flag_text = font.render(f"Flags: {40 - self.num_flags}", True, Color.RED)
        self.game.win.blit(flag_text, (30, 885))

    def draw_flag(self, x, y):
        """draws flags
        """
        self.game.win.blit(self.flag_image, (x, y))

    def draw_mine(self, x, y):
        """draws mines
        """
        self.game.win.blit(self.mine_image, (x, y))

    def collidepoint(self, pos):
        """detects where a tile is and relays to use when detecting clicks
        """
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                x = column * (self.TILE_SIZE + self.GAP) + self.BUFFER
                y = row * (self.TILE_SIZE + self.GAP)
                rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
                if rect.collidepoint(pos):
                    return True
        return False

    def clear_adjacent_tiles(self, row, column):
        """this clears tiles that are adjacent to tiles with 0 adjacent mines
        """
        for r in range(row - 1, row + 2):
            for c in range(column - 1, column + 2):
                if (
                    0 <= r < self.num_rows
                    and 0 <= c < self.num_columns
                    and self.tile_state[r][c]['covered']
                ):
                    self.tile_state[r][c]['covered'] = False
                    self.tile_state[r][c]['flagged'] = False
                    if self.tile_state[r][c]['adjacent_mines'] == 0:
                        self.clear_adjacent_tiles(r, c)

pygame.init()

pygame.display.set_caption("Minesweeper")

# Create the game instance
game = Game()

# Start the game loop
game.loop()

# Quit Pygame
pygame.quit()