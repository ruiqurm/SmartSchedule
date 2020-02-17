import datetime

from django.urls import path,re_path
from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter

from apps.schedules.views import ScheduleList,ScheduleViewset,ScheduleTableViewset,\
                                 TodoViewset
from apps.utils.date import this_day,this_week,this_month,next_7days,next_30days

router = DefaultRouter()

router.register(r"schedule",ScheduleViewset,basename="schedule")
router.register(r"scheTable",ScheduleTableViewset,basename="scheTable")
router.register(r"todo",TodoViewset,basename="todo")
#router.register(r"todo/list",TodoList,basename="todolist")

urlpatterns = [
    re_path(r"^schedule/list/",include([
        url(r"^day",ScheduleList.as_view(),{"date":this_day()}),
        url(r"^week",ScheduleList.as_view(),{"date":this_week()}),
        url(r"^7days",ScheduleList.as_view(),{"date":next_30days()}),
        url(r"^month",ScheduleList.as_view(),{"date":this_month()}),
        url(r"^30days",ScheduleList.as_view(),{"date":next_7days()}),
    ])),
    re_path(r"^schedule/list/",ScheduleList.as_view()),
    url(r"^",include(router.urls)),

]