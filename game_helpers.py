import curses


def init_highscore():
    highscore_file = open("highscore.txt", "w+")
    if not highscore_file.read():
        highscore_file.write("0")
    highscore_file.close()


def endgame(points):
    curses.endwin()
    print("The game has ended! - " + str(points) + " points!")
    # Did the user beat the highscore?
    highscore = get_highscore()
    if points > highscore:
        print("You beat the highscore which was previously " + str(highscore) + " points!")
        # Save the new highscore
        highscore_file = open("highscore.txt", "w")
        highscore_file.write(str(points))
        highscore_file.close()
    quit()


def get_highscore():
    highscore_file = open("highscore.txt", "r")
    highscore = int(highscore_file.read())
    highscore_file.close()
    return highscore
