import Tkinter
import para_time

def main():
    root = Tkinter.Tk()
    root.resizable(False, False)
    root.title('PT Clock')
    string = Tkinter.StringVar()
    Tkinter.Label(textvariable=string, font=('helvetica', 16, 'bold')).grid(padx=5, pady=5)
    thread = para_time.Quantum_Timer(update, string)
    thread.start()
    root.mainloop()

def update(string):
    s = para_time.seconds()
    t = para_time.format(s)
    p = 1000000000 * 1.01 ** (s / para_time.SECONDS_PER_YEAR)
    string.set('T = %s\nP = %s' % (t, format(p)))

def format(number):
    cache = str(int(number))
    string = ''
    count = 0
    while cache:
        string = cache[-1] + string
        cache = cache[:-1]
        if cache:
            count += 1
            if count == 3:
                string = ',' + string
                count = 0
    return string

if __name__ == '__main__':
    main()
