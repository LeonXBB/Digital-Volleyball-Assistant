'''
run.py is a so-called "shell-script" created because there's a need to import main script's dependencies
during runtime and not compiling. It does so by running DVA.pyw in Python without compiling it. 
Executables created with pyinstaller have their own Python interpreter in them so it is irrelavent whether
user has Python installed or not. Kivy is imported implicitly.

First, 'directory' variable is created which contains current directory (directory = os.getcwd())
Then, the exact command that's being executed is 
'subprocess.run(f'cmd /c "python {directory}\DVA.pyw"', shell=True)'. Shell is set to True because otherwise 
Kivy's terminal window appears.
'''

import subprocess
import os

directory = os.getcwd()
subprocess.run(f'cmd /c "python {directory}\DVA.pyw"', shell=True)
