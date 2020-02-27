from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import mixins

from django.core.exceptions import ValidationError
from rest_framework.views import exception_handler
from friendship.models import Friend,Follow

from apps.users.models import UserProfile
from apps.users.serializer import UserSerializer,FridenshipSerializer,OrgSerializer
from apps.utils.permission import IsOwner
# class FriendViewset(viewsets.GenericViewSet):
#     authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#     #serializer_class = FridenshipSerializer
#     # def list(self,request,*args,**kwargs):
#     #     return Response(UserSerializer(Friend.objects.friends(request.user),many=True).data)
#     # def get_queryset(self):
#     #     return Friend.objects.friends(self.request.user)
class UserViewset(viewsets.ViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action == 'update':
            return [IsOwner(), ]
        elif self.action == 'get' or self.action == 'post':
            return [IsAuthenticated(), ]
        else:
            return [IsAdminUser(), ]

    @action(methods=['GET', 'POST'], detail=True)
    def profile(self, request, pk=None):
        if request.method == 'GET':
            user = UserProfile.objects.get(pk=pk)
            return Response(UserSerializer(user).data)
        elif request.method == 'POST':
            instance = UserProfile.objects.get(pk=pk)
            serializer = UserSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    @action(methods=['GET'],detail=True,url_path="info/posts")
    def get_post_info_from_org(self):
        """
        获取机构号发布的post
        :return:
        """
        pass
class OrgViewset(viewsets.ViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    def get_permissions(self):
        if self.action == 'update':
            return [IsOwner(),IsAdminUser()]
        elif self.action == 'get'or self.action=='post':
            return [IsAuthenticated(),]
        else:
            return [IsAdminUser(),]

    @action(methods=['GET','UPDATE'],detail=True)
    def profile(self,request,pk=None):
        """
        TODO:可能需要进一步调试
        """
        if request.method == 'GET':
            orguser = UserProfile.objects.get(pk=pk)
            if orguser.org is None:
                #TODO:以后改为统一的返回消息
                return Response("非机构号无法关注",404)
            return Response(OrgSerializer(orguser.org).data,200)
        elif request.method == 'UPDATE':
            instance = UserProfile.objects.get(pk=pk).org
            serializer = OrgSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)

    @action(methods=['GET','POST'], detail=True,url_path="follow")
    def follow(self,request,pk=None):
        """
        GET关注，POST取消关注
        """
        followee = UserProfile.objects.get(pk=pk)
        if request.method == 'GET':
            if not followee.is_org:
                return Response({"message":"无法关注非机构号"},403)
            Follow.objects.add_follower(request.user,followee)
            return Response(None,201)
        elif request.method == 'POST':
            Follow.objects.remove_follower(request.user, followee)
            return Response(None,201)

    @action(methods=['GET'], detail=True,url_path="follow/list")
    def follower(self,request,pk):
        """
        TODO:返回关注者列表 待做
        :param request:
        :param pk:
        :return:
        """
        return Response(None,status=404)
    @action(methods=['GET'], detail=True)
    def post(self,request,pk):
        """
        TODO:返回历史POST 待做
        :param request:
        :param pk:
        :return:
        """
        return Response(None, status=404)

