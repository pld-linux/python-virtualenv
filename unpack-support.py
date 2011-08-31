#!/usr/bin/python

import re
import os
import sys

cmd_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(cmd_folder, '..'))

import virtualenv

file_regex = re.compile(
        r'##file (.*?)\n([a-zA-Z][a-zA-Z0-9_]+)\s*=\s*convert\("""(.*?)"""\)',
        re.S)

f = open('virtualenv.py', 'rb')
content = f.read()
f.close()
match = None
for match in file_regex.finditer(content):
	f = open(os.path.join('virtualenv_support', match.group(1)), 'wb')
	f.write(eval("virtualenv." + match.group(2)))
	f.close()
