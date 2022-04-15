from django.shortcuts import render
from .models import MainTable

from django.http import HttpResponse

import jwt
import json
from .jwt_creds import jwtpayload, jwtkey

from .check_requests import check_request

def TablePage(request):
    table = MainTable.objects.order_by('grade', 'name', 'time', 'status')

    return render(request, 'main/MainTable.html', {'table': table})


def api(request):
    checkJWT = jwt.encode(jwtpayload, jwtkey, algorithm="HS256")

    if 'jwt' in request.COOKIES.keys():
        if request.COOKIES['jwt'] == checkJWT:
            table = MainTable.objects.order_by('grade', 'name', 'time', 'status')

            data = json.loads(request.body.decode("utf-8"))
            name = data["Name"]
            grade = data["Grade"]
            time = data["Time"]
            status = data["Status"]

            if check_request(table, name, status):
                MainTable.objects.bulk_create([MainTable(grade=grade, name=name, time=time, status=status)])

    return HttpResponse('<h1>API moment</h1>')
