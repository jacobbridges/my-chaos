import os
import cmd
import spice
import random
import cStringIO

################################################################################

class Interface(cmd.Cmd):

    def preloop(self):
        'Setup the command prompt.'
        self.prompt = '>>> '
        self.intro = 'CS Profile Manager v2.0'
        self.intro += '\n' + self.ruler * len(self.intro)
        self.use_rawinput = False
        try:
            self.control = Profile_Manager('Profile.dat', 'save',
                                           'Doukutsu.exe', 1478656, 260997856)
            self.error = False
        except Exception, reason:
            self.reason = reason
            self.error = True

    def precmd(self, line):
        'Look for Profile_Manager error.'
        if self.error:
            return 'quit'
        return line

    def postloop(self):
        'Provide proper shutdown messages.'
        if self.error:
            self.stdout.write(self.reason.message)
        else:
            self.stdout.write('Goodbye.')

    def do_shell(self, arg):
        'shell <arg>\nPass argument to the command prompt.'
        os.system(arg)

    def do_save(self, arg):
        'save <arg>\nSave profile by name or alias.'
        try:
            self.control.save(arg)
        except Exception, reason:
            self.stdout.write(reason.message + '\n')

    def do_list(self, arg):
        'list\nList profiles with their aliases.'
        try:
            array = self.control.list()
            if array:
                for alias, name in enumerate(self.control.list()):
                    self.stdout.write('(%s) %s\n' % (alias + 1, name))
            else:
                self.stdout.write('NO PROFILES LOADED\n')
        except Exception, reason:
            self.stdout.write(reason.message + '\n')

    def do_load(self, arg):
        'load <arg>\nLoad profile by name or alias.'
        try:
            self.control.load(arg)
        except Exception, reason:
            self.stdout.write(reason.message + '\n')

    def do_away(self, arg):
        'away <arg>\nDelete profile by name or alias.'
        try:
            self.control.away(arg)
        except Exception, reason:
            self.stdout.write(reason.message + '\n')

    def do_quit(self, arg):
        'quit\nExit the profile manager.'
        return True

################################################################################

class Profile_Manager:

    STRING = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    def __init__(self, filename, savepath,
                 testfile=None, testsize=None, testhash=None):
        'Initialize the Profile Manager object.'
        if testfile is not None:
            self.test(testfile, testsize, testhash)
        self.filename = filename
        self.savepath = savepath
        self.autoload()

    def test(self, testfile, testsize, testhash):
        'Perform tests instructed by the caller.'
        assert os.path.exists(testfile), '%r does not exist.' % testfile
        assert os.path.isfile(testfile), '%r is not a file.' % testfile
        if testsize is not None:
            assert os.path.getsize(testfile) == testsize, \
                   '%r has an invalid size.' % testfile
        if testhash is not None:
            assert hash(file(testfile, 'rb').read()) == testhash, \
                   '%r has an invalid hash.' % testfile

    def autoload(self):
        'Automatically load available profiles.'
        self.profiles = {}
        if not os.path.exists(self.savepath):
            os.makedirs(self.savepath)
        else:
            for path, dirs, data in os.walk(self.savepath):
                for name in data:
                    self.autoread(os.path.join(path, name))
        self.aliases = self.profiles.keys()

    def autoread(self, pathname):
        'Read in profiles from their pathnames.'
        # Create the keys.
        random.seed(int(os.path.getctime(pathname)))
        major = spice.major()
        minor = spice.minor()
        # Decode the file.
        string = cStringIO.StringIO()
        spice.decode(open(pathname, 'rb'), string, major, minor)
        string = string.getvalue()
        # Extract the data.
        namesize = ord(string[0]) + 2
        name = string[1:namesize]
        profile = string[namesize:]
        # Archive the data.
        assert profile, '%r has no profile data.' % pathname
        self.profiles[name] = [profile, pathname, major, minor]

    def save(self, arg):
        'Save profile with name and archive.'
        assert os.path.exists(self.filename), '%r NOT FOUND' % self.filename
        assert 1 <= len(arg) <= 256, 'BAD NAME LENGTH'
        arg = self.solve(arg, False)
        profile = file(self.filename, 'rb').read()
        if arg in self.profiles:
            # Update profile and get save info.
            self.profiles[arg][0] = profile
            pathname, major, minor = self.profiles[arg][1:]
            destination = open(pathname, 'wb')
        else:
            # Create a pathname.
            random.seed()
            name = ''.join(random.sample(self.STRING, len(self.STRING)))
            pathname = os.path.join(self.savepath, name)
            while os.path.exists(pathname):
                name = ''.join(random.sample(self.STRING, len(self.STRING)))
                pathname = os.path.join(self.savepath, name)
            # Create destination and keys.
            destination = open(pathname, 'wb')
            random.seed(int(os.path.getctime(pathname)))
            major = spice.major()
            minor = spice.minor()
            # Create a new profile entry.
            self.profiles[arg] = [profile, pathname, major, minor]
            self.aliases.append(arg)
        # Save the updated profile.
        string = cStringIO.StringIO(chr(len(arg) - 1) + arg + profile)
        spice.encode(string, destination, major, minor)
        destination.close()

    def list(self):
        'Return an array of loaded profiles.'
        return tuple(self.aliases)

    def load(self, arg):
        'Load an archived profile for use.'
        arg = self.solve(arg)
        profile = self.profiles[arg][0]
        file(self.filename, 'wb').write(profile)

    def away(self, arg):
        'Detele the specified profile.'
        arg = self.solve(arg)
        os.remove(self.profiles[arg][1])
        del self.profiles[arg]
        self.aliases.remove(arg)

    def solve(self, arg, require=True):
        'Solve profile alias if given.'
        if arg not in self.profiles:
            try:
                index = int(arg) - 1
            except:
                if require:
                    raise Exception('%r NOT FOUND' % arg)
                return arg
            assert self.aliases, 'NO PROFILES LOADED'
            try:
                assert index > -1
                return self.aliases[index]
            except:
                raise Exception('INDEX OUT OF BOUNDS')
        return arg

################################################################################

if __name__ == '__main__':
    Interface().cmdloop()
