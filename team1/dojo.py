import itertools
import random
import time
import curses


class Life:
    def __init__(self, w, h, screen):
        self.width = w
        self.height = h
        self.world = {(x, y): False for x in range(self.width) for y in range(self.height)}
        self.world = {(x, y): random.random() < 0.5 for x in range(self.width) for y in range(self.height)}
        self.screen = screen
        self.paused = True
        self.delay = 0.1
        self.population = 0
        self.generation = 0

    def tick(self):
        world_new = {}
        self.population = 0
        for x, y in self.world:
            currently_alive = self.world[(x, y)]
            live_neighbours = 0
            for (dx, dy) in itertools.product(range(-1, 2), repeat=2):
                if (dx, dy) == (0, 0):
                    continue
                live_neighbours += self.world[((x+dx) % self.width, (y+dy) % self.height)]
            if live_neighbours == 2:
                world_new[(x, y)] = currently_alive
            elif live_neighbours == 3:
                world_new[(x, y)] = True
            else:
                world_new[(x, y)] = False
            self.population += world_new[(x, y)]
        self.world = world_new
        self.generation += 1

    def run(self):
        quit = False
        fastmode = False
        while not quit:
            self.screen.nodelay(0)
            while self.paused:
                self.display()
                key = self.screen.getch()
                if key == curses.KEY_MOUSE:
                    _, x, y, _, bstate = curses.getmouse()
                    if bstate & curses.BUTTON1_RELEASED:
                        self.world[(x, y)] = not self.world[(x, y)]
                elif key == ord('p'):
                    self.paused = False
            self.screen.nodelay(1)
            while not self.paused:
                self.tick()
                self.display()
                key = self.screen.getch()
                while key != -1:
                    if key == ord('p'):
                        self.paused = True
                    elif key == ord('q'):
                        quit = self.paused = True
                    elif key in (ord('+'), ord('=')):
                        self.delay /= 1.5
                    elif key == ord('-'):
                        self.delay *= 1.5
                    elif key == ord('f'):
                        fastmode = not fastmode
                    key = self.screen.getch()
                if not fastmode:
                    time.sleep(self.delay)

    def display(self):
        for y in range(self.height):
            line = "".join(["#" if self.world[(x, y)] else " " for x in range(self.width)])
            self.screen.addstr(
                y,
                0,
                line
            )
        self.screen.addstr(
            self.height, 0,
            "Generation {}; Population {}".format(self.generation, self.population),
            curses.A_REVERSE
        )
        self.screen.refresh()

if __name__ == "__main__":
    try:
        stdscr = curses.initscr()

        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        curses.mousemask(1)

        l = Life(curses.COLS - 1, curses.LINES - 1, screen=stdscr)
        l.run()
    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
