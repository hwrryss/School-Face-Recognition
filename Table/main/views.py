from django.shortcuts import render
from .models import Person

from django.http import HttpResponse
import json

import jwt
from .jwt_creds import jwtpayload, jwtkey

from .check_requests import check_request

import pandas as pd

from . import rcModule
from . import utils

from django.contrib.auth import get_user_model

User = get_user_model()
users = User.objects.all()

filt_dict = {'Dycent': '8С'}


def TablePage(request):
    global filt_dict

    User = get_user_model()
    users = User.objects.all()
    users = users.values()
    users = pd.DataFrame(users).to_dict(orient="list")
    users = users['username']

    for user in users:
        if user not in filt_dict:
            filt_dict[user] = '5С'

    context = {}
    context['table'] = Person.objects.order_by('grade', 'name', 'time', 'status')
    context['colors'] = []
    everyone = utils.parseStudents()
    table = context['table'].values()
    table = pd.DataFrame(table).to_dict(orient="list")
    filt = '5С'

    username = None
    if request.user.is_authenticated:
        username = request.user.username
        filt = filt_dict[username]

    for entity in everyone:
        if table:
            if entity[1] not in table['name']:
                Person.objects.create(grade=entity[0], name=' '.join(entity[1:]), status='Неизвестно', time='00:00:00',
                                      reason='Неизвестно')
        else:
            Person.objects.create(grade=entity[0], name=' '.join(entity[1:]), status='Неизвестно', time='00:00:00',
                                  reason='Неизвестно')

    req = request.GET

    if req:
        if 'reason' in req.keys():
            req = request.GET['reason']
            context['table'].filter(name=' '.join(req.split()[1:])).update(reason=req.split()[0])

        elif 'filter' in req.keys():
            req = request.GET['filter']
            filt = req
            filt_dict[username] = filt

        elif 'report' in req.keys():
            req = request.GET['report']
            data = []

            for i in range(len(table['name'])):
                if table['grade'][i] == req and table['name'][i] not in data:
                    data.append([table['name'][i].split()[0], table['status'][i], table['reason'][i]])

            rcModule.sendForm(data, req)

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

    return render(request, 'main/MainTable.html',
                  {'table': zip(context['table'], context['colors']), 'filter': filt} if context['table'] else {})


def TimeTablePage(request):
    context = {}
    context['table'] = Person.objects.order_by('grade', 'name', 'time', 'status')
    context['existing'] = False

    for ind, row in enumerate(context['table']):
        if str(row.time) != '00:00:00':
            context['existing'] = True

        context['table'][ind].time = str(row.time)

    return render(request, 'main/TimeTable.html', context)


def AboutPage(request):
    return render(request, 'main/About.html')


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
                    Person.objects.filter(name=name).update(grade=grade, name=name, time=time, status=status)

    return HttpResponse('<h1>API moment</h1>')
