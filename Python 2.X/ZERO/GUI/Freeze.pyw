import Tkinter
import ImageGrab
import ImageTk

def main():
    root = Tkinter.Tk()
    root.bind_all('<Escape>', lambda event: event.widget.quit())
    root.overrideredirect(True)
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('%dx%d+0+0' % (w, h))
    canvas = Tkinter.Canvas(root, width=w, height=h, highlightthickness=0)
    canvas.pack()
    image = ImageTk.PhotoImage(ImageGrab.grab())
    canvas.create_image(w / 2, h / 2, image=image)
    root.mainloop()

if __name__ == '__main__':
    main()
