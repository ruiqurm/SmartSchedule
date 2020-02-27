import datetime

from rest_framework import generics
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin,UpdateModelMixin,\
                                DestroyModelMixin,CreateModelMixin
from rest_framework.response import Response
from django.db.models import Q
from friendship.models import Follow,Friend
from apps.schedules.serializer import ScheduleSerializer,ScheduleTableSerializer,\
                                      TodoSerializer,PostSerializer
from apps.schedules.models import Schedule,ScheduleTable,Todo
from apps.users.models import UserProfile
from apps.utils.permission import IsOwner


"""
TODO:添加一个分页器
"""

class ScheduleViewset(RetrieveModelMixin,UpdateModelMixin,
                      DestroyModelMixin,viewsets.GenericViewSet,
                      CreateModelMixin):
    """
    通过pk对Schedule进行获取，更改，删除。
    只有用户本人才能执行以上操作。
    """
    serializer_class = ScheduleSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes =(IsAuthenticated,IsOwner)
    queryset = Schedule.objects.all()

class ScheduleTableViewset(RetrieveModelMixin,UpdateModelMixin,
                           DestroyModelMixin,CreateModelMixin,
                           viewsets.GenericViewSet):
    """
    通过pk对ScheduleTable进行创建，获取，更改，删除。
    只有用户本人才能执行以上操作。
    获取一个ScheduleTable的所有Schedule: Get /schedule/list/
    """
    serializer_class = ScheduleTableSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes =(IsAuthenticated,IsOwner)
    queryset = ScheduleTable.objects.all()

class TodoViewset(RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    通过pk对Todo进行获取，更改，删除。
    只有用户本人才能执行以上操作。
    """
    serializer_class = TodoSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes =(IsAuthenticated,IsOwner)
    queryset = Todo.objects.all()
    lookup_field = "pk"

    def list(self, request, *args, **kwargs):
        """
        返回当前用户的所有Todo
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.filter_queryset(request.user.user_todo.all())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ScheduleList(generics.ListAPIView):
    """
    给定时间和表明，返回一个用户的日程表内内容
    TODO：添加分页
    TODO：添加权限
    """
    serializer_class = ScheduleSerializer
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    def get_queryset(self):
        user_pk = self.request.user.pk
        table_title = self.request.query_params.get("table_title",
                                UserProfile.objects.get(pk=user_pk).user_table.first().title)
        if ("date" in self.kwargs):
            start_time,end_time = self.kwargs["date"][0],self.kwargs["date"][1]
            #用于检查是否有手动传参；直接解包会报错，虽然没错
        else:
            start_time,end_time = \
                self.request.query_params.get("stime",None),\
                self.request.query_params.get("etime",None),
        if not(start_time or end_time):
            #如果都没有提供
            return UserProfile.objects.get(pk=user_pk). \
                user_table.get(title=table_title).table_schedule.all()
        elif start_time is None:
            return UserProfile.objects.get(pk=user_pk). \
                user_table.get(title=table_title).table_schedule.\
            filter(Q(end_time__lte=end_time))
        elif end_time is None:
            return UserProfile.objects.get(pk=user_pk). \
                user_table.get(title=table_title).table_schedule. \
                filter(Q(start_time__gte=start_time))
        else:
            return UserProfile.objects.get(pk=user_pk). \
                user_table.get(title=table_title).table_schedule. \
                filter(Q(start_time__gte=start_time) & Q(end_time__lte=end_time))

class Postviewset(viewsets.ViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    @action(methods=['GET'],detail=False)
    def org(self,request):
        orgs = Follow.objects.following(request.user)
        posts = []
        for org in orgs:
            posts.extend(org.user_post)
        return PostSerializer(posts,many=True)

    @action(methods=['GET'], detail=False)
    def friend(self, request):
        friends = Friend.objects.friends(request.user)
        posts = []
        for friend in friends:
            posts.extend(friend.user_post)
        return PostSerializer(posts, many=True)

    # @action(methods=['GET'], detail=False)
    # def friend(self, request):
