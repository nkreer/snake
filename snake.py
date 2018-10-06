# SNAKE game
# based on https://github.com/engineer-man/youtube/blob/master/015/snake.py

import curses, random
import game_helpers

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
snake_x = int(screen_width / 4)
snake_y = int(screen_height / 2)

# Set 3 snake tiles to begin with
snake = [
    [snake_y, snake_x],
    [snake_y, snake_x-1],
    [snake_y, snake_y-2]
]

# Position of the food and initial placing
food = [int(screen_height/2), int(screen_width/2)]
win.addstr(food[0], food[1], food_char, curses.color_pair(2))

key = curses.KEY_RIGHT

# Game must be in a loop so it continues to run
while True:
    next_key = win.getch()

    # If something is pressed, change the key!
    if next_key != -1:
        key = next_key

    # Set the new head of the snake depending on the direction its going
    new_head = [snake[0][0], snake[0][1]]

    if key == curses.KEY_DOWN:
        new_head[0] += 1
    elif key == curses.KEY_UP:
        new_head[0] -= 1
    elif key == curses.KEY_LEFT:
        new_head[1] -= 1
    else:
        new_head[1] += 1

    # Test whether the snake hits itself or gets out of bounds so the player actually loses
    if new_head in snake or new_head[0] not in range(0, screen_height) or new_head[1] not in range(0, screen_width):
        game_helpers.endgame(len(snake) - 3)
        break

    # Add the head to the snake
    snake.insert(0, new_head)

    # Consume food if the snake hits any
    if snake[0] == food:
        # Unset food and try to generate a new one that's not within the snake
        food = None
        while food is None:
            new_food = [
                random.randint(1, screen_height - 1),
                random.randint(1, screen_width - 1)
            ]

            # Set the food if it's not found within the snake
            if not snake.__contains__(new_food):
                food = new_food

        # Place the food
        win.addstr(food[0], food[1], food_char, curses.color_pair(2))

    else:
        # Remove a bit of the snake's tail so it looks like it is moving
        tail = snake.pop()
        win.addch(tail[0], tail[1], travelled_char)

    # Draw the new snake head
    win.addstr(snake[0][0], snake[0][1], snake_char,  curses.color_pair(1))

    # Show current points
    win.addstr(screen_height - 1, 0, str(len(snake) - 3))
