from subprocess import Popen

import psutil

for process in psutil.process_iter():
    if process.cmdline() == ['python3.9', '__main__.py', '--ssl', '-d', './upload', '--password', '*', '--env', 'PROD']:
        print('Process found. Terminating it.')
        process.terminate()
        break

print('Pull code')
git_pull_process = Popen(["git", "pull"])
git_pull_process.wait()

print('Install deps')
pip_process = Popen(["pip3.9", "install", "-r", "requirements.txt"])
pip_process.wait()

print('Starting server...')
server = Popen(['python3.9', '__main__.py', '--ssl', '-d', './upload', '--password', '*', '--env', 'PROD'])
