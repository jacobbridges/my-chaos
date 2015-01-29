#!/usr/bin/env python
"""
Add a webpage to the local web.
"""

################################################################################
# Imports
import subprocess
import json
import sys


################################################################################
# Main Function
def main():
    if len(sys.argv) < 3:
        print "\nUsage: add <url> <depth>"
        return
    print json.dumps(sys.argv)
    subprocess.call(["wget", "-E", "-H", "-k", "-p", "-O", "./web", "--convert-links", sys.argv[1]], shell=True)
    
if __name__ == '__main__':
    main()