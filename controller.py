import game_helpers, curses, random

def move_snake(snake, key, food, win, screen_height, screen_width, snake_color, food_color):
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
        win.addstr(food[0], food[1], "o", curses.color_pair(food_color))

    else:
        # Remove a bit of the snake's tail so it looks like it is moving
        tail = snake.pop()
        win.addch(tail[0], tail[1], " ")

    # Draw the new snake head
    win.addstr(snake[0][0], snake[0][1], "I",  curses.color_pair(snake_color))

    # Show current points
    win.addstr(screen_height - 1, 0, str(len(snake) - 3))

    return [snake, key, food]