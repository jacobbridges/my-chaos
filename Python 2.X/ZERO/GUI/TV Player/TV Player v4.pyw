import Tkinter
import tkFileDialog
import ImageTk

COLORS = 'black', 'red', 'green', 'blue'

def main():
    global X, Y, hold, speed, blink, pause, screen, timer
    X, Y = 0, 0
    hold = []
    speed = 128
    blink = None
    pause = None
    root = Tkinter.Tk()
    root.withdraw()
    root.resizable(False, False)
    root.title('Tiled Video Player')
    root.bind('<Escape>', do_pause)
    root.bind('-', slow)
    root.bind('=', fast)
    image = get_image()
    screen = Tkinter.Canvas(root, width=320, height=240, background='red', highlightthickness=0)
    screen.bind('<Motion>', motion)
    screen.bind('<ButtonPress-1>', press)
    screen.bind('<ButtonRelease-1>', release)
    screen.bind('<Button-3>', delete)
    screen.pack()
    screen.create_image(800, 600, image=image)
    timer = screen.after(100, update)
    root.deiconify()
    root.mainloop()

def slow(event):
    global speed, timer
    if timer is None:
        update(True, False)
    else:
        if speed < 1024:
            speed <<= 1
            screen.after_cancel(timer)
            timer = screen.after(speed, update)
        show_speed(True)

def fast(event):
    global speed, timer
    if timer is None:
        update(False, False)
    else:
        if speed > 2:
            speed >>= 1
            screen.after_cancel(timer)
            timer = screen.after(speed, update)
        show_speed(True)

def get_image():
    try:
        filename = tkFileDialog.askopenfilename(title='Tiled Video Player')
        assert filename
        image = ImageTk.PhotoImage(file=filename)
        assert (1600, 1200) == (image.width(), image.height())
        return image
    except:
        raise SystemExit

def motion(event):
    if hold:
        hold.extend([event.x, event.y])
        event.widget.create_line(hold[-4:], fill='red', width=2, tag='TEMP')

def press(event):
    global hold
    hold = [event.x, event.y]

def release(event):
    global hold
    if len(hold) > 2:
        event.widget.delete('TEMP')
        event.widget.create_line(hold, fill='red', width=2, tag='LINE', smooth=True)
    hold = []

def delete(event):
    event.widget.delete('LINE')

def do_pause(event):
    global timer, pause
    if timer is None:
        timer = screen.after(speed, update)
        screen.delete('PAUSE')
        screen.after_cancel(pause)
        pause = None
    else:
        timer = screen.after_cancel(timer)
        show_pause(True)

def show_pause(start=False):
    global P_COLOR, pause
    if start:
        P_COLOR = 0
        if pause is not None:
            screen.after_cancel(pause)
    else:
        P_COLOR += 1
        P_COLOR %= len(COLORS)
    screen.delete('PAUSE')
    fill = COLORS[P_COLOR]
    screen.create_text(295, 10, fill=fill, text='PAUSE', tag='PAUSE')
    pause = screen.after(500, show_pause)

def show_speed(start=False):
    global FPS_COLOR, blink
    if start:
        FPS_COLOR = 0
        if blink is not None:
            screen.after_cancel(blink)
    else:
        FPS_COLOR += 1
    screen.delete('FPS')
    if FPS_COLOR < len(COLORS):
        fill = COLORS[FPS_COLOR]
        text = '%s FPS' % int(1000.0 / speed + 0.5)
        screen.create_text(25, 10, fill=fill, text=text, tag='FPS')
        blink = screen.after(500, show_speed)
    else:
        blink = None

def update(back=False, loop=True):
    global X, Y, timer
    if loop:
        timer = screen.after(speed, update)
    if not back:
        X += 1
        if X == 5:
            X = 0
            Y += 1
            if Y == 5:
                Y = 0
                screen.move(1, 1280, 960)
            else:
                screen.move(1, 1280, -240)
        else:
            screen.move(1, -320, 0)
    else:
        backup()

def backup():
    global X, Y
    X -= 1
    if X < 0:
        X = 4
        Y -= 1
        if Y < 0:
            Y = 4
            screen.move(1, -1280, -960)
        else:
            screen.move(1, -1280, 240)
    else:
        screen.move(1, 320, 0)

if __name__ == '__main__':
    main()
