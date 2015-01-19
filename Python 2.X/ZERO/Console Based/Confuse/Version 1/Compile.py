from distutils.core import setup
import py2exe
import sys

sys.argv.append('py2exe')

setup(console=['confuse_1.py', 'confuse_2.py'],
      options={'py2exe': {'ascii': 1,
                          'bundle_files': 1,
                          'compressed': 1,
                          'optimize': 2}},
      zipfile=None)
