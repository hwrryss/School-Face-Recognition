from django.shortcuts import render
from .models import Person

from django.core import serializers
from django.http import HttpResponse
import json

import jwt
from .jwt_creds import jwtpayload, jwtkey

from .check_requests import check_request

import pandas as pd

from . import rcModule
from . import utils

filt = '5С'

def TablePage(request):
    context = {}
    context['table'] = Person.objects.order_by('grade', 'name', 'time', 'status')
    context['colors'] = []
    everyone = utils.parseStudents()
    table = context['table'].values()
    table = pd.DataFrame(table).to_dict(orient="list")
    global filt

    for entity in everyone:
        if table:
            if entity[1] not in table['name']:
                Person.objects.create(grade = entity[0], name = ' '.join(entity[1:]), status = 'Неизвестно', time = '00:00:00', reason = 'Неизвестно')
        else:
            Person.objects.create(grade = entity[0], name = ' '.join(entity[1:]), status = 'Неизвестно', time = '00:00:00', reason = 'Неизвестно')

    req = request.GET

    if req:
        if 'reason' in req.keys():
            req = request.GET['reason']
            context['table'].filter(name=' '.join(req.split()[1:])).update(reason=req.split()[0])
        else:
            req = request.GET['filter']
            filt = req

    if table:
        for status, reason in zip(table['status'], table['reason']):
            if status == 'Вошел':
                context['colors'].append('#A0E35C')

            elif status == 'Неизвестно':
                if reason == 'Неизвестно':
                    context['colors'].append('#D3C85E')
                else:
                    context['colors'].append('E3B85C')

            else:
                context['colors'].append('#D3655E')


    return render(request, 'main/MainTable.html', {'table': zip(context['table'], context['colors']), 'filter': filt} if context['table'] else {})


def api(request):
    checkJWT = jwt.encode(jwtpayload, jwtkey, algorithm="HS256")

    if 'jwt' in request.COOKIES.keys():
        if request.COOKIES['jwt'] == checkJWT:
            if request.COOKIES['action'] == 'report':
                data = Person.objects.order_by('grade', 'name', 'time', 'status')
                rcModule.createReport(data)

            if request.COOKIES['action'] == 'delete':
                Person.objects.all().delete()

            if request.COOKIES['action'] == 'add':
                table = Person.objects.order_by('grade', 'name', 'time', 'status')

                data = json.loads(request.body.decode("utf-8"))
                name = data["Name"]
                grade = data["Grade"]
                time = data["Time"]
                status = data["Status"]

                if check_request(table, name, status):
                    Person.objects.bulk_create([Person(grade=grade, name=name, time=time, status=status)])

    return HttpResponse('<h1>API moment</h1>')
