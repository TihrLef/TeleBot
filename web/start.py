import subprocess
import threading
import time
import sys

PORT = 8000

def runserver():
	subprocess.run([sys.executable, "./manage.py", "runserver", "0.0.0.0:"+str(PORT)])

def runbot():
	subprocess.run([sys.executable, "./manage.py", "bot"])

serv = threading.Thread(target=runserver)
serv.start()
time.sleep(1)
print()
print()
bot = threading.Thread(target=runbot)
bot.start()