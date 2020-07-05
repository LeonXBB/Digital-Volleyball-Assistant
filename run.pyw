import subprocess
import os

directory = os.getcwd()
subprocess.run(f'cmd /c "python {directory}\DVA.pyw"', shell=True)
