from distutils.core import setup
import py2exe
import sys

sys.argv.extend(["py2exe", "-q"])

################################################################

RT_MANIFEST = 24

manifest_template = '''
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

################################################################

class Target:
    version = "0.1.2"
    company_name = "West Coast Baptist College"
    copyright = "Freeware"
    name = "Heaven VS Hell"
    description = "Interactive Illustration"
    script = "Heaven VS Hell.pyw"
    other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog="Heaven VS Hell"))]
    icon_resources = [(1, "data\\icon.ico")]
    dest_base = "Heaven VS Hell"

################################################################

setup(
    options = {"py2exe": {"compressed": 1,
                          "optimize": 2,
                          "ascii": 1,
                          "bundle_files": 1}},
    zipfile = None,
    windows = [Target],
    )
