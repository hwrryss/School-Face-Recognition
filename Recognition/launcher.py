import os
from datetime import datetime

while True:
    now = datetime.now()

    if now.strftime('%H') == '22':
        os.system('python determinater.py')
