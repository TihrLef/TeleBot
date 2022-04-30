import subprocess
import sys

subprocess.run([sys.executable,"manage.py", "makemigrations"])
subprocess.run([sys.executable, "manage.py", "migrate"])

subprocess.run([sys.executable, "manage.py", "shell"], text=True, input="from Users.models import User\n\
admin = User.objects.create(telegram_id=-1, username='admin', password = 'Berlingo', is_active=True, is_staff=True, is_superuser = True)\n\
admin.save()")