from pygame import *
from random import *
from socket import *
from thread import *

from matrix import *
import spots as spots

import os
import sys
import traceback
import server

server.LOCAL_MODE = True
server.RUN_SERVER = False

########################################

_thread = start_new_thread

def start_new_thread(function, args):
    _thread(_show_thread, (function, args))

def _show_thread(function, args):
    try:
        function(*args)
    except SystemExit:
        pass
    except:
        traceback.print_exc()

########################################

OLD_POINTER = False
USE_SOUND = True

def program_loop():
    global window, stack
    display.init()
    font.init()
    sound_init()
    sound.background.set_volume(.3)
    sound.background.play(-1)
    icon = image.load(os.path.join('img', 'icon.tif'))
    display.set_icon(icon)
    size = 320, 240
    window = display.set_mode(size)
    display.set_caption('Tic Tac Toe')
    if OLD_POINTER:
        mouse.set_cursor(*cursors.tri_left)
    else:
        mouse.set_visible(False)
        cursor = image.load(os.path.join('img', 'cursor.tif'))
    stack = [Get_Host()]
    clock = time.Clock()
    while True:
        for moment in event.get():
            if moment.type == QUIT or (moment.type == KEYDOWN and moment.key == K_ESCAPE):
                sys.exit()
            stack[-1].handle(moment)
        stack[-1].run()
        if OLD_POINTER or not mouse.get_focused():
            display.flip()
            clock.tick(5)
        else:
            copy = window.copy()
            pos = mouse.get_pos()
            window.blit(cursor, pos)
            display.flip()
            window.blit(copy, pos, cursor.get_rect().move(pos))
            clock.tick(20)

########################################

def sound_init():
    global sound
    try:
        assert USE_SOUND
        mixer.init()
        class Sound_Help:
            def __init__(self):
                self.__cache = {}
            def __getattr__(self, name):
                if name in self.__cache:
                    return self.__cache[name]
                snd = mixer.Sound(os.path.join('snd', name + '.wav'))
                snd.set_volume(.6)
                self.__cache[name] = snd
                return snd
    except:
        class Sound_Help:
            def __call__(self, *args, **kwargs):
                pass
            def __getattr__(self, name):
                return Sound_Help()
    sound = Sound_Help()

########################################

class Get_Host:

    def __init__(self):
        self.error = False
        self.font = font.SysFont('Verdana', 15)
        self.num_font = font.SysFont('Courier', 10)
        self.color = 255, 255, 255
        self.numbers = []
        self.draw()
        self.start()

    def start(self):
        pass

    def draw(self):
        window.fill((64, 64, 64))
        if self.error:
            string = 'Game Host IP# - Could not connect.'
        else:
            string = 'Game Host IP#'
        text = self.font.render(string, 1, self.color)
        window.blit(text, (5, 0))
        self.draw_numbers()
        self.draw_server()

    def run(self):
        pass

    def handle(self, moment):
        if moment.type == KEYDOWN:
            key = moment.key - 48
            if 0 <= key <= 9 and len(self.numbers) != 12 and not server.RUN_SERVER:
                self.numbers.append(key)
                self.draw()
                if len(self.numbers) == 12:
                    text = self.font.render('Please press Enter', 1, self.color)
                    window.blit(text, (5, self.font.get_height() + self.num_font.get_height() + 10))
            elif moment.key == 8 and not server.RUN_SERVER:
                self.numbers = self.numbers[:-1]
                self.draw()
            elif moment.key == 13 and (len(self.numbers) == 12 or server.RUN_SERVER):
                if server.RUN_SERVER:
                    string = '127.0.0.1 '
                else:
                    index = 1
                    string = ''
                    for num in self.numbers:
                        string += str(num)
                        index += 1
                        if index % 4 == 0:
                            string += '.'
                            index += 1
                stack.append(Find_Player(string[:-1]))
        elif moment.type == MOUSEBUTTONDOWN:
            if self.button.collidepoint(*moment.pos):
                server.RUN_SERVER = not server.RUN_SERVER
                if server.RUN_SERVER:
                    start_new_thread(server.main, ())
                self.draw()

    def draw_numbers(self):
        if server.RUN_SERVER:
            string = '127.0.0.1 '
        else:
            index = 1
            string = ''
            for num in self.numbers:
                string += str(num)
                index += 1
                if index % 4 == 0:
                    string += '.'
                    index += 1
            while len(string) <= 15:
                if index % 4 == 0:
                    string += '.'
                else:
                    string += '_'
                index += 1
        string = ' '.join(string[:-1])
        text = self.num_font.render(string, 1, self.color)
        window.blit(text, (5, self.font.get_height() + 5))

    def draw_server(self):
        if server.RUN_SERVER:
            text = self.font.render('Please press Enter', 1, self.color)
            window.blit(text, (5, self.font.get_height() + self.num_font.get_height() + 10))
            args = 'Server is [ON]', 1, (0, 255, 0), (0, 0, 95)
        else:
            args = 'Server is [OFF]', 1, (255, 0, 0), (0, 0, 95)
            if len(self.numbers) == 12:
                text = self.font.render('Please press Enter', 1, self.color)
                window.blit(text, (5, self.font.get_height() + self.num_font.get_height() + 10))
        text = self.font.render(*args)
        pos = 5, window.get_height() - text.get_height() - 5
        window.blit(text, pos)
        self.button = text.get_rect().move(*pos)

########################################

class Find_Player:

    OTHER = {'o': 'x', 'x': 'o'}

    def __init__(self, host):
        self.host = host
        self.font = font.SysFont('Verdana', 15)
        self.color = 255, 255, 255
        self.count = 0
        self.draw()
        self.start()

    def start(self):
        start_new_thread(self.link_to_host, ())

    def draw(self):
        window.fill((32, 32, 32))

    def handle(self, moment):
        pass

    def run(self):
        self.count += 1
        if self.count % 20 == 0:
            self.draw()
            text = self.font.render('Finding Player ' + '.' * (self.count / 20), 1, self.color)
            window.blit(text, (5, 5))
        self.count %= 60

    def link_to_host(self):
        self.server = socket()
        try:
            stack[-2].error = False
            self.server.connect((self.host, 2536))
            self.shake_hands(spots.qri(self.server))
        except:
            stack[-2].error = True
            stack[-2].draw()
            stack.pop()

    def shake_hands(self, qri):
        self.ID, taken = qri.query()
        if taken in list('ox'):
            you = self.OTHER[taken]
            stack.append(Show_You(you, qri))
        else:
            you = choice(self.OTHER.keys())
            stack.append(Get_Choice(you, qri))

########################################

class Get_Choice:

    def __init__(self, you, server):
        self.you = you
        self.server = server
        self.font = font.SysFont('Verdana', 15)
        self.color = 255, 255, 255
        self.draw()
        self.start()

    def draw(self):
        window.fill((127, 0, 0))
        text = self.font.render('Do you want to play as "%s" today?' % self.you.upper(), 1, self.color)
        window.blit(text, (5, 5))
        # make buttons
        yes = self.font.render('YES', 1, self.color, (0, 200, 0))
        no = self.font.render('NO', 1, self.color, (0, 200, 0))
        yes_cord = 5, 10 + text.get_height()
        no_cord = 10 + yes.get_rect().width, 10 + text.get_height()
        window.blit(yes, yes_cord)
        window.blit(no, no_cord)
        # save boxs
        self.yes = yes.get_rect().move(*yes_cord)
        self.no = no.get_rect().move(*no_cord)

    def start(self):
        pass

    def handle(self, moment):
        if moment.type == MOUSEBUTTONDOWN:
            if self.yes.collidepoint(*moment.pos):
                # player liked choice
                self.server.reply(stack[-2].ID, self.you)
                stack.append(Game_Board(self.you, self.server, True))
            elif self.no.collidepoint(*moment.pos):
                # player did not like
                you = Find_Player.OTHER[self.you]
                self.server.reply(stack[-2].ID, you)
                stack.append(Game_Board(you, self.server, True))

    def run(self):
        pass

########################################

class Show_You:

    def __init__(self, player, server):
        self.server = server
        self.player = player
        self.font = font.SysFont('Verdana', 15)
        self.color = 255, 255, 255
        self.draw()
        self.start()

    def draw(self):
        window.fill((0, 127, 0))
        text = self.font.render('You will be playing as "%s" today.' % self.player.upper(), 1, self.color)
        window.blit(text, (5, 5))
        text = self.font.render('OKAY', 1, self.color, (200, 0, 0))
        box = text.get_rect()
        cord = 5, 10 + text.get_height()
        window.blit(text, cord)
        self.box = box.move(*cord)
        
    def start(self):
        pass

    def handle(self, moment):
        if moment.type == MOUSEBUTTONDOWN:
            if self.box.collidepoint(*moment.pos):
                self.server.reply(stack[-2].ID, self.player)
                stack.append(Game_Board(self.player, self.server, False))
                
    def run(self):
        pass

########################################

class Game_Board:

    SERVER_TIMEOUT = 3

    def __init__(self, you, server, pause):
        self.you = you
        self.server = server
        self.pause = pause
        self.playing = True
        self.won = False
        self.lost = False
        self.font = font.SysFont('Verdana', 15)
        self.color = 255, 255, 255
        # Create image resources
        self.mark_o = image.load(os.path.join('img', 'mark_o.tif'))
        self.mark_x = image.load(os.path.join('img', 'mark_x.tif'))
        self.board = image.load(os.path.join('img', 'board.tif'))
        # Create lines for grid
        self.horz = Surface((160, 5))
        self.vert = Surface((5, 160))
        self.horz.fill((0, 0, 180))
        self.vert.fill((0, 0, 180))
        # END
        self.create_rect()
        self.draw()
        self.start()

    def create_rect(self):
        self.imgs = Matrix(3, 3)
        self.rect = Matrix(3, 3)
        for y in range(3):
            for x in range(3):
                self.rect[y][x] = Rect(80 + 55 * x, 75 + 55 * y, 50, 50)
        
    def draw(self):
        window.blit(self.board, (0, 0))
        window.blit(self.horz, (80, 125))
        window.blit(self.horz, (80, 180))
        window.blit(self.vert, (130, 75))
        window.blit(self.vert, (185, 75))
        window.blit(getattr(self, 'mark_' + self.you), (265, 5))
        count = 0
        for y, row in enumerate(self.imgs):
            for x, img in enumerate(row):
                if img is not None:
                    window.blit(img, self.rect[y][x].topleft)
                    count += 1
        if count == 9 and self.playing:
            self.playing = False
            sound.stalemate.play()
            text = self.font.render('Game was tied.', 1, self.color, (0, 0, 0))
            window.blit(text, (5, 5))
            sys.exit()

    def start(self):
        start_new_thread(self.engine, ())

    def handle(self, moment):
        if moment.type == MOUSEBUTTONDOWN and self.playing and not self.pause:
            for y, row in enumerate(self.rect):
                for x, rect in enumerate(row):
                    if rect.collidepoint(*moment.pos):
                        start_new_thread(self.click, (y, x))

    def run(self):
        pass

    def click(self, row, col):
        try:
            code, response = self.server.call((row, col), self.SERVER_TIMEOUT)
            if code:
                # click was good
                if response in list('ox'):
                    getattr(sound, 'win%s' % randint(1, 3)).play()
                    msg = 'You won!'
                    self.won = True
                    self.playing = False
                else:
                    if row == col == 1:
                        sound.local_middle.play()
                    else:
                        sound.local_move.play()
                    msg = "It is your opponent's turn."
                self.imgs[row][col] = getattr(self, 'mark_' + self.you)
            else:
                # click was out of turn
                msg = response
        except Warning:
            sound.error.play()
            msg = 'Server is not responding.'
            self.playing = False
        except IOError:
            sound.error.play()
            msg = 'Server has disconnected.'
            self.playing = False
        except:
            sound.error.play()
            traceback.print_exc()
            msg = 'UNKNOWN ERROR !!!'
            self.playing = False
        self.draw()
        text = self.font.render(str(msg), 1, self.color, (0, 0, 0))
        window.blit(text, (5, 5))

    def engine(self):
        if self.pause:
            text = self.font.render('Waiting for response ...', 1, self.color, (0, 0, 0))
            window.blit(text, (5, 5))
            while self.pause:
                try:
                    data = self.server.query(1)
                    time.wait(100)
                    self.server.reply(*data)
                    self.pause = False
                except Warning:
                    pass
                except:
                    self.playing = False
            self.draw()
        check = False
        sound.startup.play()
        while (self.playing or check) and not (self.won or self.lost):
            try:
                ID, pos = self.server.query(self.SERVER_TIMEOUT)
            except:
                check = False
                for row in self.imgs:
                    if None in row:
                        check = True
                        break
                continue
            if pos == (-1, -1):
                sound.lose.play()
                self.playing = False
                self.lost = True
                self.draw()
                text = self.font.render("You lost    :'(", 1, self.color, (0, 0, 0))
                window.blit(text, (5, 5))
            else:
                if pos == (1, 1):
                    if sum(map(lambda x: 0 if x is None else 1, (cell for row in self.imgs for cell in row))) != 8:
                        sound.remote_middle.play()
                else:
                    sound.remote_move.play()
                other = Find_Player.OTHER[self.you]
                row, col = pos
                self.imgs[row][col] = getattr(self, 'mark_' + other)
                try:
                    self.draw()
                    text = self.font.render('It is your turn.', 1, self.color, (0, 0, 0))
                    window.blit(text, (5, 5))
                except:
                    check = True
                    continue
            self.server.reply(ID, None)
        time.wait(10000)
        stack[-3].server.shutdown(SHUT_RDWR)
        stack[-3].server.close()
        stack.pop()
        stack.pop()
        stack.pop()
        stack[-1].draw()

########################################

def main():
    try:
        program_loop()
    finally:
        quit()
