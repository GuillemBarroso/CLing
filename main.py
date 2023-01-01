
# Importing pygame module
import pygame, eztext
from pygame.locals import *
from player import Player

# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# Add caption in the window
pygame.display.set_caption('Player Movement')

WIDTH, HEIGHT = 1300, 900

velocity = 10
direction = "N"
x = 100
y = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

canvas = pygame.display.set_mode((WIDTH, HEIGHT))

image = pygame.image.load(r'player.jpg')
image = pygame.transform.scale(image, (50, 50))

# Define text box
input = eztext.Input(maxlength=6, color=(0,0,255),y=0, prompt='>>> ')
input.focus = True

# Initializing the clock
# Clocks are used to track and
# control the frame-rate of a game
clock = pygame.time.Clock()

# Initialize player object
player = Player(x,y, image)

# Terminal
TERMINAL_WIDTH = WIDTH
TERMINAL_HEIGHT = 160
LINE_HEIGHT = 30
N_DISPLAY_ROWS = 5
terminal_history = []

# sub = canvas.subsurface(input_rect)
terminal = pygame.Surface((TERMINAL_WIDTH, TERMINAL_HEIGHT))
input = eztext.Input(maxlength=80, color=(255, 255, 255),y=TERMINAL_HEIGHT-LINE_HEIGHT, prompt='> ')
input.focus = True

# Creating an Infinite loop
run = True
while run:
    # Set the frame rates to 60 fps
    clock.tick(60)

    canvas.fill((255, 255, 255))

    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    events = pygame.event.get()
    for event in events:
        # Closing the window and program if the
        # type of the event is QUIT
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        # Changing the value of the direction variable
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = "E"
            elif event.key == pygame.K_LEFT:
                direction = "W"
            elif event.key == pygame.K_UP:
                direction = "N"
            elif event.key == pygame.K_DOWN:
                direction = "S"

    player.move()
    player.draw(canvas, direction)

    user_input = input.update(events)

    canvas.blit(terminal, (0, canvas.get_height() - TERMINAL_HEIGHT))
    terminal.fill(BLACK)
    input.draw(terminal)

    # Draw terminal history
    for i_line in range(len(terminal_history)):
        text = input.font.render(terminal_history[-(i_line+1)], True, WHITE)
        text_rect = text.get_rect()
        # text_rect.y = canvas.get_height() - TERMINAL_HEIGHT - LINE_HEIGHT*(i+1)
        text_rect.y = TERMINAL_HEIGHT - LINE_HEIGHT*(i_line+2)
        terminal.blit(text, text_rect)

    if user_input:
        # Add input to the terminal history
        terminal_history.append(f"{input.prompt}{user_input}")

        # Reset input and print
        input.value = ''
        input.draw(terminal)

    # Draws the surface object to the screen.
    pygame.display.update()

