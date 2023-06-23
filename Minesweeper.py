import pygame
import random

# Create the game window
win = pygame.display.set_mode((888, 938))
pygame.display.set_caption("Minesweeper")

# Define the Color class to store color values
class Color(object):
    GRAY = 155, 155, 155
    BACKGROUND = 120, 120, 120
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    DARK_GRAY = 100, 100, 100
    RED = 255, 0, 0
    BLUE = 0, 0, 255
    GREEN = 0, 255, 0
    DARK_BLUE = 0, 0, 139
    MAROON = 128, 0, 0
    TURQUOISE = 48, 213, 200

class TutorialScreen(object): # creates the tutorial screen
    def __init__(self):
        self.font = pygame.font.Font(None, 30) # Font for tutorial text
        self.text_color = Color.BLACK # Color for tutorial text
        self.instructions = [
            "Minesweeper Tutorial",
            "",
            "Left-click to uncover a tile.",
            "Right-click to flag a tile as a potential mine.",
            "Uncover all tiles except the mines to win.",
            "If you uncover a mine, you lose the game.",
            "The numbers say how many mines are adjacent to the tile cleared",
            "",
            "Press R to restart",
            "",
            "Press SPACE to start the game.",
        ]

    def draw(self): # draws the tutorial screen
        win.fill(Color.BACKGROUND)
        for i, instruction in enumerate(self.instructions):
            text = self.font.render(instruction, True, self.text_color)
            text_rect = text.get_rect(center=(win.get_width() // 2, 100 + i * 30))
            win.blit(text, text_rect)

        pygame.display.update() # Update the display

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Transition to the game state
                    game.state = "game"

class GameWonScreen(object): # creates the victory screen
    def __init__(self):
        self.font = pygame.font.Font(None, 30) # Font for win text
        self.text_color = Color.BLACK # Color for win text
        self.instructions = [
            "Congratulations! You win!",
            "Would you like to play again?",
            "",
            "Press R to restart"
        ]

    def draw(self): # draws the win screen
        win.fill(Color.BACKGROUND)
        for i, instruction in enumerate(self.instructions):
            text = self.font.render(instruction, True, self.text_color)
            text_rect = text.get_rect(center=(win.get_width() // 2, 100 + i * 30))
            win.blit(text, text_rect)

        pygame.display.update() # Update the display

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # restart to the game state
                    game.restart()

class ResetButton(object): # creates the reset button
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('reset_button.png'), (Tiles.TILE_SIZE, Tiles.TILE_SIZE))
        self.rect = self.image.get_rect(center=(win.get_width() // 2, win.get_height() - 30))

    def draw(self):
        win.blit(self.image, self.rect)

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            game.restart()


# Define the Game class to manage the game loop and game objects
class Game(object):
    def __init__(self):
        pygame.init()
        self.game_objects = []
        self.tiles = None
        self.game_over = False
        self.game_won = False
        self.game_won_message_printed = False
        self.state = "tutorial"
        self.clock = pygame.time.Clock()
        self.time_elapsed = 0
        self.start_time = 0

        self.tutorial_screen = TutorialScreen()
        self.game_won_screen = GameWonScreen()
        self.reset_button = ResetButton()

    def add_game_objects(self, *list_of_game_objects, **dict_of_game_objects):
        for game_object in list_of_game_objects:
            self.add_game_object(game_object)
        for game_object_id, game_object in dict_of_game_objects.items():
            self.add_game_object(game_object)

    def add_game_object(self, game_object):
        self.game_objects.append(game_object)
        if isinstance(game_object, Tiles):
            self.tiles = game_object

    def get_game_objects_with_attribute(self, attribute_name):
        return [game_object for game_object in self.game_objects if hasattr(game_object, attribute_name)]

    def draw(self): # calls all of the draw functions
        
        if self.game_over:
            self.tiles.draw()
        
        if self.game_won and not self.game_won_message_printed:
            self.game_won_screen.draw()
            self.game_won_message_printed = True

        self.reset_button.draw()

    def get_remaining_flags(self):
        count = 0
        for row in self.tiles.tile_state:
            for tile in row:
                if tile['flagged'] and tile['covered']:
                    count += 1
        return count

    def loop(self):
        run = True
        while run:

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()

            if self.state == "tutorial":
                self.tutorial_screen.handle_events(events)
                self.tutorial_screen.draw()
            elif self.state == "game": # detects clicks
                win.fill(Color.BACKGROUND) # Clear the screen with the background color

                mouse_button_events = [event for event in events if event.type == pygame.MOUSEBUTTONUP]
                for event in mouse_button_events:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if not self.game_over and self.tiles.collidepoint(mouse_pos):
                            if self.start_time == 0:
                                self.start_time = pygame.time.get_ticks() # Start the timer on the first tile uncover
                            self.tiles.uncover(mouse_pos)
                        self.reset_button.handle_click(mouse_pos)
                    elif event.button == 3:
                        mouse_pos = pygame.mouse.get_pos()
                        if not self.game_over and self.tiles.collidepoint(mouse_pos):
                            self.tiles.flag(mouse_pos)

                self.tiles.draw()
                self.draw()

            if self.game_won and not self.game_won_message_printed:
                self.game_won_screen.draw()
                self.state = "game_won"

            if self.state == "game_over" or self.state == "game_won":
                self.game_won_screen.handle_events(events)

            if self.start_time != 0 and not self.game_over and not self.game_won:
                self.time_elapsed = (pygame.time.get_ticks() - self.start_time) // 1000

            if self.state != "tutorial":
            # Render and blit the clock text onto the screen
                font = pygame.font.SysFont(None, 36)
                clock_text = font.render(f"Time: {self.time_elapsed}", True, Color.RED)
                win.blit(clock_text, (760, 885)) # Display the clock text at (10, 10) position on the screen

            pygame.display.flip()

    def restart(self): # restarts the game
        self.tiles = Tiles() # Reinitialize the Tiles object
        self.game_over = False
        self.game_won = False
        self.game_won_message_printed = False
        self.state = "tutorial" # Reset the game state
        self.start_time = 0
        self.time_elapsed = 0

        self.add_game_object(self.tiles) # Add the Tiles object back to the game_objects list

# Define the Field class to represent the play area
class Field(object):
    def draw(self):
        win.fill(Color.BACKGROUND)

# Define the Tiles class to handle the game tiles
class Tiles(object):
    num_rows = 16
    num_columns = 16
    TILE_SIZE = 52
    GAP = 3
    BUFFER = 5

    def __init__(self):
        self.tile_state = self.create_initial_state()
        self.place_mines()
        self.calculate_adjacent_mines()
        self.flag_image = pygame.image.load('flag.png')
        self.flag_image = pygame.transform.scale(pygame.image.load('flag.png'), (self.TILE_SIZE, self.TILE_SIZE))
        self.mine_image = pygame.image.load('mine.png')
        self.mine_image = pygame.transform.scale(pygame.image.load('mine.png'), (self.TILE_SIZE, self.TILE_SIZE))
        self.num_flags = 0

    def create_initial_state(self):
        state = []
        for row in range(self.num_rows):
            row_state = []
            for column in range(self.num_columns):
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
        # Calculate and store the number of adjacent mines for each tile
        for row in range(self.num_rows):
            for column in range(self.num_columns):
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
                                new_row >= 0 and new_row < self.num_rows
                                and new_column >= 0 and new_column < self.num_columns
                                and self.tile_state[new_row][new_column]['mine']
                            ):
                                adjacent_mines += 1
                    tile['adjacent_mines'] = adjacent_mines

    def place_mines(self):
        num_mines = 40 # Number of mines to place
        while num_mines >0:
            row = random.randint(0, self.num_rows - 1)
            column = random.randint(0, self.num_columns - 1)
            if not self.tile_state[row][column]['mine']:
                self.tile_state[row][column]['mine'] = True
                num_mines -=1

    def uncover(self, pos):
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
                            game.game_over = True
                            # calls self.reveal_board on game over
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

                            # Check win condition
                            num_covered_non_mines = sum(
                                sum(1 for tile in row if tile['covered'] and not tile['mine'])
                                for row in self.tile_state
                            )
                            if num_covered_non_mines == 0:
                                game.game_won = True
                            if tile['adjacent_mines'] == 0:
                                self.clear_adjacent_tiles(row, column) # Call clear_adjacent_tiles for tiles with zero adjacent mines

    def reveal_board(self): # reveals the mines on the board
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                if self.tile_state[row][column]['mine']:
                    self.tile_state[row][column]['covered'] = False

    def flag(self, pos): # creates flags
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                x = column * (self.TILE_SIZE + self.GAP) + self.BUFFER
                y = row * (self.TILE_SIZE + self.GAP)
                rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
                if rect.collidepoint(pos):
                    tile = self.tile_state[row][column]
                    if tile['flagged']:
                        tile['flagged'] = False # Unflag the tile
                        self.num_flags -= 1 # Decrement the flag count
                    elif tile['covered']:
                        if self.num_flags < 40: # Maximum number of flags is 40 (equal to the number of mines)
                            tile['flagged'] = True # Flag the tile
                            self.num_flags += 1 # Increment the flag count

    def draw(self): # draws the game elments
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                x = column * (self.TILE_SIZE + self.GAP) + self.BUFFER
                y = row * (self.TILE_SIZE + self.GAP)
                tile = self.tile_state[row][column]

                if tile['covered']:
                    color = Color.GRAY
                else:
                    color = Color.BACKGROUND

                pygame.draw.rect(win, color, (x, y, self.TILE_SIZE, self.TILE_SIZE))

                if not tile['covered']:
                    border_color = (Color.DARK_GRAY)
                    border_width = 1
                    pygame.draw.rect(win, border_color, (x, y, self.TILE_SIZE, self.TILE_SIZE), border_width)

                if tile['covered']:
                    border_width = 2
                    if column < self.num_columns - 1:
                        pygame.draw.line(win, Color.WHITE, (x + self.TILE_SIZE, y), (x + self.TILE_SIZE, y + self.TILE_SIZE), border_width)
                    if row < self.num_rows - 1:
                        pygame.draw.line(win, Color.WHITE, (x, y + self.TILE_SIZE), (x + self.TILE_SIZE, y + self.TILE_SIZE), border_width)
                    pygame.draw.line(win, Color.DARK_GRAY, (x, y), (x + self.TILE_SIZE, y), border_width)
                    pygame.draw.line(win, Color.DARK_GRAY, (x, y), (x, y + self.TILE_SIZE), border_width)

                if not tile['covered'] and tile['mine']:
                    self.draw_mine(x, y)

                if not tile['covered'] and not tile['mine'] and tile['adjacent_mines'] >= 1:
                    # Shows the number of mines adjacent to uncovered
                    adjacent_mines = tile['adjacent_mines']
                    font = pygame.font.Font(None, 30)

                    # Set the color based on the number of adjacent mines
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
                    win.blit(text, text_rect)

                if tile['flagged']:
                    self.draw_flag(x, y)

        font = pygame.font.SysFont(None, 36)
        flag_text = font.render(f"Flags: {40 - self.num_flags}", True, Color.RED)
        win.blit(flag_text, (30, 885)) # Display the flag count at (30, 885) position on the screen

    def draw_flag(self, x, y):
        win.blit(self.flag_image, (x, y))

    def draw_mine(self, x, y):
        win.blit(self.mine_image, (x, y))

    def collidepoint(self, pos): # detects where a tile is and relays to detect clicks
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                x = column * (self.TILE_SIZE + self.GAP) + self.BUFFER
                y = row * (self.TILE_SIZE + self.GAP)
                rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
                if rect.collidepoint(pos):
                    return True
        return False

    def clear_adjacent_tiles(self, row, column): # clears tiles adjacent to 0 tiles
        for r in range(row - 1, row + 2):
            for c in range(column - 1, column + 2):
                if (
                    0 <= r < self.num_rows
                    and 0 <= c < self.num_columns
                    and self.tile_state[r][c]['covered']
                    and not self.tile_state[r][c]['flagged']
                ):
                    self.tile_state[r][c]['covered'] = False
                    if self.tile_state[r][c]['adjacent_mines'] == 0:
                        self.clear_adjacent_tiles(r, c) # Recursively clear adjacent tiles

# Define the Mouse class to handle mouse-related functionality
class Mouse(object):
    def __init__(self):
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        
# Create the game instance
game = Game()

# Add game objects to the game instance
game.add_game_objects(
    field=Field(),
    tiles=Tiles(),
    mouse=Mouse(),
)

# Start the game loop
game.loop()

# Quit Pygame
pygame.quit()