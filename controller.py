import game_helpers, curses, random, time


# Check whether a location is on the screen or out of bounds
def in_bounds(location, screen_height, screen_width):
    if location[0] not in range(0, screen_height) or location[1] not in range(0, screen_width):
        return False
    return True


def move_snake(snake, key, food, obstacles, win, screen_height, screen_width, snake_color, food_color):
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

    # Test whether the snake hits an obstacle or gets out of bounds so the player actually loses
    if new_head in obstacles or not in_bounds(new_head, screen_height, screen_width):
        game_helpers.endgame(len(snake) - 3)

    # Add the head to the snake
    snake.insert(0, new_head)

    # Consume food if the snake hits any
    if snake[0] == food:
        # Unset food and try to generate a new one that's not in an obstacle
        food = None
        while food is None:
            new_food = [
                random.randint(1, screen_height - 1),
                random.randint(1, screen_width - 1)
            ]

            # Set the food if it's not found within the snake
            if not obstacles.__contains__(new_food):
                food = new_food

    else:
        # Remove a bit of the snake's tail so it looks like it is moving
        tail = snake.pop()
        win.addch(tail[0], tail[1], " ")

    # Place the food
    win.addstr(food[0], food[1], "o", curses.color_pair(food_color))

    # Draw the new snake head
    win.addstr(snake[0][0], snake[0][1], "I",  curses.color_pair(snake_color))

    return [snake, key, food]


# AI has to find its way to the food!
# Possibly the most inefficient pathfinding ever!
def pathfinding(facing, location, destination, obstacles, screen_width, screen_height):
    neighbors = []
    new_location = location
    if facing == curses.KEY_UP:
        neighbors.append([new_location[0]-1, new_location[1], curses.KEY_UP])       # top
        neighbors.append([new_location[0], new_location[1]+1, curses.KEY_RIGHT])    # right
        neighbors.append([new_location[0], new_location[1]-1, curses.KEY_LEFT])     # left
    elif facing == curses.KEY_DOWN:
        neighbors.append([new_location[0]+1, new_location[1], curses.KEY_DOWN])     # down
        neighbors.append([new_location[0], new_location[1]+1, curses.KEY_RIGHT])    # right
        neighbors.append([new_location[0], new_location[1]-1, curses.KEY_LEFT])     # left
    elif facing == curses.KEY_LEFT:
        neighbors.append([new_location[0]-1, new_location[1], curses.KEY_UP])       # up
        neighbors.append([new_location[0]+1, new_location[1], curses.KEY_DOWN])     # down
        neighbors.append([new_location[0], new_location[1]-1, curses.KEY_LEFT])     # font
    else:
        neighbors.append([new_location[0]-1, new_location[1], curses.KEY_UP])       # up
        neighbors.append([new_location[0]+1, new_location[1], curses.KEY_DOWN])     # down
        neighbors.append([new_location[0], new_location[1]+1, curses.KEY_RIGHT])    # front

    # Remove all neighbors we cannot go to
    for neighbor in neighbors:
        # Is border?
        if not in_bounds([neighbor[0], neighbor[1]], screen_width, screen_height):
            neighbors.remove(neighbor)
        # Is obstacle snake?
        if [neighbor[0], neighbor[1]] in obstacles:
            neighbors.remove(neighbor)

    # Are we trapped? Check for free neighbors
    if len(neighbors) > 0:
        # Not trapped, go through neighbors again and check which one is closest to our destination
        closest_distance = (screen_width*screen_height)**10  # huge number here
        best_neighbor = []
        for neighbor in neighbors:
            distance_x = abs(neighbor[1] - destination[1])
            distance_y = abs(neighbor[0] - destination[0])
            # Calculate total distance
            distance = distance_x + distance_y
            # Found a closer route? Use it!
            if distance < closest_distance:
                closest_distance = distance
                best_neighbor = neighbor

        return best_neighbor[2]
    else:
        # Trapped
        curses.beep()
        return random.choice([curses.KEY_DOWN, curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT])
