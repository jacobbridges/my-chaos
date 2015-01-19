import os
import sys
import thread
import Queue
import Image
import ImageTk
import Tkinter

def main():
    root = Tkinter.Tk()
    root.resizable(False, False)
    next = run_image_sys()
    draw = Tkinter.Canvas(root, width=320, height=240, highlightthickness=0)
    draw.pack()
    image = next.get()
    root.title('TV Show <> %s' % image.name)
    ident = draw.create_image(800, 600, image=image)
    draw.after(100, update, root, next, draw, image, ident, 0, 0)
    root.mainloop()

def run_image_sys():
    images = []
    path = os.path.dirname(sys.argv[0])
    for name in os.listdir(path):
        path_name = os.path.join(path, name)
        if os.path.isfile(path_name):
            try:
                assert Image.open(path_name).size == (1600, 1200)
            except:
                pass
            else:
                images.append(path_name)
    if not images:
        sys.exit()
    next = Queue.Queue(1)
    thread.start_new_thread(loader, (images, next))
    return next

def loader(images, next):
    gen = iter(images)
    while True:
        try:
            name = gen.next()
            image = ImageTk.PhotoImage(file=name)
            image.name = os.path.splitext(os.path.basename(name))[0]
            next.put(image)
        except StopIteration:
            gen = iter(images)

def update(root, next, draw, image, ident, X, Y):
    X += 1
    if X == 5:
        X = 0
        Y += 1
        if Y == 5:
            Y = 0
            draw.delete(ident)
            image = next.get()
            root.title('TV Show <> %s' % image.name)
            ident = draw.create_image(800, 600, image=image)
        else:
            draw.move(ident, 1280, -240)
    else:
        draw.move(ident, -320, 0)
    draw.after(100, update, root, next, draw, image, ident, X, Y)

if __name__ == '__main__':
    main()
