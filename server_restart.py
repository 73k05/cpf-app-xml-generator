import psutil
from subprocess import Popen

for process in psutil.process_iter():
    if process.cmdline() == ['python', 'simple_http_server.py']:
        print('Process found. Terminating it.')
        process.terminate()
        break
else:
    print('Process not found: starting it.')
    Popen(['python', 'simple_http_server.py'])