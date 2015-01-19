import aens_time
import Tkinter

def main():
    root = Tkinter.Tk()
    root.resizable(False, False)
    root.title('AT Clock')
    string = Tkinter.StringVar()
    Tkinter.Label(textvariable=string, font=('helvetica', 16, 'bold')).grid(padx=5, pady=5)
    thread = aens_time.Mille_Timer(update, string)
    thread.start()
    root.mainloop()

def update(string):
    s = aens_time.seconds()
    t = aens_time.format(s)
    p = 1000000000 * 1.01 ** (s / aens_time.SECONDS_PER_YEAR)
    string.set('T = %s\nP = %s' % (t, format(p)))

def format(number):
    cache = str(int(number))
    string = ''
    count = 0
    while cache:
        string = cache[-1] + string
        cache = cache[:-1]
        count += 1
        if count == 3 and cache:
            count = 0
            string = ',' + string
    return string

if __name__ == '__main__':
    main()
