import os, sys
from getpass import getuser
from random import choice
from winreg import Key, KEY, HKEY, REG_SZ

# THIS PROGRAM CHANGES SETTINGS IN THE REGISTRY
# HOWEVER, IT IS NOT SUCCESSFUL AT CHANGING THE
# BACKGROUND

def main():
    install()
    change_background()

def install():
    # Where is the python interpreter?
    python = r'C:\Python25\pythonw.exe'
    # What key do we need to access?
    hive = HKEY.LOCAL_MACHINE
    subkey = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
    # What do we need to write and where?
    value = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    data = REG_SZ('"%s" "%s"' % (python, sys.argv[0]))
    # Install the program.
    Key(hive, subkey, KEY.WRITE).values[value] = data

def change_background():
    # What key do we need to access?
    hive = HKEY.CURRENT_USER
    subkey = r'Control Panel\Desktop'
    # What do we need to write and where?
    value = 'ConvertedWallpaper'
    data = REG_SZ(choose_background())
    # Change the background.
    Key(hive, subkey, KEY.WRITE).values[value] = data
    # Change the theme.
    subkey = r'Software\Microsoft\Windows\CurrentVersion\Themes\LastTheme'
    value = 'Wallpaper'
    data = REG_SZ(os.path.join('%USERPROFILE%', data.value.split('\\%s\\' % getuser(), 1)[1]))
    Key(hive, subkey, KEY.WRITE).values[value] = data

def choose_background():
    # Where are our pictures?
    root = r'C:\Documents and Settings\%s\My Documents\My Pictures' % getuser()
    # What is there to choose from?
    files = [os.path.join(root, picture) for root, dirs, files in os.walk(root) for picture in files if os.path.splitext(picture)[1].lower() == '.jpg']
    # Return the new picture.
    return choice(files)

if __name__ == '__main__':
    main()
