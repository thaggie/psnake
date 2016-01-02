import curses
import atexit 
from collections import deque
import random

# Setup the drawing environment
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
curses.curs_set(0)

# cleanup the drawing environment on exit
def cleanup():
	curses.nocbreak()
	curses.curs_set(1)
	stdscr.keypad(0) 
	curses.echo()
	curses.endwin()
atexit.register(cleanup)	

# We don't want to wait for keyboard input
stdscr.nodelay(1)

maxscore = 0
maxy, maxx = stdscr.getmaxyx()

def drawBorder():
    for x in range(0, maxx-1):
    	stdscr.addstr(0, x, " ", curses.A_REVERSE)
    	stdscr.addstr(maxy-1, x, " ", curses.A_REVERSE)
    for y in range(0, maxy-1):
    	stdscr.addstr(y, 0, " ", curses.A_REVERSE)
    	stdscr.addstr(y, maxx-1, " ", curses.A_REVERSE)
    stdscr.addstr(0, maxx/2-3, "SNAKE", curses.A_REVERSE)    


class GameState:
    def __init__(self):
        self.reset()
    def reset(self):
        stdscr.clear()
        drawBorder()
        self.dx = 2
        self.dy = 0
        self.x = maxx / 2
        self.y = maxy / 2
        self.xs = deque([self.x, self.x, self.x, self.x])
        self.ys = deque([self.y, self.y, self.y, self.y])
        self.score = 0
        self.nextTarget()
    def nextTarget(self):
        self.ax = random.randint(1, (maxx-1)/2) * 2
        self.ay = random.randint(1, maxy-1)
        stdscr.addstr(self.ay, self.ax, "*")
    def within(self):
        for i in range(0, len(self.xs)):
            if self.x == self.xs[i] and self.y == self.ys[i]:
                return 1
        return 0
    def next(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        if self.within() or self.x == 0 or self.y == 0 or self.x >= maxx-1 or self.y >= maxy-1:
            curses.flash()
            gs.reset()
        else:
            if self.x == self.ax and self.y == self.ay:
                self.score = self.score + 10
                self.nextTarget()
            else:
                ox = gs.xs.popleft()
                oy = gs.ys.popleft()
                stdscr.addstr(oy, ox, " ")
            self.xs.append(self.x)
            self.ys.append(self.y)
            stdscr.addstr(self.y, self.x, "o")


gs = GameState()

while 1:
    c = stdscr.getch()
    if c == ord('q'):
        break  # Exit the while()
    elif c == curses.KEY_LEFT:
    	gs.dx = -2
    	gs.dy = 0
    elif c == curses.KEY_RIGHT:
    	gs.dx = 2
    	gs.dy = 0
    elif c == curses.KEY_UP:
    	gs.dx = 0
    	gs.dy = -1
    elif c == curses.KEY_DOWN:
    	gs.dx = 0
    	gs.dy = +1

    gs.next()

    if gs.score > maxscore:
        maxscore = gs.score
    
    stdscr.addstr(maxy-1, 1, "Score: {0} Max: {1}".format(gs.score, maxscore), curses.A_REVERSE)
    curses.napms(200)