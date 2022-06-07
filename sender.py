import requests

import jwt
from jwt_creds import jwtkey, jwtpayload

url = "http://127.0.0.1:8000/api"


def sendData(Grade, Name, Time, Status, Action):
    token = jwt.encode(jwtpayload, jwtkey, algorithm="HS256")
    cookies = {"jwt": token, "action": Action}

    requests.get(url, json={'Grade': Grade, "Name": Name, "Time": Time, "Status": Status}, cookies=cookies)
