import Tkinter
import tkFileDialog
import tkMessageBox
import os
import spice

################################################################################

def main():
    global root, sour_d, sour_e, dest_d, dest_e, keys_d, keys_e
    root = Tkinter.Tk()
    root.title('Cinnamon')
    root.resizable(False, False)
    root.bind_class('Entry', '<Control-Key-a>', select)
    sour_d = tkFileDialog.Open(root, parent=root, title='Please select source file.')
    dest_d = tkFileDialog.Directory(root, parent=root, title='Please select destination directory.', mustexist=True)
    keys_d = tkFileDialog.Open(root, parent=root, title='Please select key file.')
    sour_f = Tkinter.LabelFrame(root, text='Source')
    dest_f = Tkinter.LabelFrame(root, text='Destination')
    keys_f = Tkinter.LabelFrame(root, text='Keys')
    sour_e = Tkinter.Entry(sour_f, width=30)
    dest_e = Tkinter.Entry(dest_f, width=30)
    keys_e = Tkinter.Entry(keys_f, width=30)
    sour_b = Tkinter.Button(sour_f, text='Browse ...', command=b_sour)
    dest_b = Tkinter.Button(dest_f, text='Browse ...', command=b_dest)
    keys_b = Tkinter.Button(keys_f, text='Browse ...', command=b_keys)
    enco_b = Tkinter.Button(root, text='Encode File', command=safe_encode)
    deco_b = Tkinter.Button(root, text='Decode File', command=safe_decode)
    crea_b = Tkinter.Button(root, text='Create Key', command=safe_create)
    sour_e.bind('<Return>', b_sour)
    dest_e.bind('<Return>', b_dest)
    keys_e.bind('<Return>', b_keys)
    sour_b.bind('<Return>', b_sour)
    dest_b.bind('<Return>', b_dest)
    keys_b.bind('<Return>', b_keys)
    enco_b.bind('<Return>', safe_encode)
    deco_b.bind('<Return>', safe_decode)
    crea_b.bind('<Return>', safe_create)
    sour_f.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
    dest_f.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
    keys_f.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
    sour_e.grid(row=0, column=0, padx=5, pady=5)
    sour_b.grid(row=0, column=1, padx=5, pady=5)
    dest_e.grid(row=0, column=0, padx=5, pady=5)
    dest_b.grid(row=0, column=1, padx=5, pady=5)
    keys_e.grid(row=0, column=0, padx=5, pady=5)
    keys_b.grid(row=0, column=1, padx=5, pady=5)
    enco_b.grid(row=3, column=0, padx=5, pady=5, sticky=Tkinter.NSEW)
    deco_b.grid(row=3, column=1, padx=5, pady=5, sticky=Tkinter.NSEW)
    crea_b.grid(row=4, column=0, padx=5, pady=5, sticky=Tkinter.NSEW, columnspan=2)
    root.mainloop()

def select(event):
    event.widget.selection_range(0, Tkinter.END)
    return 'return'

def b_sour(event=None):
    path = sour_d.show()
    if path:
        sour_e.delete(0, Tkinter.END)
        sour_e.insert(0, os.path.realpath(path))
    sour_e.focus_set()

def b_dest(event=None):
    path = dest_d.show()
    if path:
        dest_e.delete(0, Tkinter.END)
        dest_e.insert(0, os.path.realpath(path))
    dest_e.focus_set()

def b_keys(event=None):
    path = keys_d.show()
    if path:
        keys_e.delete(0, Tkinter.END)
        keys_e.insert(0, os.path.realpath(path))
    keys_e.focus_set()

def safe_encode(event=None):
    safe(encode, 'The file could not be encoded.')

def safe_decode(event=None):
    safe(decode, 'The file could not be decoded.')

def safe_create(event=None):
    safe(create, 'The key could not be created.')

def safe(function, message):
    root.withdraw()
    try:
        function(sour_e.get(), dest_e.get(), keys_e.get())
    except Exception, error:
        tkMessageBox.showerror('Error', '%s\n%s' % (message, error))
    root.deiconify()

def encode(sour, dest, keys):
    spice.encode(file(sour, 'rb'), file(os.path.join(dest, os.path.basename(sour) + '.cam'), 'wb'), *get_keys(keys))

def decode(sour, dest, keys):
    spice.decode(file(sour, 'rb'), file(os.path.join(dest, os.path.basename(sour)[:-4]), 'wb'), *get_keys(keys))

def create(sour, dest, keys):
    path = os.path.join(dest, os.path.basename(keys))
    file(path + '.major', 'wb').write(spice.major())
    file(path + '.minor', 'wb').write(spice.minor())

def get_keys(keys):
    assert keys[-6:].lower() in ('.major', '.minor'), 'Key has invalid extention.'
    path = keys[:-5]
    return file(path + 'major', 'rb').read(), file(path + 'minor', 'rb').read()

if __name__ == '__main__':
    main()
