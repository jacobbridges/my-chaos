import distutils.core
import os
import py2exe
import sys

import dfs

################################################################################

MANIFEST_TEMPLATE = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
/>
<description>%(prog)s Program</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
'''

################################################################################

def main(program_name):
    sys.argv.extend(["py2exe", "-q"])
    build_exe(program_name)
    concatenate(program_name)
    final_clean(program_name)

################################################################################

def build_exe(program_name):
    class Target:
        version = '1.0'
        company_name = 'West Coast Baptist College'
        copyright = 'Freeware'
        name = program_name
        description = 'Game Installer'
        script = 'Installer.pyw'
        other_resource = [(24, 1, MANIFEST_TEMPLATE % dict(prog=program_name))]
        icon_resources = [(1, 'icon.ico')]
        dest_base = 'Install %s' % program_name
    distutils.core.setup(
        options={'py2exe': {'compressed': 1,
                            'optimize': 2,
                            'ascii': 1,
                            'bundle_files': 1}},
        windows=[Target])

################################################################################

def concatenate(program_name):
    destination = file('dist\\Install %s.exe' % program_name, 'ab')
    destination.seek(0, 2)
    files = dfs.Acquire(destination)
    for name in os.listdir('Root'):
        files.acquire(os.path.join('Root', name))
    destination.close()

################################################################################

def final_clean(program_name):
    os.remove('dfs.pyc')
    os.remove('dist\\MSVCR71.dll')
    os.remove('dist\\w9xpopen.exe')
    os.rename('dist', 'Installer')
    for r, d, f in os.walk('build', False):
        for n in f:
            os.remove(os.path.join(r, n))
        os.rmdir(r)
    
################################################################################

if __name__ == '__main__':
    main('Reaction')
