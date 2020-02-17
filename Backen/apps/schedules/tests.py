from django.test import TestCase

import datetime

from apps.users.models import UserProfile
from apps.schedules.models import Schedule, ScheduleTable,Todo

user = UserProfile.objects.all().get(username="admin")
ST = ScheduleTable(title="测试",user=user)
ST.save()

l = [Schedule(start_time = datetime.datetime(2020, 2, 9, 21, 17),
         end_time = datetime.datetime(2020, 2, 9, 22, 17),
         title="测试的日程单项",
         weight = 9,
         user = user,
         table = ST),
Schedule(start_time = datetime.datetime(2020, 2, 10, 21, 17),
         end_time = datetime.datetime(2020, 2, 10, 22, 17),
         title="测试的日程单项",
         weight = 9,
         user = user,
         table = ST),
Schedule(start_time = datetime.datetime(2020, 2, 8, 21, 17),
         end_time = datetime.datetime(2020, 2, 8, 22, 17),
         title="测试的日程单项",
         weight = 9,
         user = user,
         table = ST)]
Todo.objects.create(title="数分",user=user)
Todo.objects.create(title="模电",user=user)
Todo.objects.create(title="数据结构",user=user)
for i in l:
    i.save()
