import bz2
import cap
import cPickle
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
    root.title('Archive 1.0')
    Tkinter.Label(root, text='NOTICE:\nFiles produced by this program may be\nmore efficiently packed than ZIP files.', padx=5, pady=5).grid(sticky=Tkinter.NSEW)
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
        message = str(error)
        if message:
            tkMessageBox.showerror('Exception', '%s: %s' % (error.__class__.__name__, message))
        else:
            tkMessageBox.showerror('Exception', error.__class__.__name__)
    root.deiconify()

def GUI_compressor():
    source = tkFileDialog.askdirectory(parent=root, title='Please select the source directory.', mustexist=True)
    if source:
        destination = tkFileDialog.asksaveasfilename(parent=root, title='Save Archive', filetypes=['Archive .pfa'])
        if destination:
            if not destination.lower().endswith('.pfa'):
                destination += '.pfa'
            compress(source, open(destination, 'wb'))

def GUI_decompressor():
    source = tkFileDialog.askopenfile(mode='rb', parent=root, title='Open Archive', filetypes=['Archive .pfa'])
    if source:
        destination = tkFileDialog.askdirectory(parent=root, title='Please select the destination directory.', mustexist=True)
        if destination:
            decompress(source, destination)

def compress(source, destination):
    source = cap.Directory(source)
    temp = tempfile.TemporaryFile()
    cPickle.dump(source, temp, cPickle.HIGHEST_PROTOCOL)
    del source
    temp.seek(0)
    compressor = bz2.BZ2Compressor()
    buff = temp.read(1048576)
    while buff:
        destination.write(compressor.compress(buff))
        buff = temp.read(1048576)
    temp.close()
    destination.write(compressor.flush())
    destination.close()

def decompress(source, destination):
    decompressor = bz2.BZ2Decompressor()
    temp = tempfile.TemporaryFile()
    buff = source.read(1048576)
    while buff:
        temp.write(decompressor.decompress(buff))
        buff = source.read(1048576)
    source.close()
    temp.write(decompressor.unused_data)
    temp.seek(0)
    source = cPickle.load(temp)
    temp.close()
    source.write(destination)

################################################################################

if __name__ == '__main__':
    main()
