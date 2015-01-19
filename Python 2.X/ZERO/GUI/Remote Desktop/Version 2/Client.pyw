SERVER = 'luna', 8061       # HOST ADDRESS
WIDTH = 800                 # SCREEN WIDTH
HEIGHT = 600                # SCREEN HEIGHT
AFTER = 5000                # UPDATED AFTER

import Tkinter
import socket
import struct
import bz2
import Image
import ImageTk
import cPickle
import bsdiff

X, Y = WIDTH / 2, HEIGHT / 2

def main():
    canvas = build_GUI()
    prime_system(canvas)
    Tkinter.mainloop()

def build_GUI():
    root = Tkinter.Tk()
    root.title('Secret Eye')
    root.resizable(False, False)
    canvas = Tkinter.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
    canvas.bind('<ButtonPress-1>', lambda event: setattr(canvas, 'cursor', (event.x, event.y)))
    canvas.bind('<ButtonRelease-1>', lambda event: delattr(canvas, 'cursor'))
    canvas.bind('<Motion>', move)
    canvas.pack()
    return canvas

def move(event):
    global X, Y
    canvas = event.widget
    if hasattr(canvas, 'cursor'):
        x = event.x - canvas.cursor[0]
        y = event.y - canvas.cursor[1]
        canvas.move(Tkinter.ALL, x, y)
        canvas.cursor = event.x, event.y
        X += x
        Y += y

def prime_system(canvas):
    server = socket.socket()
    server.connect(SERVER)
    width, height, size = struct.unpack('!HHI', recvall(server, 8))
    origin = bz2.decompress(recvall(server, size))
    image = ImageTk.PhotoImage(Image.fromstring('RGB', (width, height), origin))
    handle = canvas.create_image(X, Y, image=image)
    canvas.after(AFTER, get_update, server, origin, image, canvas, handle)

def recvall(socket, size):
    buff = ''
    while len(buff) < size:
        temp = socket.recv(size - len(buff))
        if temp:
            buff += temp
        else:
            raise EOFError
    return buff

def get_update(server, origin, image, canvas, handle):
    server.sendall('\0')
    width, height, size = struct.unpack('!HHI', recvall(server, 8))
    string = recvall(server, size)
    pickle = bz2.decompress(string)
    diff = cPickle.loads(pickle)
    update = bsdiff.Patch(origin, width * height * 3, *diff)
    image = ImageTk.PhotoImage(Image.fromstring('RGB', (width, height), update))
    canvas.delete(handle)
    handle = canvas.create_image(X, Y, image=image)
    canvas.after(AFTER, get_update, server, update, image, canvas, handle)

if __name__ == '__main__':
    main()
