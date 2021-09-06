
from django.core.management import call_command
def my_backup():
    try:
        call_command('dbbackup')
    except:
        pass
#if you like run back up in  terminal run this code  python3 manage.py crontab add
