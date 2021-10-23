import os
from datetime import datetime

while True:
    now = datetime.now()

    if int(now.strftime('%H')) < 22 and int(now.strftime('%H')) > 7:
        os.system('python determinater.py')
