import os
from datetime import datetime

while True:
    now = datetime.now()

    if int(now.strftime('%H')) < int('22'):
        os.system('python determinater.py')
