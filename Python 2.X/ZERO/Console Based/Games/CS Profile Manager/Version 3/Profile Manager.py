import cmd
import sys
import os

################################################################################

class View(cmd.Cmd):

    def preloop(self):
        'Setup the command prompt.'
        self.intro = 'Profile Manager v3.0'
        self.intro += '\n' + self.ruler * len(self.intro)
        self.prompt = '>>> '
        self.use_rawinput = False
        self.cmdqueue.extend(sys.argv[1:])
        self.oldname = ''
        try:
            self.control = Profile_Manager('Profile.dat', 'save',
                                           'Doukutsu.exe', 1478656,
                                           HASH) # CALC HASH -- TODO
            self.error = False
        except Exception, reason:
            self.reason = reason
            self.error = True

    def precmd(self, line):
        'Look for Profile_Manager error.'
        if self.error:
            return 'exit'
        return line

    def postloop(self):
        'Provide proper shutdown messages.'
        if self.error:
            self.stdout.write(self.reason.message)
        else:
            self.stdout.write('Goodbye.')

    def do_shell(self, arg):
        'shell <command>\nPass argument to the command prompt.'
        os.system(arg)

    def do_save(self, arg):
        'save <name>\nSave profile by name or alias.'
        try:
            self.control.save(arg)
        except Exception, reason:
            self.stdout.write(reason.message + '\n')

    def do_load(self, arg):
        'load <name>\nLoad profile by name or alias.'
        try:
            self.control.load(arg)
        except Exception, reason:
            self.stdout.write(reason.message + '\n')
    
    def do_delete(self, arg):
        'delete <name>\nDelete profile by name or alias.'
        try:
            self.control.away(arg)
        except Exception, reason:
            self.stdout.write(reason.message + '\n')

    def do_rename(self, arg):
        'rename <old>\nrename <new>\nRename profile by name or alias.'
        if self.oldname and arg:
            try:
                self.control.rename(self.oldname, arg)
            except Exception, reason:
                self.stdout.write(reason.message + '\n')
            self.oldname = ''
        else:
            self.oldname = arg

    def do_import(self, arg):
        'import <file>\nImport profiles from file.'
        try:
            self.control.import_(arg, 'Doukutsu Monogatari')
        except Exception, reason:
            self.stdout.write(reason.message + '\n')

    def do_export(self, arg):
        'export <file>\nExport profiles from file.'
        try:
            self.control.export_(arg, 'Doukutsu Monogatari')
        except Exception, reason:
            self.stdout.write(reason.message + '\n')

    def do_show(self, arg):
        'show\nShow profiles with aliases.'
        names = self.control.names()
        if names:
            for alias, name in enumerate(names):
                self.stdout.write('(%s) %s\n' % (alias + 1, name))
        else:
            self.stdout.write('NO PROFILES LOADED\n')

    def do_exit(self, arg):
        'exit\nExit the profile manager.'
        return True
