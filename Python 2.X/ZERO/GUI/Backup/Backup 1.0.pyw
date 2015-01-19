import os
import sys
import Tkinter
import tkFileDialog
import tkMessageBox

def main():
    global master, source_dialog, destination_dialog, source_entry, destination_entry
    # Create the main window.
    master = Tkinter.Tk()
    master.title('Backup 1.0')
    master.resizable(False, False)
    # Create the file dialogs.
    options = {'mustexist': True, 'parent': master, 'title': 'Please choose a source directory and then select OK.'}
    if os.name == 'nt':
        if os.path.exists('C:\\Documents and Settings'):
            options['initialdir'] = 'C:\\Documents and Settings'
        elif os.path.exists('C:\\'):
            options['initialdir'] = 'C:\\'
    source_dialog = tkFileDialog.Directory(master, **options)
    options['title'] = options['title'].replace('source', 'destination')
    destination_dialog = tkFileDialog.Directory(master, **options)
    # Create widgets.
    source = Tkinter.LabelFrame(master, text='Source')
    source_entry = Tkinter.Entry(source, width=30)
    source_button = Tkinter.Button(source, text='Browse ...', command=browse_source)
    destination = Tkinter.LabelFrame(master, text='Destination')
    destination_entry = Tkinter.Entry(destination, width=30)
    destination_button = Tkinter.Button(destination, text='Browse ...', command=browse_destination)
    okay_button = Tkinter.Button(master, text='Okay', command=okay)
    exit_button = Tkinter.Button(master, text='Exit', command=terminate)
    # Create bindings.
    source_button.bind('<Return>', browse_source)
    destination_button.bind('<Return>', browse_destination)
    okay_button.bind('<Return>', okay)
    exit_button.bind('<Return>', terminate)
    # Display widgets.
    source_entry.grid(row=0, column=0, padx=5, pady=5)
    source_button.grid(row=0, column=1, padx=5, pady=5)
    destination_entry.grid(row=0, column=0, padx=5, pady=5)
    destination_button.grid(row=0, column=1, padx=5, pady=5)
    source.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
    destination.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
    okay_button.grid(row=2, column=0, padx=5, pady=5, sticky='news')
    exit_button.grid(row=2, column=1, padx=5, pady=5, sticky='news')
    # Execute the main loop.
    master.mainloop()

def browse_source(event=None):
    # Get the selected source.
    path = source_dialog.show()
    if path:
        # Replace the text.
        source_entry.delete(0, Tkinter.END)
        source_entry.insert(0, os.path.realpath(path))

def browse_destination(event=None):
    # Get the selected destination.
    path = destination_dialog.show()
    if path:
        # Replace the text.
        destination_entry.delete(0, Tkinter.END)
        destination_entry.insert(0, os.path.realpath(path))

def okay(event=None):
    source = source_entry.get()
    # Does the source exist?
    if os.path.exists(source):
        # Is the source a directory?
        if os.path.isdir(source):
            destination = destination_entry.get()
            # Does the destination exist?
            if os.path.exists(destination):
                # Is the destination a directory?
                if os.path.isdir(destination):
                    master.withdraw()
                    try:
                        backup(source, destination)
                    except:
                        tkMessageBox.showerror(title='Error', message='The backup could not be completed.')
                    master.deiconify()
                else:
                    tkMessageBox.showwarning(title='Warning', message='The destination is not a directory.')
            else:
                tkMessageBox.showwarning(title='Warning', message='The destination does not exist.')
        else:
            tkMessageBox.showwarning(title='Warning', message='The source is not a directory.')
    else:
        tkMessageBox.showwarning(title='Warning', message='The source does not exist.')

def backup(source, destination, errors=None):
    # Check for recursion level.
    if errors is None:
        errors = list()
        root = True
    else:
        root = False
    # Copy all directories and files from source to destination.
    for name in os.listdir(source):
        source_name = os.path.join(source, name)
        destination_name = os.path.join(destination, name)
        try:
            if os.path.isdir(source_name):
                os.mkdir(destination_name)
                backup(source_name, destination_name, errors)
            elif os.path.isfile(source_name):
                binary = open(source_name, 'rb')
                file(destination_name, 'wb').write(binary.read())
                binary.close()
        except:
            errors.append('%s\n%s' % (source_name, destination_name))
    # Write an error log if needed.
    if root and errors:
        file(os.path.join(os.path.dirname(sys.argv[0]), 'error.log'), 'w').write('\n\n'.join(errors))

def terminate(event=None):
    # Terminate the program.
    master.quit()

if __name__ == '__main__':
    main()
