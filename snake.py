# SNAKE game
# based on https://github.com/engineer-man/youtube/blob/master/015/snake.py

import curses, random
import game_helpers, controller

# config
food_char = "o"
snake_char = "I"
travelled_char = " "

# Initial setup
scr = curses.initscr()
game_helpers.init_highscore()
curses.start_color()
curses.noecho()
curses.cbreak()
curses.curs_set(0)

# Color of the snake
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
# Color of the food
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)

# Define the size of the screen
screen_height, screen_width = scr.getmaxyx()

# Create a window for the game to be played in
win = curses.newwin(screen_height, screen_width, 0, 0)
win.keypad(True)
win.timeout(100)

# Starting position of the snake
player_snake_x = int(screen_width / 4)
player_snake_y = int(screen_height / 2)

# Set 3 snake tiles to begin with
player_snake = [
    [player_snake_y, player_snake_x],
    [player_snake_y, player_snake_x-1],
    [player_snake_y, player_snake_y-2]
]

# Position of the food and initial placing
food = [int(screen_height/2), int(screen_width/2)]
win.addstr(food[0], food[1], food_char, curses.color_pair(2))

key = curses.KEY_RIGHT


# Game must be in a loop so it continues to run
while True:
    # First of all, handle the player
    next_key = win.getch()

    # If something is pressed, change the key!
    if next_key != -1:
        key = next_key

    # Move and update our data
    result = controller.move_snake(player_snake, key, food, win, screen_height, screen_width, 1, 2)
    player_snake = result[0]
    key = result[1]
    food = result[2]