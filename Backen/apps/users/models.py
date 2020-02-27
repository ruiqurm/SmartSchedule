from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import Permission
from friendship.models import Friend,Follow


class OrgProfile(models.Model):
    verified_name = models.CharField(max_length=50,verbose_name="认证名称",unique=True)
    def __str__(self):
        return f"认证名称:{self.verified_name}"

class UserProfile(AbstractUser):
    username = models.CharField(max_length=30,verbose_name="用户名",unique=True)
    email = models.EmailField(verbose_name="邮箱",unique=True)
    org = models.OneToOneField(OrgProfile,on_delete=models.CASCADE,verbose_name="机构号信息",
                                related_name="user",null=True)
    def __str__(self):
        return f"用户名:{self.username}"
# class Friendship(models.Model):
#     user = models.ForeignKey(UserProfile, verbose_name="用户1",
#                                  on_delete=models.DO_NOTHING,
#                                  related_name="user_friend")
#     friend = models.ForeignKey(UserProfile, verbose_name="用户2",
#                             on_delete=models.DO_NOTHING,
#                             related_name="friend_user")
#
#     def __str__(self):
#         return f"user:{self.user},friend:{self.friend}"
#
# TODO:好友请求
# class FriendshipRequest(models.Model):
#     pass
#
# class Follow(models.Model):
#     followed = models.ForeignKey(OrgProfile,verbose_name="被关注者",
#                              on_delete=models.DO_NOTHING,
#                              related_name="followed_user")
#     fan = models.ForeignKey(UserProfile,verbose_name="粉丝",
#                              on_delete=models.DO_NOTHING,
#                              related_name="follower_user")
#     def __str__(self):
#         return f"{self.fan}--->{self.followed}"
#

class Group(models.Model):
    name = models.CharField(max_length=32,verbose_name="团队名")