# SNAKE game
# based on https://github.com/engineer-man/youtube/blob/master/015/snake.py

import curses
import game_helpers, controller

# Initial setup
scr = curses.initscr()
game_helpers.init_highscore()
curses.start_color()
curses.noecho()
curses.cbreak()
curses.curs_set(0)

# Color of the snake // player
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
# Color of the food // player
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
# Color of the snake // AI
curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_CYAN)
# Color of the food // AI
curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW)

# Define the size of the screen
screen_height, screen_width = scr.getmaxyx()

# Create a window for the game to be played in
win = curses.newwin(screen_height, screen_width, 0, 0)
win.keypad(True)
win.timeout(100)

# Starting position of the players' snake
player_snake_x = 5
player_snake_y = 5

# Starting position of the AI's snake
ai_snake_x = screen_width - 5
ai_snake_y = 5

# Set 3 snake tiles to begin with
player_snake = [
    [player_snake_y, player_snake_x],
    [player_snake_y - 1, player_snake_x],
    [player_snake_y - 2, player_snake_y]
]

ai_snake = [
    [ai_snake_y, ai_snake_x],
    [ai_snake_y - 1, ai_snake_x],
    [ai_snake_y - 2, ai_snake_x]
]

# Position of the food and initial placing
player_food = [int(screen_height/2), int(screen_width/2)]
win.addstr(player_food[0], player_food[1], "o", curses.color_pair(2))

ai_food = [int(screen_height/2)-2, int(screen_width/2)]
win.addstr(ai_food[0], ai_food[1], "o", curses.color_pair(4))

key = curses.KEY_DOWN
ai_key = curses.KEY_DOWN

# Game must be in a loop so it continues to run
while True:
    # First of all, handle the player
    next_key = win.getch()

    # If something is pressed, change the key!
    if next_key != -1:
        key = next_key

    # Move and update our data
    obstacles = ai_snake + player_snake + ai_food
    result = controller.move_snake(player_snake, key, player_food, obstacles, win, screen_height, screen_width, 1, 2)
    player_snake = result[0]
    key = result[1]
    player_food = result[2]

    # Control the AI
    # Do not hit any snake
    obstacles = ai_snake + player_snake + player_food
    # Find out where to move next
    ai_key = controller.pathfinding(ai_key, [ai_snake[0][0], ai_snake[0][1]], ai_food, obstacles, screen_height, screen_width)
    # Do the action
    ai_result = controller.move_snake(ai_snake, ai_key, ai_food, obstacles, win, screen_height, screen_width, 3, 4)
    ai_snake = ai_result[0]
    ai_key = ai_result[1]
    ai_food = ai_result[2]
