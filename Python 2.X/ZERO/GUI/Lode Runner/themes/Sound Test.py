import os, winsound
raw_input('There are %s sound files.' % len([winsound.PlaySound(os.path.join(root, name), winsound.SND_FILENAME) for root, dirs, files in os.walk(os.getcwd()) for name in files if '.' not in name]))
