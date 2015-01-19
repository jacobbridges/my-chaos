# STANDARD
import os
import random
import sys
import time
# GUI
import Tkinter
import tkMessageBox
import tkSimpleDialog
# SUPPORT
import winreg
import physics

################################################################################

BALLS = 20                  # NUMBER OF SIMULATED BALLS

BALL_RADIUS = 15            # RADIUS OF BALL IN PIXELS
START_SPACE = 100           # SIDE OFFSET IN PIXELS
SCREEN_WIDTH = 450          # WIDTH OF SCREEN IN PIXELS
SCREEN_HEIGHT = 450         # HEIGHT OF SCREEN IN PIXELS
WALL_SPACE = 35             # WIDTH OF WALLS IN PIXELS
FLOOR_SPACE = 25            # HEIGHT OF FLOOR IN PIXELS

BACKGROUND = 'white'        # COLOR OF BACKGROUND
BALL_COLOR = 'red'          # COLOR OF BALLS
FLOOR_COLOR = 'blue'        # COLOR OF FLOOR
FORCE_COLOR = 'light green' # COLOR OF FOURCE FIELD

FPS = 50                    # FRAMES PER SECOND
SPEED_LIMIT = 750           # PIXELS PER SECOND
WALL_FORCE = 2000           # PIXELS PER SECOND
GRAV_RATE = 200             # PIXELS PER SECOND
FRIC_RATE = 0.05            # VELOCITY PER SECOND

BOUNCE_MUL = 10             # COLLISION FORCE MULTIPLIER
COLORS = ('#FF0000',
          '#FF7F00',
          '#FFFF00',
          '#00FF00',
          '#0000FF',
          '#FF00FF')        # SELECTABLE BALL COLORS

TITLE = 'Kaos Rain (MKv3)'  # TITLE OF PROGRAM
HST_FONT = 'Courier 12'     # FONT OF HIGH SCORES
HST_COLOR = 'green'         # COLOR OF HIGH SCORES
START_HEIGHT = 70           # POSITION OF START BUTTON
START_TEXT = 'Play Game'    # START BUTTON TEXT
START_FONT = 'Helvetica 30' # START BUTTON FONT
DISABLED_COLOR = 'blue'     # DISABLED START BUTTON
ACTIVE_COLOR = 'red'        # ACTIVE START BUTTON
START_COLOR = 'black'       # HST BACKGROUND COLOR

MAX_NAME_LEN = 20           # LENGTH IN CHARACTERS
HST_WIDTH = 30              # LENGTH IN CHARACTERS
HST_SPACER = '.'            # JOINS NAME AND SCORE
WORLD_COLOR = 'white'       # GAME BACKGROUND COLOR
TIME_LIMIT = 600            # MAX TIME PER ROUND

WIN_TOGGLE_PAUSE = 500      # TIME IN MILLISECONDS
WIN_MESSAGE_TIME = 2250     # TIME IN MILLISECONDS
WIN_TEXT = 'YOU WIN'        # TEXT DISPLAYED ON WIN
WIN_FONT = 'Helvetica 50'   # WIN TEXT FONT
WIN_COLOR = 'red'           # WIN TEXT FILL COLOR

HST_SUBKEY = 'Software\\Atlantis Zero\\Kaos Rain\\Version 3\\HST'
SAMPLE_HST = {540: ['Wiz-Kid'],
              480: ['Speed Daemon'],
              420: ['[SW] O B 1'],
              360: ['1337 Spartan'],
              300: ['<<SHIFTED>>'],
              240: ['NovaSuperNova'],
              180: ['[ZT] Berserk Fury'],
              120: ['[ZT] Shadow'],
              60: ['newbie123'],
              0: ['SiriuS']}

################################################################################

# PROGRAM INITIALIZATION FUNCTIONS

def main():
    'Start the program.'
    initialise()
    show_start()
    Tkinter.mainloop()

def initialise():
    'Build the game\'s drawing surface.'
    global root, screen
    root = Tkinter.Tk()
    root.resizable(False, False)
    root.title(TITLE)
    root.protocol('WM_DELETE_WINDOW', terminate)
    root.bind_all('<Escape>', terminate)
    x = (root.winfo_screenwidth() - SCREEN_WIDTH) / 2
    y = (root.winfo_screenheight() - SCREEN_HEIGHT) / 2
    root.geometry('%dx%d+%d+%d' % (SCREEN_WIDTH, SCREEN_HEIGHT, x, y))
    screen = Tkinter.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.pack()

def show_start():
    'Display the start menu to the user.'
    global HST
    if not globals().has_key('HST'):
        try:
            HST = load_HST()
            check_HST(HST)
        except:
            HST = SAMPLE_HST
    string = format_HST(HST)
    screen.delete(Tkinter.ALL)
    screen.create_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, text=string, font=HST_FONT, fill=HST_COLOR)
    screen.create_text(SCREEN_WIDTH / 2, START_HEIGHT, text=START_TEXT, font=START_FONT, fill=DISABLED_COLOR, tag='start')
    screen.tag_bind('start', '<Enter>', activate)
    screen.tag_bind('start', '<Leave>', disable)
    screen.tag_bind('start', '<1>', start_game)
    screen['background'] = START_COLOR

################################################################################

# PROGRAM TERMINATION FUNCTIONS

def terminate(event=None):
    'Save the HST and close the program.'
    save_HST()
    root.quit()

def save_HST():
    'Save the HST in the registry.'
    hst = get_key(winreg.HKEY.CURRENT_USER, HST_SUBKEY, winreg.KEY.ALL_ACCESS)
    del hst.values
    for score in HST:
        hst.values[str(score)] = winreg.REG_SZ(repr(tuple(HST[score]))[1:-1])

def get_key(key, sub_key, sam=None):
    'Return the subkey specified.'
    key = winreg.Key(key=key)
    for sub_key in sub_key.split('\\'):
        if sub_key not in key.keys:
            key.keys = sub_key
        key = key.keys[sub_key]
    return winreg.Key(key=key, sam=sam)

################################################################################

# HST PREPARATION FUNCTIONS

def load_HST():
    'Load the High Score Table.'
    hst = get_key(winreg.HKEY.CURRENT_USER, HST_SUBKEY, winreg.KEY.ALL_ACCESS)
    database = {}
    for score in hst.values:
        database[int(score)] = list(eval(hst.values[score].value))
    return database

def check_HST(database):
    'Check number and type of names.'
    HST_NAMES = sum(map(len, SAMPLE_HST.values()))
    names = 0
    for key in database.keys():
        for name in database[key]:
            assert isinstance(name, str)
            names += 1
            assert names <= HST_NAMES
    assert names == HST_NAMES

def format_HST(database):
    lines = []
    for key in sorted(database.keys(), reverse=True):
        score = ' ' + str(key)
        for name in database[key]:
            lines.append((name[:MAX_NAME_LEN] + ' ').ljust(HST_WIDTH - len(score), HST_SPACER) + score)
    return '\n'.join(lines)

################################################################################

# MENU SUPPORT FUNCTIONS

def activate(event):
    'Highlight the start button.'
    screen.itemconfig('start', fill=ACTIVE_COLOR)

def disable(event):
    'Disable the start button.'
    screen.itemconfig('start', fill=DISABLED_COLOR)

def start_game(event):
    'Setup program for game play.'
    screen.delete(Tkinter.ALL)
    build_balls()
    build_world()
    build_loops()

################################################################################

# GAME SETUP FUNCTIONS
    
def build_balls():
    'Build some non-overlapping balls.'
    global balls
    balls = []
    sides = set()
    for ball in xrange(BALLS):
        x = -START_SPACE if random.randint(0, 1) else START_SPACE + SCREEN_WIDTH
        y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - FLOOR_SPACE - BALL_RADIUS) / BALL_RADIUS * BALL_RADIUS
        while (x, y) in sides:
            x = -START_SPACE if random.randint(0, 1) else START_SPACE + SCREEN_WIDTH
            y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - FLOOR_SPACE - BALL_RADIUS) / BALL_RADIUS * BALL_RADIUS
        sides.add((x, y))
        balls.append(physics.Ball(x, y, BALL_RADIUS))
        balls[-1].type = 0

def build_world():
    'Build the game\'s environment.'
    global clock_xy
    x = WALL_SPACE - 1
    y = SCREEN_HEIGHT - FLOOR_SPACE + 2
    screen.create_rectangle(0, 0, x, y, fill=FORCE_COLOR)
    screen.create_rectangle(SCREEN_WIDTH - x, 0, SCREEN_WIDTH, y, fill=FORCE_COLOR)
    screen.create_line(0, y, SCREEN_WIDTH, y, fill=FLOOR_COLOR, width=3)
    screen.bind('<1>', click)
    screen['background'] = WORLD_COLOR
    clock_xy = x / 2, (y + SCREEN_HEIGHT) / 2

def build_loops():
    'Build the game\'s two updating loops.'
    global frame_h, clock_h, start, frame, units
    frame_h = screen.after(1000 / FPS, update_frame)
    clock_h = screen.after(1000, update_clock)
    screen.create_text(clock_xy, text=f_time(TIME_LIMIT), tag='timer')
    start = time.clock()
    frame = 1.0
    units = 0

################################################################################

# ANIMATION LOOP FUNCTIONS

def update_frame():
    'Move and draw all balls.'
    global frame_h, frame
    move_balls()
    draw_balls()
    frame += 1
    frame_h = screen.after(int((start + frame / FPS - time.clock()) * 1000), update_frame)

def move_balls():
    'Crash, move, and mutate the balls.'
    for index, ball_1 in enumerate(balls[:-1]):
        for ball_2 in balls[index+1:]:
            ball_1.crash(ball_2)
    for ball in balls:
        ball.err *= BOUNCE_MUL
        ball.correct()
        governor(ball)
        ball.move(FPS)
        for mutate in wall, floor, gravity, friction:
            mutate(ball)

def draw_balls():
    'Draw the contents of the screen.'
    screen.delete('ball')
    for num, ball in enumerate(balls):
        x1 = ball.pos.x - ball.rad
        y1 = ball.pos.y - ball.rad
        x2 = ball.pos.x + ball.rad
        y2 = ball.pos.y + ball.rad
        screen.create_oval(x1, y1, x2, y2, fill=COLORS[ball.type], tag=(num, 'ball'))

################################################################################

# VELOCITY MUTATOR FUNCTIONS

def wall(ball):
    'Simulate a wall.'
    space = WALL_SPACE + BALL_RADIUS
    force = float(WALL_FORCE) / FPS
    if ball.pos.x <= space:
        ball.vel.x += force
    elif ball.pos.x >= SCREEN_WIDTH - space:
        ball.vel.x -= force

def floor(ball):
    'Simulate a floor.'
    floor_height = SCREEN_HEIGHT - FLOOR_SPACE - BALL_RADIUS
    if ball.pos.y >= floor_height:
        ball.pos.y = floor_height
        ball.vel.y *= -1

def gravity(ball):
    'Simulate gravity.'
    ball.vel.y += float(GRAV_RATE) / FPS

def friction(ball):
    'Simulate friction.'
    ball.vel *= FRIC_RATE ** (1.0 / FPS)

def governor(ball):
    'Simulate speed governor.'
    if abs(ball.vel) > SPEED_LIMIT:
        ball.vel = ball.vel.unit() * SPEED_LIMIT

################################################################################

# GAME INTERACTION FUNCTIONS

def click(event):
    'Try to change a ball\'s color.'
    global win_text, win_h
    try:
        ball = balls[int(screen.gettags(screen.find_withtag(Tkinter.CURRENT))[0])]
        ball.type = (ball.type + 1) % len(COLORS)
        if sum(map(lambda ball: ball.type, balls)) == len(COLORS) * BALLS - BALLS:
            screen.after_cancel(frame_h)
            screen.after_cancel(clock_h)
            screen.delete('ball')
            win_text = screen.create_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, text=WIN_TEXT, font=WIN_FONT, fill=WIN_COLOR)
            win_h = screen.after(WIN_TOGGLE_PAUSE, toggle_win)
            screen.after(WIN_MESSAGE_TIME, win if TIME_LIMIT - units >= min(HST.keys()) else lose)
    except:
        pass

def toggle_win():
    'Blink the win text on screen.'
    global win_text, win_h
    win_h = screen.after(WIN_TOGGLE_PAUSE, toggle_win)
    if win_text:
        screen.delete(win_text)
        win_text = None
    else:
        win_text = screen.create_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, text=WIN_TEXT, font=WIN_FONT, fill=WIN_COLOR)

def win():
    'Add name to HST and send to menu.'
    name = tkSimpleDialog.askstring('High Score', 'Please enter your name\nfor the high score table.') or 'No Name'
    score = TIME_LIMIT - units
    if HST.has_key(score):
        HST[score].insert(0, name)
    else:
        HST[score] = [name]
    loser = min(HST.keys())
    if len(HST[loser]) > 1:
        del HST[loser][-1]
    else:
        del HST[loser]
    screen.after_cancel(win_h)
    show_start()

################################################################################

# GAME TIMER FUNCTIONS

def update_clock():
    'Update the clock of the screen.'
    global clock_h, units
    screen.delete('timer')
    units += 1
    screen.create_text(clock_xy, text=f_time(TIME_LIMIT - units), tag='timer')
    if TIME_LIMIT - units:
        clock_h = screen.after(int((start + units + 1 - time.clock()) * 1000), update_clock)
    else:
        lose(True)

def f_time(seconds):
    'Return time with the correct format.'
    return '%02d:%02d' % (seconds / 60, seconds % 60)

def lose(real=False):
    'End the game and get input.'
    try_again = tkMessageBox.askquestion('GAME OVER', 'Do you want to try again?') == 'yes'
    screen.after_cancel(frame_h if real else win_h)
    screen.delete(Tkinter.ALL)
    if try_again:
        start_game(None)
    else:
        show_start()

################################################################################

# EXPERIMENTAL
# ============
# This section is being designed to install and
# uninstall this program on a computer. Installing
# involves creating registry entries for all program
# variables and for the High Score Table. Uninstalling
# involves removing all registry entries associated
# with this program, deleting this program, and
# deleting the support library for this program.
# Adding and removing this program should not fail.
# Optionally, this program should remove all traces
# of itself by keeping track of all places that it
# has been run from. Currently, this program has a
# per-user High Score Table. A "global" HST could
# be added as well, and it would be among the "global"
# HST entries that the run history of the program
# could be found, thus enabling global uninstallation.
# HKEY_LOCAL_MACHINE is recommended for global settings.

# NOTE
# ====
# Move this code to an installer that automatically
# deletes itself. Also, write the unistaller so that
# it is a separate program as well. In the end, there
# should be three programs: "install" , "Uninstall" ,
# and ("Game" , "Program" , etc.). There should also
# be one directory or zip file that contains the rest
# of the program's library of code for execution.
    
################################################################################

if __name__ == '__main__':
    main()
