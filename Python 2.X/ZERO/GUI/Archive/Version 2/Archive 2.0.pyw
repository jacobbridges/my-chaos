import bz2
import dfs
import os
import tempfile
import Tkinter
import tkFileDialog
import tkMessageBox

################################################################################

def main():
    global root
    root = Tkinter.Tk()
    root.resizable(False, False)
    root.title('Archive 2.0')
    Tkinter.Label(root, text='NOTICE:\nThis program is not backward-compatible and\nconnot be used with the "Archive 1.0" program.', padx=5, pady=5).grid()
    Tkinter.Button(root, text='Compress Directory to File', command=wrapped_compressor).grid(sticky=Tkinter.NSEW)
    Tkinter.Button(root, text='Decompress File to Directory', command=wrapped_decompressor).grid(sticky=Tkinter.NSEW)
    root.mainloop()

def wrapped_compressor():
    wrapper(GUI_compressor)

def wrapped_decompressor():
    wrapper(GUI_decompressor)

def wrapper(function):
    root.withdraw()
    try:
        function()
    except Exception, error:
        if error:
            tkMessageBox.showerror('Exception', '%s: %s' % (error.__class__.__name__, error))
        else:
            tkMessageBox.showerror('Exception', error.__class__.__name__)
    root.deiconify()

def GUI_compressor():
    source = tkFileDialog.askdirectory(parent=root, title='Please select the source directory.', mustexist=True)
    if source:
        destination = tkFileDialog.asksaveasfilename(parent=root, title='Save Archive', filetypes=['Archive .caa'])
        if destination:
            if not destination.lower().endswith('.caa'):
                destination += '.caa'
            destination = open(destination, 'wb')
            try:
                compress(source, destination)
            finally:
                destination.close()

def GUI_decompressor():
    source = tkFileDialog.askopenfile(mode='rb', parent=root, title='Open Archive', filetypes=['Archive .caa'])
    if source:
        try:
            destination = tkFileDialog.askdirectory(parent=root, title='Please select the destination directory.', mustexist=True)
            if destination:
                decompress(source, destination)
        finally:
            source.close()

def compress(source, destination):
    temp = tempfile.TemporaryFile()
    dfs.Acquire(temp).acquire(source)
    temp.seek(0)
    compressor = bz2.BZ2Compressor()
    buff = temp.read(2 ** 20)
    while buff:
        destination.write(compressor.compress(buff))
        buff = temp.read(2 ** 20)
    temp.close()
    destination.write(compressor.flush())

def decompress(source, destination):
    decompressor = bz2.BZ2Decompressor()
    temp = tempfile.TemporaryFile()
    buff = source.read(2 ** 20)
    while buff:
        temp.write(decompressor.decompress(buff))
        buff = source.read(2 ** 20)
    temp.write(decompressor.unused_data)
    temp.seek(0)
    dfs.Release(temp).release(destination)
    temp.close()

################################################################################

if __name__ == '__main__':
    main()
