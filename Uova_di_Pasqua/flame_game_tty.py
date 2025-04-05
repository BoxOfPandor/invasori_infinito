import curses
import time
import random
import threading

WIDTH = 40
HEIGHT = 20

player_x = WIDTH // 2
player_y = HEIGHT - 2

flames = []

score = 0

FLAME_COLORS = [1, 2, 3]

INITIAL_FLAME_SPAWN_RATE = 0.1
FLAME_SPAWN_INCREASE_RATE = 0.01

MAX_FLAMES = 12

lock = threading.Lock()

MAX_SCORE_WIDTH = 10


def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)


def draw_screen(stdscr):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if x == player_x and y == player_y:
                stdscr.addch(y, x, '@')
            elif any(fx == x and fy == y for fx, fy in flames):
                color = random.choice(FLAME_COLORS)
                stdscr.addch(y, x, 'D', curses.color_pair(color))
            else:
                stdscr.addch(y, x, '.')
    # Truncate score display if it exceeds maximum width
    score_display = f"Score: {score}"[:MAX_SCORE_WIDTH]
    stdscr.addstr(HEIGHT, 0, score_display)
    stdscr.refresh()


def move_player(direction):
    global player_x, player_y
    with lock:
        if direction == 'left' and player_x > 0:
            player_x -= 1
        elif direction == 'right' and player_x < WIDTH - 1:
            player_x += 1
        elif direction == 'up' and player_y > 0:
            player_y -= 1
        elif direction == 'down' and player_y < HEIGHT - 1:
            player_y += 1


def update_flames():
    global flames, score
    with lock:
        new_flames = []
        for fx, fy in flames:
            if fy < HEIGHT - 1:
                new_flames.append((fx, fy + 1))
            else:
                score += 1
        flames = new_flames

        # Increase flame spawn rate over time
        flame_spawn_rate = INITIAL_FLAME_SPAWN_RATE + FLAME_SPAWN_INCREASE_RATE * score
        if len(flames) < MAX_FLAMES and random.random() < flame_spawn_rate:
            flames.append((random.randint(0, WIDTH - 1), 0))


def check_collision():
    with lock:
        for fx, fy in flames:
            if fx == player_x and fy == player_y:
                return True
    return False


def input_thread(stdscr):
    while True:
        key = stdscr.getch()
        if key == curses.KEY_LEFT:
            move_player('left')
        elif key == curses.KEY_RIGHT:
            move_player('right')
        elif key == curses.KEY_UP:
            move_player('up')
        elif key == curses.KEY_DOWN:
            move_player('down')
        elif key == 27:
            return


def main(stdscr):
    global score
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    init_colors()

    threading.Thread(target=input_thread, args=(stdscr,), daemon=True).start()

    while True:
        draw_screen(stdscr)
        update_flames()
        if check_collision():
            stdscr.addstr(HEIGHT // 2, WIDTH // 2 - len("Game Over") // 2, "Game Over")
            stdscr.addstr(HEIGHT // 2 + 1, WIDTH // 2 - len(f"Final Score: {score}") // 2, f"Final Score: {score}")
            stdscr.refresh()
            stdscr.nodelay(0)
            stdscr.getch()
            break

        time.sleep(0.1)


if __name__ == "__main__":
    curses.wrapper(main)

print("Final Score:", score)