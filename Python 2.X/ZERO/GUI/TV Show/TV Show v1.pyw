import os
import sys
import Image
import ImageTk
import Tkinter

def main():
    global X, Y
    X, Y = 0, 0
    root = Tkinter.Tk()
    root.resizable(False, False)
    root.title('TV Show')
    find_images()
    screen = Tkinter.Canvas(root, width=320, height=240, highlightthickness=0)
    image = load_image()
    ident = screen.create_image(800, 600, image=image)
    screen.after(100, update, screen, image, ident)
    screen.pack()
    root.mainloop()

def find_images():
    global images, gen
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
    gen = iter(images)

def load_image():
    global gen
    try:
        return ImageTk.PhotoImage(file=gen.next())
    except:
        gen = iter(images)
        return ImageTk.PhotoImage(file=gen.next())

def update(screen, image, ident):
    global X, Y
    X += 1
    if X == 5:
        X = 0
        Y += 1
        if Y == 5:
            Y = 0
            screen.delete(ident)
            image = load_image()
            ident = screen.create_image(800, 600, image=image)
        else:
            screen.move(ident, 1280, -240)
    else:
        screen.move(ident, -320, 0)
    screen.after(100, update, screen, image, ident)
            

if __name__ == '__main__':
    main()
