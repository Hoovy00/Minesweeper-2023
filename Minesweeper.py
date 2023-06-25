import pygame
import random

# DHB: it is somewhat unnatural to see pygame used before being initialised. Also, it is not cool to execute code in multiple parts
# DHB: of the file. Define your classes and functions first, then execute your code.
# Create the game window
win = pygame.display.set_mode((888, 938))
pygame.display.set_caption("Minesweeper")

# DHB: all classes in python should contain class comments, rather than preceeding the class with a comment like this
# Define the Color class to store color values
class Color(object):
    # DHB: it is not great to skip the parenthesis around a tuple, even though it is legal. If you would e.g. copy this constant
    # DHB: elsewhere, such as in a function parameter list, then it would change from being a tuple to being multiple parameters 
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

# DHB: incorrect approach to commenting a class
class TutorialScreen(object): # creates the tutorial screen
    def __init__(self):
        # DHB: missing function comments in this, and most other functions in this file.
        # DHB: comments should be in the preceeding line, not as a trailing comment
        # DHB: also, when parameters are not obvious, it is wise to call them by name rather than position
        # DHB: e.g. Font(file_path=None, size=30) 
        self.font = pygame.font.Font(None, 30) # Font for tutorial text
        # DHB: excellent choice to use named constants instead of hardcoded values
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
        # DHB: using win as a global variable is a bad practice. It is better to send
        # DHB: things like this into constructor args and store in member variables.
        # DHB: When you start unit testing, global variables are a class of hell
        # DHB: also, pretty sure you should only fill the window with the background color in the top-level draw function
        win.fill(Color.BACKGROUND)
        for i, instruction in enumerate(self.instructions):
            text = self.font.render(instruction, True, self.text_color)
            text_rect = text.get_rect(center=(win.get_width() // 2, 100 + i * 30))
            win.blit(text, text_rect)
        # DHB: I'm pretty certain only the top-level draw function should call display.update 
        pygame.display.update() # Update the display

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Transition to the game state
                    # DHB: game is a separate object. one should never modify the contents of member variables
                    # DHB: directly on another object. Instead call a function such as "set_state".
                    game.state = "game"

class GameWonScreen(object): # creates the victory screen
    def __init__(self):
        self.font = pygame.font.Font(None, 30) # Font for win text
        self.text_color = Color.BLACK # Color for win text
        # DHB: instructions is not a reasonable variable name here
        self.instructions = [
            "Congratulations! You win!",
            "Would you like to play again?",
            "",
            "Press R to restart"
        ]

    def draw(self): # draws the win screen
        # DHB: see comments elsewhere regarding fill and update
        win.fill(Color.BACKGROUND)
        for i, instruction in enumerate(self.instructions):
            text = self.font.render(instruction, True, self.text_color)
            # DHB: generally its wise to not put too much in the same line. Here, I'd move the calculations to separate variables
            # DHB: e.g.
            #      x = win.get_width() // 2
            #      y = 100 + i * 30
            # DHB: while the other way works just fine, working in this fashion leads to bugs
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
        # DHB: initialising a library should not be done in an object initialiser like this. Move it to file scope, or move everything on file scope into this class (which would be a bad choice)
        pygame.init()
        # DHB: you're not really use the game_objects system... use it, or remove it  
        self.game_objects = []
        # DHB: it is important to comment all member variables, explaining what they are used for and what they can contain, just like all functions and classes.
        self.tiles = None
        self.game_over = False
        self.game_won = False
        self.game_won_message_printed = False
        # DHB: for a state variable like this, it's especially important to ensure that the valid states are well defined. You could for example use a game state
        # DHB: enumeration class, similar to the color class, to define the valid status
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

        # DHB: I wonder if this 'game_won_message_printed' flag is a good idea. Draw loops usually draw everything
        # DHB: in every frame, but I imagine this will only make the message be drawn in one frame 
        if self.game_won and not self.game_won_message_printed:
            self.game_won_screen.draw()
            self.game_won_message_printed = True

        self.reset_button.draw()

    def get_remaining_flags(self):
        # DHB: it would be wise to name this count_remaining_flags, rather than get_remaining_flags, as get implies that the state already
        # DHB: was calculated. This function is heavy for a 'get' method.
        count = 0
        for row in self.tiles.tile_state:
            for tile in row:
                if tile['flagged'] and tile['covered']:
                    count += 1
        return count

    def loop(self):
        run = True
        while run:

            # DHB: use a helper function for keyboard events, rather than mixing it into the main loop
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
                # DHB: doing the mouse handling directly in the main loop is pretty yucky... please move to a helper function

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
                # DHB: the main loop logic and the draw code should be separated, by moving all draw calls into self.draw()
                self.tiles.draw()
                self.draw()

            if self.game_won and not self.game_won_message_printed:
                self.game_won_screen.draw()
                self.state = "game_won"

            if self.state == "game_over" or self.state == "game_won":
                self.game_won_screen.handle_events(events)

            # DHB: this is ugly in and of itself. Add comment or move to helper function
            if self.start_time != 0 and not self.game_over and not self.game_won:
                self.time_elapsed = (pygame.time.get_ticks() - self.start_time) // 1000

            if self.state != "tutorial":
            # Render and blit the clock text onto the screen
                # DHB: the comment above was incorreclty indented
                font = pygame.font.SysFont(None, 36)
                clock_text = font.render(f"Time: {self.time_elapsed}", True, Color.RED)
                win.blit(clock_text, (760, 885)) # Display the clock text at (10, 10) position on the screen

            # DHB; the end of the main loop should likely just call self.draw, which should do the background fill, call all the sub-draw-functions, and then flip
            pygame.display.flip()

    def restart(self): # restarts the game
        # DHB: the __init__ function should call the restart function, rather than duplicating the logic of setting up the state in that function and here
        self.tiles = Tiles() # Reinitialize the Tiles object
        self.game_over = False
        self.game_won = False
        self.game_won_message_printed = False
        self.state = "tutorial" # Reset the game state
        self.start_time = 0
        self.time_elapsed = 0
        # DHB: this adds self.tiles as a game object every time the game is restarted, which is unnecessary
        self.add_game_object(self.tiles) # Add the Tiles object back to the game_objects list

# Define the Field class to represent the play area
class Field(object):
    def draw(self):
        # DHB: I'm pretty certain that this is dead code, i.e. it is never called by anything.
        win.fill(Color.BACKGROUND)

# Define the Tiles class to handle the game tiles
class Tiles(object):
    # DHB: constants should always be in upper case
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
        # DHB: advanced exercise, please make a generator function that enumerates all tiles in the grid, returning tuples of (row, column, tile), and
        # DHB: use that function instead for this pattern in this class.
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                tile = self.tile_state[row][column]
                if not tile['mine']:
                    adjacent_mines = 0
                    # DHB: also please make a generator that enumerates all adjacent tiles of a tile, and use that instead for this pattern
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
                # DHB: please refactor so that each tile is a separate Tile instance, and move tile state into that class instead of using
                # DHB: a dictionary
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
                            # DHB: again, no changing directly the state variables of another object. That should be done in member functions of the object.
                            game.game_over = True
                            # calls self.reveal_board on game over
                            self.reveal_board()
                        else:
                            # DHB: this should be separated into a helper function that updates the adjacent mines for a tile
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
                # DHB: note that hit-testing a tile should also be moved to the Tile class
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
                # DHB: we should ask each Tile to draw itself, rather than do it here
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
        # DHB: this class is only being use as a side-effect of initialising it. Either use it properly, or remove it, and move the init code elsewhere
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
