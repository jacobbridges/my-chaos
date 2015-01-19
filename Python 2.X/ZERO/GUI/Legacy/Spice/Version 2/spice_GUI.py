import os
import spice_coding
import spice_key
import sys
import tkFileDialog
import Tkinter

################################################################################

class Application:

    LIMIT_FLAG = True
    LIMIT_SIZE = 1024 ** 2

    def __init__(self):
        self.__root = Tkinter.Tk()
        self.__root.title('SPICE')
        self.__root.resizable(False, False)
        Tkinter.Button(self.__root, text=' Create Key ', font='Courier 10', \
                       command=self.key).grid(row=0, column=0, padx=5, pady=5)
        Tkinter.Button(self.__root, text='Encrypt File', font='Courier 10', \
                       command=self.enc).grid(row=0, column=1, padx=5, pady=5)
        Tkinter.Button(self.__root, text='Exit Program', font='Courier 10', \
                       command=sys.exit).grid(row=1, column=0, padx=5, pady=5)
        Tkinter.Button(self.__root, text='Decrypt File', font='Courier 10', \
                       command=self.dec).grid(row=1, column=1, padx=5, pady=5)
        self.__open = tkFileDialog.Open()
        self.__save = tkFileDialog.SaveAs()
        self.__fold = tkFileDialog.Directory()
        self.__root.mainloop()

    def key(self):
        self.__root.withdraw()
        print 'Type in the name of the new key files.'
        while True:
            filename = self.__save.show()
            try:
                if filename:
                    major = open(filename + '.major', 'wb', 0)
                    minor = open(filename + '.minor', 'wb', 0)
                    major.write(spice_key.new_night_key( \
                        spice_key.new_major_key()))
                    minor.write(spice_key.new_night_key( \
                        spice_key.new_minor_key()))
                    major.close()
                    minor.close()
                break
            except Exception, error:
                print 'ERROR:', error
        self.__clean_screen()
        self.__root.deiconify()

    def enc(self):
        self.__root.withdraw()
        source, name = self.__get_source(False)
        if source:
            print 'Select the destination folder.'
            destination = self.__fold.show()
            if destination:
                major, minor = self.__get_keys()
                if major and minor:
                    name = os.path.basename(name) + '.spice'
                    destination = os.path.join(destination, name)
                    destination = file(destination, 'wb', 0)
                    destination.write(spice_coding.encode(major, minor, source))
                    destination.close()
        self.__clean_screen()
        self.__root.deiconify()

    def dec(self):
        self.__root.withdraw()
        source, name = self.__get_source(True)
        if source:
            print 'Select the destination folder.'
            destination = self.__fold.show()
            if destination:
                major, minor = self.__get_keys()
                if major and minor:
                    name = os.path.basename(name)[:-6]
                    destination = os.path.join(destination, name)
                    destination = file(destination, 'wb', 0)
                    destination.write(spice_coding.decode(major, minor, source))
                    destination.close()
        self.__clean_screen()
        self.__root.deiconify()

    def __get_source(self, decrypt):
        print 'Select the source file.'
        while True:
            filename = self.__open.show()
            try:
                if filename:
                    if decrypt:
                        assert os.path.getsize(filename) % 4 == 0, \
                               'File size is not a multiple of 4.'
                    elif self.LIMIT_FLAG:
                        assert os.path.getsize(filename) <= self.LIMIT_SIZE, \
                               'File size exceeds ' + \
                               str(self.LIMIT_SIZE) + \
                               ' bytes.'
                    return file(filename, 'rb', 0).read(), filename
                return None, None
            except Exception, error:
                print 'ERROR:', error

    def __get_keys(self):
        print 'Select a key file.'
        while True:
            filename = self.__open.show()
            try:
                if filename:
                    filename = filename[:-5]
                    major = file(filename + 'major', 'rb', 0).read()
                    minor = file(filename + 'minor', 'rb', 0).read()
                    return spice_key.new_dream_key(major), \
                           spice_key.new_dream_key(minor)
                return None, None
            except Exception, error:
                print 'ERROR:', error

    def __clean_screen(self):
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix' or os.name == 'mac':
            os.system('clear')

################################################################################

if __name__ == '__main__':
    Application()
