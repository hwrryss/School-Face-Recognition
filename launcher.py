import os
from datetime import datetime

while True:
    now = datetime.now()

    if 22 > int(now.strftime('%H')) > 7:
        os.system('python3 frModule.py')
