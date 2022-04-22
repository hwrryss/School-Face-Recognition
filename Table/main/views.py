from django.shortcuts import render
from .models import MainTable

from django.core import serializers
from django.http import HttpResponse
import json

import jwt
from .jwt_creds import jwtpayload, jwtkey

from .check_requests import check_request


def TablePage(request):
    table = MainTable.objects.order_by('grade', 'name', 'time', 'status')

    return render(request, 'main/MainTable.html', {'table': table})


def api(request):
    checkJWT = jwt.encode(jwtpayload, jwtkey, algorithm="HS256")

    if 'jwt' in request.COOKIES.keys():
        if request.COOKIES['jwt'] == checkJWT:
            if request.COOKIES['action'] == 'gather':
                data = MainTable.objects.all()
                data = serializers.serialize("json", data)

                return HttpResponse(data, content_type="application/json")

            if request.COOKIES['action'] == 'delete':
                MainTable.objects.all().delete()

            if request.COOKIES['action'] == 'add':
                table = MainTable.objects.order_by('grade', 'name', 'time', 'status')

                data = json.loads(request.body.decode("utf-8"))
                name = data["Name"]
                grade = data["Grade"]
                time = data["Time"]
                status = data["Status"]

                if check_request(table, name, status):
                    MainTable.objects.bulk_create([MainTable(grade=grade, name=name, time=time, status=status)])

    return HttpResponse('<h1>API moment</h1>')
