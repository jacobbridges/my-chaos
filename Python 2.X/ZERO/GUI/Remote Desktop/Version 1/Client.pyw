import Image
import ImageTk
import socket
import struct
import Tkinter
import zlib

W, H = 800, 600
X, Y = W / 2, H / 2

def main():
    global server, canvas
    server = socket.socket()
    server.connect(('127.0.0.1', 8060))
    root = Tkinter.Tk()
    root.resizable(False, False)
    root.title('Remote Desktop')
    canvas = Tkinter.Canvas(root, width=W, height=H, highlightthickness=0)
    canvas.cursor = [False]
    canvas.bind('<ButtonPress-1>', lambda event: setattr(canvas, 'cursor', [True, event.x, event.y]))
    canvas.bind('<ButtonRelease-1>', lambda event: setattr(canvas, 'cursor', [False]))
    canvas.bind('<Motion>', move)
    canvas.pack()
    update()
    root.mainloop()

def move(event):
    global X, Y
    if canvas.cursor[0]:
        diff = event.x - canvas.cursor[1], event.y - canvas.cursor[2]
        canvas.move(Tkinter.ALL, diff[0], diff[1])
        canvas.cursor[1:] = event.x, event.y
        X += diff[0]
        Y += diff[1]

def update():
    global image
    server.sendall('\0')
    width, height, size = struct.unpack('!HHI', recvall(server, 8))
    data = zlib.decompress(recvall(server, size))
    image = ImageTk.PhotoImage(Image.fromstring('RGB', (width, height), data))
    canvas.delete(Tkinter.ALL)
    canvas.create_image(X, Y, image=image)
    canvas.after(1000, update)

def recvall(socket, size):
    buff = ''
    while len(buff) < size:
        buff += socket.recv(size - len(buff))
    return buff

if __name__ == '__main__':
    main()
