from django.shortcuts import render
from .models import MainTable

from django.core import serializers
from django.http import HttpResponse
import json

import jwt
from .jwt_creds import jwtpayload, jwtkey

from .check_requests import check_request

import pandas as pd

from . import rcModule


def TablePage(request):
    context = {}
    context['table'] = MainTable.objects.order_by('grade', 'name', 'time', 'status')

    colors = []
    table = context['table'].values()
    table = pd.DataFrame(table).to_dict(orient="list")

    for status in table['status']:
        colors.append('#E35C5C') if status == 'Left' else colors.append('#94E35C') #yellow - '#E3CF5C'

    context['colors'] = colors

    if request.GET:
        req = request.GET['grade']
        context['table'].filter(name=req.split()[1]).update(grade=req.split()[0])

    return render(request, 'main/MainTable.html', {'table': zip(context['table'], context['colors'])})


def api(request):
    checkJWT = jwt.encode(jwtpayload, jwtkey, algorithm="HS256")

    if 'jwt' in request.COOKIES.keys():
        if request.COOKIES['jwt'] == checkJWT:
            if request.COOKIES['action'] == 'report':
                data = MainTable.objects.order_by('grade', 'name', 'time', 'status')
                rcModule.createReport(data)

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
