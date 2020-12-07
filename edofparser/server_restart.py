from subprocess import Popen

import psutil

for process in psutil.process_iter():
    if process.cmdline() == ['python', '__main__.py', '--ssl', '-d', './upload', '--password', '*', '--env', 'PROD']:
        print('Process found. Terminating it.')
        process.terminate()
        break

print('Process not found or stopped: starting it.')
Popen(['python', '__main__.py', '--ssl', '-d', './upload', '--password', '*', '--env', 'PROD'])
